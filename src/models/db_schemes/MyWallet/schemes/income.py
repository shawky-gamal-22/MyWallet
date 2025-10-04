from .base import SQLAlchemyBase
from sqlalchemy import Column, Integer, String, DateTime, func, Float, Index, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


class Income(SQLAlchemyBase):

    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("income_categories.id"), nullable= False)
    source_name = Column(String, nullable=False) # e.g. Salary, Freelance Project
    amount = Column(Float, nullable=False)
    description = Column(String, nullable= True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


    # Fields for recurring income

    is_recurring = Column(Boolean, default=False)
    recurrence_interval = Column(String, nullable=True) # e.g. "monthly", "weekly"
    next_due_date = Column(Date, nullable=True)


    user = relationship("User", back_populates="incomes")
    category = relationship("IncomeCategory", back_populates="incomes")