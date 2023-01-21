from typing import Optional
from sqlalchemy_utils import EmailType, PasswordType
from sqlalchemy import create_engine
import sqlalchemy as sa
#engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship



class Base(DeclarativeBase):
    pass

# print (Base.metadata)
# print (Base.registry)


class User(Base):
    __tablename__ = "user_account"
    # primary key is autoincrement
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[EmailType] = mapped_column(EmailType, nullable=False, unique=True)
    first_name : Mapped[sa.String]=  mapped_column(sa.String(120))
    last_name: Mapped[sa.String] = mapped_column(sa.String(120))
    #password: Mapped[PasswordType] = mapped_column(PasswordType)
    password: Mapped[sa.LargeBinary] = mapped_column(sa.LargeBinary)
    is_active: Mapped[sa.Boolean] = mapped_column(sa.Boolean)


