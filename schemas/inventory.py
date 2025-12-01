from pydantic import BaseModel

class InventoryBase(BaseModel):
    low_stock_threshold: int = 5

class InventoryCreate(InventoryBase):
    pass

class InventoryResponse(InventoryBase):
    inventory_id: int

    class Config:
        orm_mode = True
