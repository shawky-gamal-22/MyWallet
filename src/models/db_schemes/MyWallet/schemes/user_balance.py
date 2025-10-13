from .base import SQLAlchemyBase
from sqlalchemy import Column, Integer, String, DateTime, func, Float, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


class UserBalance(SQLAlchemyBase):

    __tablename__ = "user_balance"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    current_balance = Column(Float, nullable=False, default=0)



    user = relationship("User", back_populates= "balance")
