# from Django-Verify-Email/verify_email/urls.py
from .views import  (register_new_user,
                     verify_user_and_activate,
                     wp_user_login,
                     wp_logged_user_homepage)


routes = [('/user/verify-email/request-new-link',
           register_new_user,
           'request-new-link'),
          ('/user/verify-email/{email}/{token}',
           verify_user_and_activate,
           'verify-user-and-activate'),
          ('/user/verify-email/login',
           wp_user_login,
           "wp-user-login"
           ),
          ('/user/verify-email/homepage',
           wp_logged_user_homepage,
           "wp-logged-user-homepage"
           ),
          
          
          
          ]
