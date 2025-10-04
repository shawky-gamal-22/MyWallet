from .base import SQLAlchemyBase
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(SQLAlchemyBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    invoices = relationship("Invoice", back_populates="user")
    incomes = relationship("Income", back_populates="user")
