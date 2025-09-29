from .base import SQLAlchemyBase
from sqlalchemy import Column, Integer, String, DateTime, func, Float, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


class Invoice(SQLAlchemyBase):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    total_price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now(), nullable=False)
    img_path = Column(String, nullable=True)

    user = relationship("User", back_populates="invoices")
    category = relationship("Category", back_populates="invoices")



    __table_args__ = (
        Index('idx_user_created_at', 'user_id', 'created_at'),
        Index('idx_category_created_at', 'category_id', 'created_at'),
        Index('idx_user_id', 'user_id'),
        Index('idx_created_at', 'created_at'),
    )