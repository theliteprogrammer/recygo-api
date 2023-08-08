from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    password: str
    email: str
    surname: str
    phone: str
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm = True


class AdminBase(BaseModel):
    password: str
    email: str


class AdminCreate(AdminBase):
    pass


class Admin(AdminBase):
    class Config:
        orm = True


class CartBase(BaseModel):
    price: int
    quantity: int
    total: int
    itemID: int
    recycleType: str


class CartCreate(CartBase):
    pass


class Cart(CartBase):
    id: int
    user_id: int

    class Config:
        orm = True


class CheckoutBase(BaseModel):
    recycle_type: str
    quantity: int
    total: int
    address: str
    payment_type: str


class CheckoutCreate(CheckoutBase):
    pass


class Checkout(CheckoutBase):
    id: int
    user_id: int

    class Config:
        orm = True


class InvoiceBase(BaseModel):
    date: datetime
    total_price: float
    payment_method: str


class InvoiceCreate(InvoiceBase):
    pass


class Invoice(InvoiceBase):
    id: int
    user_id: int

    class Config:
        orm = True


# schemas.py

class ItemBase(BaseModel):
    name: str
    description: str
    price: int


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm = True
