from . import app_code_introspect as aci
from typing import List
from typing import Optional
import sqlalchemy as sa
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


USER = aci.get_user_model()
Base = aci.get_sqlalchemy_base()

class LinkCounter(Base):
    # TODO: cascade delete of user rows to this row
    requester_id = mapped_column(sa.Integer, sa.ForeignKey("user.id"))
    def __str__(self):
        return str(self.requester.get_username())

    def __repr__(self):
        return str(self.requester.get_username())


