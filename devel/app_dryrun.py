"""
drop down color not working in firefox
"""

from tailwind_tags import *
import ofjustpy as oj
from addict import Dict
import justpy as jp
import traceback
from starlette.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response

#from starlette.routing import Mount
#from wtforms.validators	import DataRequired

app = jp.build_app()
#admin_app = jp.build_app()


def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    # this is necessary
    # a bug in justpy for input change
            
        
    with oj.sessionctx(session_manager):
        target_ = oj.Span_("dummyplaceholder", text="I am a dummmy")
        wp_ = oj.WebPage_("oa",
                          cgens =[target_],
                          template_file='svelte.html',
                          title="myoa"
                          )
        wp = wp_()
        wp.session_manager = session_manager
    return wp

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


def admin_page_debug(request):
    return JSONResponse({"x":1})

def admin_page_jp(request):
    wp = jp.WebPage(title="surma")
    jp.Span(a=wp, text="benice")
    return wp 
    




app.add_jproute("/", launcher, name="root")
app.add_jproute("/x", admin_page_jp, name="test")
app.mount_routes('/admin',
                 [ ('/test', admin_page_jp, 'test')
                     ]
                 )
# app.router.routes.append(Mount('/admin', routes=[
#     Route('/', admin_page_jp, name=admin_page)
#     ]

#     )
#     )
#app.mount_app("/admin", admin_app, name="admin")
#admin_app.router.add_route("/x", admin_page_debug, name="admin_page")
#admin_app.add_jproute("/x", admin_page_jp, name="admin_page")
#app.router.routes.append(Mount("/admin", app=admin_app, name="admin"))
#app.mount_app("/admin", admin_app, "admin")
#print(app.router.routes)
