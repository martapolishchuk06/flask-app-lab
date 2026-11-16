from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Float, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category", lazy="select")


class Product(db.Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    category_id: Mapped[int | None] = mapped_column(db.ForeignKey('categories.id'))
    category: Mapped["Category | None"] = relationship("Category", back_populates="products")
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1", nullable=False)

    def __repr__(self) -> str:
        return f"<Product {self.name} ${self.price}>"