import ofjustpy as oj
from . import actions
import ofjustpy_react as ojr
from starlette.responses import PlainTextResponse
import justpy as jp

app = oj.aci.get_app()
from starlette.authentication import requires
ui_app_keymap = [ ("/new_user",
                   "/new_user",
                   None
                   ),
                  ("/verify_user_and_activate",
                   "/verify_user_and_activate",
                   None
                      )


                 ]
#xhr.open("GET", "/wp_logged_user_homepage", true, "san", "que");
#document.write(xhr.responseText);
def on_loginbtn_click(dbref, msg, form_inputs):
    print ("form_inputs = ", form_inputs)
    #msg.page.loop.create_task(
    #msg.page.loop.create_task(
    #document.getElementById("components").innerHTML = xhr.responseText;
    jp.run_task(msg.page.run_javascript("""
    console.log("run auth stuff");
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
    console.log("in ready state");
    console.log(this.readyState);
    console.log(this.status);
    console.log(xhr.responseText);
    if (xhr.readyState == 4 && xhr.status == 200) {
    window.location.replace("/verification/user/verify-email/homepage");

    }
    };
    var username = document.getElementById('/email').value;
    console.log("username");
    var password= document.getElementById('/password').value;
    console.log("password");
    console.log(username);
    console.log(password)
    xhr.open("GET", "/verification/user/verify-email/homepage", true);
    console.log("milestone 1");
    xhr.setRequestHeader("Authorization", "Basic "+btoa(username+':'+password));
    console.log("dso");
    xhr.withCredentials = true;
    console.log("dso2");
    console.log(xhr);
    xhr.send();
    """))
        #)
    #)

#redirect="Homepage",

#@app.requires(['authenticated'], status_code=404)
def wp_logged_user_homepage(request):
    try:
        print ("logged_user_homepage = ", request.user)
    except Exception as e:
        print ("can print request.user ", e)
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):
        placeholder_ = oj.Span_("placeholder", text="welcome authenticated user")
        wp_ = oj.WebPage_("oa",
                          cgens =[placeholder_],
                          template_file='svelte.html',
                          title="myoa"
                          )

        wp = wp_()
        wp.session_manager = session_manager
    return wp


# we don't want authentication for every request
#@requires(["authenticated"])
# async def starlette_endpoint_logged_user_homepage(request):
#     print (request.user)
#     return await app.response(wp_logged_user_homepage)(request)

#with_checkauth_wrapper = app.requires(['authenticated'], status_code=404)(starlette_endpoint)
#with_checkauth_wrapper = app.requires(['authenticated'], status_code=404)(starlette_endpoint)
#print ("with checkauth wrapper = ", with_checkauth_wrapper)
#print ("with checkauth wrapper = ", type(with_checkauth_wrapper))
# app.router.add_route("/homepage",
#                      starlette_endpoint_logged_user_homepage,
#                      name="logged-user-homepage")
#app.router.add_route("/homepage", starlette_endpoint)

def wp_user_login(request):
    """
    
    """
    session_manager = oj.get_session_manager(request.session_id)
    #@ojr.CfgLoopRunner
    def on_submit_click(dbref, msg, form_inputs_value_dict):
        print (form_inputs_value_dict)
        #The BasicAuthMiddleware should look up in the database
        #and verify the credentials. Redirect based on success and failure
        pass
    
    with oj.sessionctx(session_manager):
        def on_input_change(dbref, msg):
            # dummy event handler; otherwise react breaks
            pass
        email_ = oj.LabeledInput_("email",
                                  "Email",
                                  "me@mine.mydomain",
                                  data_validators = [oj.validator.InputRequired(),
                                            oj.validator.Email(), 
                                                     ]
                                  ).event_handle(oj.change, on_input_change)

        password_ = oj.LabeledInput_("password",
                                     "password",
                                     "Enter Password",
                                     input_type="password",
                                     data_validators=[oj.validator.InputRequired()]
                                     ).event_handle(oj.change, on_input_change)

        all_inputs_ = oj.StackV_("all_inputs",
                                 cgens = [email_,
                                          password_,
                                          ]
                                 )

        
        btn_ = oj.Button_("mybtn", text="Login", type="submit")        

        target_ = oj.Form_("myform", all_inputs_
                           ,btn_, stubStore = session_manager.stubStore
                           ).event_handle(oj.submit, on_loginbtn_click)

        wp_ = oj.WebPage_("loginpage",
                          cgens =[target_],
                          template_file='svelte.html',
                          use_websockets= False,
                          session_manager = session_manager,
                          title="Login to WikiSystem"
                          )

    # place some cookies; let signing cookie middleware do some work
    wp = wp_()
    request.state.messages.data = {'A Title': 'The message',
                                   'Another title': 'With another msg',
                                   }
    wp.session_manager = session_manager
    return wp


def wp_on_verification_failure(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):
        msgbox_ = oj.Span("msgbox",
                          text="We couldn't verify the token"
                          )
        reasonlist_ = oj.Ul_("reasonlist",
                             cgens = [oj.Li_("tokenexpired", text="Token may have expired"),
                                      oj.Li_("bug", text="could be due to bug in our system")
                             ]
                             )
        actionmsg_ = oj.Span_("actionmsg",
                             text= "consider regenerating the token or raise an issue at github"
                              )

        all_inputs_ = oj.StackV_("all_msgs",
                                 cgens = [msgbox_,
                                          reasonlist_,
                                          actionmsg_
                                          ]
                                 )
        
        wp_ = oj.WebPage_("UserAccountRegistrationFailure",
                          cgens =[target_],
                          WPtype= ojr.WebPage,
                          template_file='svelte.html',
                          use_websockets= False,
                          session_manager = session_manager,
                          title="Registration failed =: bad token"
                          )
        
    pass


def wp_on_verification_failure(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):
        msgbox_ = oj.Span("msgbox",
                          text="Something went wrong during email verification"
                       )
        reasonlist_ = oj.Ul_("reasonlist",
                             cgens = [
                                      oj.Li_("bug", text="Our system encountered a bug in our")
                             ]
                             )
        
        actionmsg_ = oj.Span_("actionmsg",
                              text= "consider regenerating the token or raise an issue at github"
                              )

        all_inputs_ = oj.StackV_("all_msgs",
                                 cgens = [msgbox_,
                                          reasonlist_,
                                          actionmsg_
                                          ]
                                 )
        
        wp_ = oj.WebPage_("UserAccountRegistrationFailure",
                          cgens =[target_],
                          WPtype= ojr.WebPage,
                          template_file='svelte.html',
                          use_websockets= False,
                          session_manager = session_manager,
                          title="Registration failed: either corrupt token or bug in the system"
                          )
        
    pass
     
def verify_user_and_activate(request, email, token):
    verify_status = actions.verify_user_and_activate(request, email, token)
    # chickened out; didn't use the complex ofjustpy-react machinary
    match verify_status:
        case "verified_success":
            #    user is verified; proceed to login page
            return wp_user_login(request)
        
        case "verified_failure":
            return wp_on_verification_failure(request)
        case "verified_exception":        
            #return wp_new_user_verified_exception(request)
            return wp_on_verification_failure(request)
# def verify_user_and_activate(request, useremail, usertoken):
#     try:
#         verified = verify_user(useremail, usertoken)
#         if verified is True:
#             if login_page and not success_template:
#                 messages.success(request, success_msg)
#                 return redirect(to=login_page)
#             return render(
#                 request,
#                 template_name=success_template,
#                 context={
#                     'msg': success_msg,
#                     'status': 'Verification Successful!',
#                     'link': reverse(login_page)
#                 }
#             )
#         else:
#             # we dont know what went wrong...
#             raise ValueError
#     except (ValueError, TypeError) as error:
#         logger.error(f'[ERROR]: Something went wrong while verifying user, exception: {error}')
#         return render(
#             request,
#             template_name=failed_template,
#             context={
#                 'msg': failed_msg,
#                 'minor_msg': 'There is something wrong with this link...',
#                 'status': 'Verification Failed!',
#             }
#         )
#     except SignatureExpired:
#         return render(
#             request,
#             template_name=link_expired_template,
#             context={
#                 'msg': 'The link has lived its life :( Request a new one!',
#                 'status': 'Expired!',
#                 'encoded_email': useremail,
#                 'encoded_token': usertoken
#             }
#         )
#     except BadSignature:
#         return render(
#             request,
#             template_name=failed_template,
#             context={
#                 'msg': 'This link was modified before verification.',
#                 'minor_msg': 'Cannot request another verification link with faulty link.',
#                 'status': 'Faulty Link Detected!',
#             }
#         )
#     except MaxRetriesExceeded:
#         return render(
#             request,
#             template_name=failed_template,
#             context={
#                 'msg': 'You have exceeded the maximum verification requests! Contact admin.',
#                 'status': 'Maxed out!',
#             }
#         )
#     except InvalidToken:
#         return render(
#             request,
#             template_name=failed_template,
#             context={
#                 'msg': 'This link is invalid or been used already, we cannot verify using this link.',
#                 'status': 'Invalid Link',
#             }
#         )
#     except UserNotFound:
#         raise Http404("404 User not found")



@oj.csrfprotect
def register_new_user(request):
    # RequestNewVerificationEmail
    # csrf_token, form, and a button
    session_manager = oj.get_session_manager(request.session_id)
    def on_input_change(dbref, msg):
        # we need dummy event handler for correct functioning of react
        pass

    User = oj.aci.get_user_model()
    @ojr.CfgLoopRunner
    def on_submit_click(dbref, msg, form_inputs_value_dict):
        print (form_inputs_value_dict)
        # the user model doesnot 1:1 map with the form
        # form has confirm password
        # but user model doesn't.
        # it seems tricky to build a model agnostic page 
        form_inputs_value_dict.pop("confirm_password")
        
        # add user in db and take actions
        val = User(**form_inputs_value_dict)
        val = User(**form_inputs_value_dict)
        print ("new user = ", str(val.id), val.email)
        #return "/new_user", User(**form_inputs_value_dict)
        return "/new_user", val
        
        #print (msg)

        #stop_validation = self._run_validation_chain(data, chain)
        # print(dbref.spathMap)
        # for cpath, cbref in dbref.spathMap.items():
        print ("form on_submit called")
        #     print (cpath, cbref)
        
        pass
    
    with oj.sessionctx(session_manager):
    # Technically, we should inspect the fields of the user; 
    # for now hardwiring to default user with email, first name, last, name, password
    
        email_ = oj.LabeledInput_("email",
                         "Email",
                         "me@mine.mydomain",
                         data_validators = [oj.validator.InputRequired(),
                                            oj.validator.Email(), 
                                            ]
                         ).event_handle(oj.change, on_input_change)




        # in Django-Verify-Email, first get the user_model, peek into meta, get the field,
        # and then get the verbose_name, along with help_text and then render out the form
        # things are bit manual here. You build your form by yourself

        first_name_ = oj.LabeledInput_("first_name",
                                        "First Name",
                                        "Mary",
                                        data_validators = [oj.validator.InputRequired(),
                                                           oj.validator.Length(max=128), # this should come from the user model only
                                                           ]).event_handle(oj.change,
                                                                           on_input_change

                                                                           )

        last_name_ = oj.LabeledInput_("last_name",
                                        "Last Name",
                                        "Fernandes",
                                        data_validators = [oj.validator.InputRequired(),
                                                           oj.validator.Length(max=128), # this should come from the user model only
                                                           ]).event_handle(oj.change,
                                                                                               on_input_change
                                                                                               )


        password_ = oj.LabeledInput_("password",
                                     "password",
                                     "Enter Password",
                                     input_type="password",
                                     data_validators=[oj.validator.InputRequired()]
                                     ).event_handle(oj.change, on_input_change)

        confirm_password_ = oj.LabeledInput_("confirm_password",
                                             "confirm_password",
                                             "Confirm Password",
                                             input_type="password",
                                             data_validators=[oj.validator.InputRequired(),
                                                              oj.validator.EqualTo(password_.spath)]
                                             ).event_handle(oj.change, on_input_change)

        all_inputs_ = oj.StackV_("all_inputs",
                                     cgens = [email_,
                                              first_name_,
                                              last_name_,
                                              password_,
                                              confirm_password_,
                                              ]
                                     )

        btn_ = oj.Button_("mybtn", text="Submit", type="submit")
        target_ = oj.Form_("myform", all_inputs_
                           , btn_, stubStore = session_manager.stubStore
                           ).event_handle(oj.submit, on_submit_click)


        wp_ = oj.WebPage_("register user",
                          cgens =[target_],
                          WPtype= ojr.WebPage,
                          template_file='svelte.html',
                          use_websockets= False,
                          ui_app_trmap_iter = ui_app_keymap,
                          action_module = actions,
                          session_manager = session_manager,
                          title="Register new user"
                          )
        
    wp = wp_()
    
    print ("wp.use_websockets = ", wp.use_websockets)
    # place some cookies; let signing cookie middleware do some work
    request.state.messages.data = {'A Title': 'The message',
                                   'Another title': 'With another msg',
                                   }
    wp.session_manager = session_manager
    return wp

