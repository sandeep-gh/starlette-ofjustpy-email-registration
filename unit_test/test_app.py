"""
an app to
1) testdrive the email_registration
2) pilot run the register-verify-email-cycle.

Things to be mindful:
- local https
- Signing middleware for cookies
- CSRF middleware
- form input validation (can we use pydantic)
- mounting admin routes (because mount is failing)

Steps:
-  add signing middleware : 
"""

# ======================= first set the logging ======================
import logging
import os

if os:
    try:
        os.remove("launcher.log")
    except:
        pass

import sys
if sys:
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename="launcher.log",
                        level=logging.DEBUG, format=FORMAT)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    

# ================================ end ===============================

from tailwind_tags import *
import ofjustpy as oj
from addict import Dict
import justpy as jp
import traceback
from starlette.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
from csrf_middleware import CSRFMiddleware
from starlette.middleware import Middleware
from asgi_signing_middleware import SerializedSignedCookieMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser, requires
)
import binascii
import base64

#from starlette.routing import Mount
#from wtforms.validators	import DataRequired



SECRET_KEY="Pls use a good professional secret key"
csrf_cookie_name = "csrftoken"
csrf_secret='shhshh2'

class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        logger.debug("Auth Middleware:BEGIN")

        if "Authorization" not in conn.headers:
            logger.debug("No authorization header in conn.headers")
            logger.debug("Auth Middleware:END")
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            
            logger.debug("recieved authentication credentials..eventually verify it")
            logger.debug(f"scheme={scheme} credentials={credentials}")
            if scheme.lower() != 'basic':
                logger.debug("auth scheme not basic: no authorization begin done")
                return
            decoded = base64.b64decode(credentials).decode("ascii")
            logger.debug(f"decoded = {decoded}")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            logger.debug("authentication ran into exception")
            raise AuthenticationError('Invalid basic auth credentials')
        logger.debug("authentication done: user is verified")
        return AuthCredentials(["authenticated"]), SimpleUser("user")


auth_middleware =     Middleware(AuthenticationMiddleware,
               backend=BasicAuthBackend(),
               on_error=lambda _, exc: PlainTextResponse("error during authentication", status_code=401)
               

               )
    
csrf_middleware = Middleware(CSRFMiddleware,
                                secret=csrf_secret,
                                field_name = csrf_cookie_name)
signed_cookie_middleware = Middleware(SerializedSignedCookieMiddleware,
                               secret=b'a very, very secret thing',  
                               state_attribute_name='messages',  
                               cookie_name='my_cookie',
                               cookie_ttl=60 * 5,  
                               )

app = jp.build_app([auth_middleware, 
                    signed_cookie_middleware,
                    csrf_middleware
                    ])
oj.aci.set_app(app)
# email_registration needs to be import after app has been initialized
# and has be setup


from email_registration.views import register_new_user
import email_registration


# ====================== instantiate a database ======================
import sqlalchemy  as sa
#engine = sa.create_engine("sqlite+pysqlite:///:memory:", echo=False)
engine = sa.create_engine("sqlite+pysqlite:///testdb.db", echo=False)
# create users and other register-via_email-verify tables (link counter)
import models
models.Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(engine)

with Session() as session:
    user = models.User(email="x@y.com",
                       first_name="y",
                       last_name="z",
                       is_active = False,
                       password="gg".encode('utf-8'))
    session.add(user)
    session.commit()
    
oj.aci.set_sqlalchemy_session(Session)


# ================================ end ===============================

#app.add_jproute("/", register_new_user)



# def launcher(request):
#     session_manager = oj.get_session_manager(request.session_id)
#     # this is necessary
#     # a bug in justpy for input change
            
    
#     with oj.sessionctx(session_manager):
#         def on_input_change(dbref, msg):
#             #traceback.print_stack(file=sys.stdout)
#             print (msg)
#             pass
        
#         def on_submit_click(dbref, msg, form_inputs_value_dict):
#             #print (msg)

#                         #stop_validation = self._run_validation_chain(data, chain)
#             # print(dbref.spathMap)
#             # for cpath, cbref in dbref.spathMap.items():
#             print ("form on_submit called")
#             #     print (cpath, cbref)
#             pass
    
#         target_ = oj.Span_("dummyplaceholder",
#                            text="I am a dummmy")
#         btn_ = oj.Button_("mybtn", text="Submit", type="submit")
#         username_input_ = oj.LabeledInput_("username",
#                                            "Username",
#                                            "username",
                                           
#                                            data_validators = [oj.validator.InputRequired(),
#                                                               oj.validator.Length(min=5, max=8)
#                                                               ]).event_handle(oj.change,
#                                                                                        on_input_change
#                                                                                        )

#         email_input_ = oj.LabeledInput_("email",
#                                            "Email",
#                                            "Email",
                                           
#                                            data_validators = [oj.validator.Email()]).event_handle(oj.change,
#                                                                                        on_input_change
#                                                                                        )

#         password_ = oj.LabeledInput_("password",
#                                      "password",
#                                      "Enter Password",
#                                      input_type="password",
#                                      data_validators=[oj.validator.InputRequired()]
#                                      ).event_handle(oj.change, on_input_change)
        
#         confirm_password_ = oj.LabeledInput_("confirm_password",
#                                      "confirm_password",
#                                      "Confirm Password",
#                                              input_type="password",
#                                      data_validators=[oj.validator.InputRequired(),
#                                                       oj.validator.EqualTo(password_.spath)]
#                                      ).event_handle(oj.change, on_input_change)
        
        
#         all_inputs_ = oj.StackV_("all_inputs",
#                                  cgens = [username_input_,
#                                           email_input_,
#                                           password_,
#                                           confirm_password_]
#                                  )
#         target_ = oj.Form_("myform", all_inputs_
#                            ,btn_, stubStore = session_manager.stubStore
#                 ).event_handle(oj.submit, on_submit_click)
        
#         btn_ = oj.Button_("mybtn", text="Submit", type="submit")
        
#         wp_ = oj.WebPage_("oa",
#                           cgens =[target_],
#                           template_file='svelte.html',
#                           title="myoa",
#                           use_websockets = False
                          
#                           )
#         wp = wp_()
#         wp.session_manager = session_manager
#         request.state.messages.data = {'A Title': 'The message',
#                                        'Another title': 'With another msg',
#                                        csrf_cookie_name: csrf_secret
#                                        }
#         wp.cookies[csrf_cookie_name] = 'shhshh2'
#     return wp




# app.add_jproute("/", launcher, name="root")



# ======================= only for demo purpose ======================
# ===================== mounting routes for admin ====================
def admin_page(request):
    session_manager = oj.get_session_manager(request.session_id)
    # this is necessary
    # a bug in justpy for input change
    with oj.sessionctx(session_manager):
        target_ = oj.Span_("dummyplaceholder", text="this is dummy")
        wp_ = oj.WebPage_("oa",
                          cgens =[target_],
                          template_file='svelte.html',
                          title="myoa"
                          )
        wp = wp_()
        wp.session_manager = session_manager
    return wp


#@app.requires(['authenticated'], status_code=404)
def wp_dummy_starlette_endpoint(request):
    return PlainTextResponse("Hello")





app.mount_routes('/verification', email_registration.routes
                 )

#app.router.add_route("/homepage", wp_dum)

app.mount_routes('/admin',
                 [ ('/test', admin_page, 'test')
                     ]
                 )


# ================================ end ===============================

# ========================== test drive register new user form input =========================
# from addict import Dict
# request = Dict()
# request.session_id = "abc"
# wp = register_new_user(request)
# _sm = wp.session_manager
# _ss = _sm.stubStore
# _ss.email.target.value = "spoofemail@monallabs.in"
# _ss.first_name.target.value = "sxsdsdfs"
# _ss.last_name.target.value = "mypass1"
# _ss.password.target.value = "mypass1"
# _ss.confirm_password.target.value = "mypass1"
# msg = Dict()
# msg.page = wp
# _ss.myform.target.on_submit(msg)

# ================================ end ===============================

# from starlette.testclient import TestClient
# client = TestClient(app)
# response = client.get('/verification/user/verify-email/eEB5LmNvbQ==/bf01ci-5014c0202644db792be0551053e93f21')

