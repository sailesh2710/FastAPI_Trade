from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

# SQLAlchemy Model for Database
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    order_type = Column(String(10), nullable=False)

# Pydantic Model for Request Validation
class OrderCreate(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: str

# Pydantic Model for API Response
class OrderResponse(OrderCreate):
    id: int