from .base import SQLAlchemyBase
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class IncomeCategory(SQLAlchemyBase):

    __tablename__ = "income_categories"

    id = Column(Integer, primary_key=True, index= True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    incomes = relationship("Income", back_populates="category")