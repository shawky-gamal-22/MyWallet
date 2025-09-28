from .base import SQLAlchemyBase
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


class Invoice(SQLAlchemyBase):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    total_price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now(), nullable=False)
    img_path = Column(String, nullable=True)

    user = relationship("User", back_populates="invoices")
    category = relationship("Category", back_populates="invoices")