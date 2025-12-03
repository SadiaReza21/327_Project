from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from db.database import Base

class Inventory(Base):
    __tablename__ = "inventories"

    product_id: Mapped[int] = mapped_column(primary_key=True)  
    name: Mapped[str] = mapped_column(String)
    stock: Mapped[int] = mapped_column(Integer)
    is_available: Mapped[bool] = mapped_column(Boolean)
