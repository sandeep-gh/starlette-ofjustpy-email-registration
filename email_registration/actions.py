# do actions
from . import  token_manager
def send_verification_link(appstate, arg_user):
    """appctx:/new_user

    arg: new user instance. 
    """
    print ("called send_verification_link")
    print (appstate)
    print (arg_user)
    print (arg_user.email)
    relative_link = token_manager.generate_relative_link(arg_user, arg_user.email)
    print (relative_link)

    
def verify_user_and_activate(request, email, token):
    """appctx:/verify_user_and_activate

    arg: new user instance. 
    """
    print ("called verify_user_and_activate", email, token)
    #verified = token_manager.verify_user(email, token)
    decoded_email = token_manager.perform_decoding(email)
    #print ("verified = ", res)
    try:
        #verified = token_manager.verify_user(email, token)
        # res = token_manager.get_user_by_token("x@y.com", token)
        # print ("verified = ", verified)
        #TODO: we should be calling decrypt link; but for now using this shortcut
        #for simplicity
        verified_user = token_manager.get_user_by_token(decoded_email, token)
    
        if verified_user:
            return "verified_success"
           
        else:
            return "verified_failure"
           
    except Exception as e:
        return "verified_exception"


