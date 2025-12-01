from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, DateTime, func
from db.database import Base

class Archived(Base):
    __tablename__ = "archived"

    product_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    stock: Mapped[int] = mapped_column(Integer)
    is_archived: Mapped[bool] = mapped_column(Boolean)
