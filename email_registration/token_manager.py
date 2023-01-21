import logging
from datetime import datetime
from datetime import timedelta
from binascii import Error as BASE64ERROR
from base64 import urlsafe_b64encode, urlsafe_b64decode
from django.contrib.auth.tokens import default_token_generator
from django.core import signing
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36

#from django.contrib.auth import get_user_model
#from django.contrib.auth.tokens import default_token_generator

#from .app_configurations import GetFieldFromSettings
from .errors import (UserAlreadyActive,
                     MaxRetriesExceeded,
                     UserNotFound,
                     WrongTimeInterval,
                     InvalidToken
                     )
import sqlalchemy as sa
import ofjustpy as oj
__all__ = [
    "TokenManager"
]

logger = logging.getLogger(__name__)

max_retries = 2
max_age = None
_time_units = ['s', 'm', 'h', 'd']
secret=key = "my secret key"  #self.settings.get('key', raise_exception=False)
key_salt = None #self.settings.get('salt', raise_exception=False)
sep = ":" #self.settings.get('sep', raise_exception=False)
#TODO: need to fix this
algorithm ="sha256"
# https://stackoverflow.com/questions/21155264/setting-expiration-time-to-django-password-reset-token
PASSWORD_RESET_TIMEOUT = 259200 # 3 days, in seconds

def perform_encoding(plain_entity):
    return urlsafe_b64encode(str(plain_entity).encode('UTF-8')).decode('UTF-8')

    
def __generate_token(user):
    """
    If "EXPIRE_AFTER" is specified in settings.py,
    will generate a timestamped signed encrypted token for
    user, otherwise will generate encrypted token without timestamp.
    """
    user_token = default_token_generator.make_token(user)
    if max_age is None:
        return perform_encoding(user_token)

    signed_token = signing.TimestampSigner.sign(user_token)
    return perform_encoding(signed_token)

def _make_hash_value(user, timestamp):
    """
    Hash the user's primary key, email (if available), and some user state
    that's sure to change after a password reset to produce a token that is
    invalidated when it's used:
    1. The password field will change upon a password reset (even if the
       same password is chosen, due to password salting).
    2. The last_login field will usually be updated very shortly after
       a password reset.
    Failing those things, settings.PASSWORD_RESET_TIMEOUT eventually
    invalidates the token.

    Running this data through salted_hmac() prevents password cracking
    attempts using the reset token, provided the secret isn't compromised.
    """
    # Truncate microseconds so that tokens are consistent even if the
    # database doesn't support microseconds.
    login_timestamp = ""
    # TODO: fix thies
    # 
    # (
    #     ""
    #     if user.last_login is None
    #     else user.last_login.replace(microsecond=0, tzinfo=None)
    # )
    #Hardwiring to email and id 
    email_field = "email" #user.get_email_field_name()
    email = getattr(user, email_field, "") or ""
    return f"{user.password}{login_timestamp}{timestamp}{email}"

    
def _make_token_with_timestamp(user, timestamp, secret):
    # timestamp is number of seconds since 2001-1-1. Converted to base 36,
    # this gives us a 6 digit string until about 2069.
    ts_b36 = int_to_base36(timestamp)
    hash_string = salted_hmac(
        key_salt,
        _make_hash_value(user, timestamp),
        secret=secret,
        algorithm=algorithm,
    ).hexdigest()[
        ::2
    ]  # Limit to shorten the URL.
    return "%s-%s" % (ts_b36, hash_string)

def _num_seconds(dt):
    return int((dt - datetime(2001, 1, 1)).total_seconds())

def _now():
    # Used for mocking in tests
    return datetime.now()
    
def make_token(user):
    """
    Return a token that can be used once to do a password reset
    for the given user.
    """
    #traceback.print_stack(file=sys.stdout)
    return _make_token_with_timestamp(
        user,
        _num_seconds(_now()),
        secret,
    )
    
def generate_relative_link(inactive_user, user_email):
    """
    Generates link for the first time.
    """
    #token = __generate_token(inactive_user)
    token = make_token(inactive_user)
    encoded_email = urlsafe_b64encode(str(user_email).encode('utf-8')).decode('utf-8')

    link = f"/verification/user/verify-email/{encoded_email}/{token}/"
    return encoded_email, token

    #absolute_link = request.build_absolute_uri(link)
    # need full/a link
    #absolute_link  = link
    #request.url.host
    #return absolute_link
    return link


# ================== decrypt/verify generated token ==================
def __get_seconds(interval):
    """
    converts the time specified in settings.py "EXPIRE_AFTER" into seconds.
        By default the time will be considered in seconds, to specify days/minutes/hours
        suffix the time with relevant unit.
            - for example:
                for 1 day, it'll be : "1d"
                and so on.

        If integer is specified, that will be considered in seconds
    """
    if isinstance(interval, int):
        return interval
    if isinstance(interval, str):
        unit = [i for i in _time_units if interval.endswith(i)]
        if not unit:
            unit = 's'
            interval += unit
        else:
            unit = unit[0]
        try:
            digit_time = int(interval[:-1])
            if digit_time <= 0:
                raise WrongTimeInterval('Time must be greater than 0')

            if unit == 's':
                return digit_time
            if unit == 'm':
                return timedelta(minutes=digit_time).total_seconds()
            if unit == 'h':
                return timedelta(hours=digit_time).total_seconds()
            if unit == 'd':
                return timedelta(days=digit_time).total_seconds()
            else:
                return WrongTimeInterval(f'Time unit must be from : {_time_units}')

        except ValueError:
            raise WrongTimeInterval(f'Time unit must be from : {_time_units}')
    else:
        raise WrongTimeInterval(f'Time unit must be from : {_time_units}')


def perform_decoding(encoded_entity):
    try:
        return urlsafe_b64decode(encoded_entity).decode('UTF-8')
    except BASE64ERROR:
        return False    

def check_token(user, token):
    """
    Check that a password reset token is correct for a given user.
    """
    if not (user and token):
        return False
    # Parse the token
    try:
        ts_b36, _ = token.split("-")
    except ValueError:
        return False

    try:
        ts = base36_to_int(ts_b36)
    except ValueError:
        return False

    # Check that the timestamp/uid has not been tampered with
    if constant_time_compare(
            _make_token_with_timestamp(user, ts, secret),
            token,
        ):
        pass
    else:
        return False

    # Check the timestamp is within limit.
    if (_num_seconds(_now()) - ts) > PASSWORD_RESET_TIMEOUT:
        return False

    return True

    
def get_user_by_token(plain_email, encrypted_token):
    """
    returns either a bool or user itself which fits the token and is not active.
    Exceptions Raised
    -----------------
        - UserAlreadyActive
        - InvalidToken
        - UserNotFound
    """
    Session = oj.aci.get_sqlalchemy_session()
    User = oj.aci.get_user_model()
    with Session() as session:
        inactive_users = session.execute(sa.select(User).filter_by(email=plain_email)).all()[0]
    #inactive_users = session.query(User.email == plain_email).one()
    encrypted_token = encrypted_token.split(':')[0]
    for unique_user in inactive_users:
        valid = check_token(unique_user, encrypted_token)
        print ("valid = ", valid)
        if valid:
            if unique_user.is_active:
                raise UserAlreadyActive(f'The user with email: {plain_email} is already active')
            return unique_user
        else:
            raise InvalidToken('Token is invalid')
    else:
        raise UserNotFound(f'User with {plain_email} not found')


    
def decrypt_link(encoded_email, encoded_token):
    """
    main verification and decryption happens here.
    Exceptions Raised
    ------------------
        - signing.SignatureExpired
        - MaxRetriesExceeded
        - signing.BadSignature
        - UserAlreadyActive
        - InvalidToken
    """
    decoded_email = perform_decoding(encoded_email)
    decoded_token = perform_decoding(encoded_token)

    if decoded_email and decoded_token:
        if max_age:
            alive_time = __get_seconds(max_age)
            try:
                user_token = signing.TimestampSigner.unsign(decoded_token, alive_time)
                user = get_user_by_token(decoded_email, user_token)
                if user:
                    return user
                return False

            except signing.SignatureExpired:
                logger.warning(f'\n{"~" * 40}\n[WARNING] : The link is Expired!\n{"~" * 40}\n')
                user = get_user_by_token(decoded_email, __decrypt_expired_user(decoded_token))
                if not __verify_attempts(user):
                    raise MaxRetriesExceeded()
                raise

            except signing.BadSignature:
                logger.critical(
                    f'\n{"~" * 40}\n[CRITICAL] : X_x --> CAUTION : LINK SIGNATURE ALTERED! <-- x_X\n{"~" * 40}\n'
                )
                raise
        else:
            user = get_user_by_token(decoded_email, decoded_token)
            return user if user else False
    else:
        logger.error(f'\n{"~" * 40}\nError occurred in decoding the link!\n{"~" * 40}\n')
        return False
    

def verify_user(useremail, usertoken):
    user = decrypt_link(useremail, usertoken)
    if user:
        return True
    return False
