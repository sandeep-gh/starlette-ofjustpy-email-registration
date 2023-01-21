from token_manager import decrypt_link

def verify_user(useremail, usertoken):
    user = decrypt_link(useremail, usertoken)
            
