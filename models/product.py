from sqlalchemy import String, Float, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from db.database import Base

class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    image_url: Mapped[str] = mapped_column(String, nullable=True)
    date_added: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

    # Category relationship
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.category_id"))
    category = relationship("Category", back_populates="products")


