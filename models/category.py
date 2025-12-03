from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base


class Category(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    products = relationship("Product", back_populates="category")


