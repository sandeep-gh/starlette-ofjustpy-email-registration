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

    
import models
import sqlalchemy  as sa
from email_registration.views import  register_new_user
from addict import Dict 
import sys
from sqlmodel import Field, SQLModel
from typing import Optional
import justpy as jp

# app = jp.build_app([Middleware(SerializedSignedCookieMiddleware,
#                                secret=b'a very, very secret thing',  
#                                state_attribute_name='messages',  
#                                cookie_name='my_cookie',
#                                cookie_ttl=60 * 5,  
#                                )
#                     ])


app = jp.build_app()

app.add_jproute("/", register_new_user)

engine = sa.create_engine("sqlite+pysqlite:///:memory:", echo=True)
models.Base.metadata.create_all(engine)
# from starlette.testclient import TestClient
# client = TestClient(app)
# response = client.get('/')

from addict import Dict
request = Dict()
request.session_id = "abc"
wp = register_new_user(request)
_sm = wp.session_manager
_ss = _sm.stubStore
#print(_ss.labeldinput_input)
_ss.freeze()
print(_ss.keys())
_ss.email.target.value = "spoofemail@monallabs.in"
_ss.first_name.target.value = "sxsdsdfs"
_ss.last_name.target.value = "mypass1"
_ss.password.target.value = "mypass1"
_ss.confirm_password.target.value = "mypass1"
#print(_ss.keys())
msg = Dict()
msg.page = wp
_ss.myform.target.on_submit(msg)



