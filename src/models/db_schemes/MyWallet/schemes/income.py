from .base import SQLAlchemyBase
from sqlalchemy import Column, Integer, String, DateTime, func, Float, Index, Boolean, Date, text
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

    last_run_date = Column(Date, nullable= True)

    user = relationship("User", back_populates="incomes")
    category = relationship("IncomeCategory", back_populates="incomes")




    __table_args__ = (
        Index("idx_incomes_user_id", 'user_id'),
        Index("idx_incmoes_user_id_category_id", "user_id", "category_id"),
        Index("idx_incomes_created_at", 'created_at'),
        Index("idx_incomes_is_recurring", 'is_recurring'),
        Index(
            "indx_recurring_incomes",
            "next_due_date",
            "last_run_date",
            postgresql_where=text("is_recurring = TRUE")
        )
    )