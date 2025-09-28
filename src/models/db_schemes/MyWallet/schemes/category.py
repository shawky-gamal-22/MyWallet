from .base import SQLAlchemyBase
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Category(SQLAlchemyBase):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    invoices = relationship("Invoice", back_populates="category")