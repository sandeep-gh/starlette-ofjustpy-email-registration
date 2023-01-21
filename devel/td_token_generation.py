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

from email_registration import  token_manager
from email_registration import  app_code_introspect as aci
from addict import Dict 
import sys
from sqlmodel import Field, SQLModel
from typing import Optional
import justpy as jp


engine = sa.create_engine("sqlite+pysqlite:///:memory:", echo=False)
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
    
#verification_link  = token_manager.generate_link(user, "x@y.com")
with Session() as session:
    all_users = [_ for _ in session.query(models.User)]
    print("all_users = ", all_users)

user = all_users[0]

encoded_email, token = token_manager.generate_relative_link(user, "x@y.com")
#print(verification_link)

print (type(encoded_email))
print (type(token))

print ("token = ", token)
aci.set_sqlalchemy_session(Session)

res = token_manager.get_user_by_token("x@y.com", token)
print (res)
