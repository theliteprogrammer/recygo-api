from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, DECIMAL, Text
from sqlalchemy.orm import relationship

from authentication.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    surname = Column(String(255))
    phone = Column(String(255))
    name = Column(String(255))

    invoices = relationship("Invoice", back_populates="user")
    checkouts = relationship("Checkout", back_populates="user")
    carts = relationship("Cart", back_populates="user")


class Cart(Base):
    __tablename__ = "cart"

    itemID = Column(Integer, primary_key=True, index=True)
    price = Column(Integer)
    quantity = Column(Integer)
    total = Column(Integer)
    recycleType = Column(String(255))

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="carts")


class Checkout(Base):
    __tablename__ = "checkout"
    id = Column(Integer, primary_key=True, index=True)  # Primary key should be 'id'
    user_id = Column(Integer, ForeignKey("user.id"))  # Correctly match user_id
    recycle_type = Column(String(50))  # Correctly match recycle_type
    quantity = Column(Integer)  # Match quantity
    total = Column(Integer)  # Match total
    address = Column(String(255))  # Match address
    payment_type = Column(String(100))  # Correctly match payment_type

    user = relationship("User", back_populates="checkouts")


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))


class Invoice(Base):
    __tablename__ = "invoice"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    total_price = Column(DECIMAL(10, 2))  # Update column name to total_price
    payment_method = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="invoices")


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text)
    price = Column(Integer)  # Add the 'price' column to the model

