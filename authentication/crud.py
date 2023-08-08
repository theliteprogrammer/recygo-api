from sqlalchemy.orm import Session
from authentication import models
from authentication import schemas
from authentication import hashing
from authentication.hashing import bcrypt_context, get_hashed
from authentication.models import User
from authentication.models import Item
from authentication.schemas import ItemCreate, ItemUpdate


def get_user(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# Function to verify a password
def verify_password(plain_password: str, hashed_password: str):
    return bcrypt_context.verify(plain_password, hashed_password)


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def delete_user(db: Session, id: int):
    db_user = db.query(User).filter(User.id == id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        deleted_db_user = db.query(User).filter(User.id == id).first()
        if deleted_db_user is None:
            return True
    return False


# creates a new user by taking a database session and user schema
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(password=hashing.get_hashed(user.password),
                          email=user.email,
                          surname=user.surname,
                          phone=user.phone,
                          name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# CRUD for Cart

def get_cart(db: Session, cart_id: int):
    return db.query(models.Cart).filter(models.Cart.itemID == cart_id).first()


def get_carts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cart).offset(skip).limit(limit).all()


def create_cart(db: Session, cart: schemas.CartCreate, user_id: int):
    db_cart = models.Cart(
        price=cart.price,
        quantity=cart.quantity,
        total=cart.total,
        recycleType=cart.recycleType,
        user_id=user_id  # Set the user_id when creating the cart item
    )
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


def delete_cart(db: Session, cart_id: int):
    db_cart = db.query(models.Cart).filter(models.Cart.itemID == cart_id).first()
    if db_cart:
        db.delete(db_cart)
        db.commit()
        return True
    else:
        return False


# CRUD for Invoice

def get_invoice(db: Session, invoice_id: int):
    return db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()


def get_invoices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Invoice).offset(skip).limit(limit).all()


def create_invoice(db: Session, invoice: schemas.InvoiceCreate):
    db_invoice = models.Invoice(
        date=invoice.date,
        totalPrice=invoice.totalPrice,
        paymentMethod=invoice.paymentMethod,
        user_id=invoice.user_id
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def delete_invoice(db: Session, invoice_id: int):
    db_invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if db_invoice:
        db.delete(db_invoice)
        db.commit()
        return True
    else:
        return False


# CRUD for Admin

def get_admin(db: Session, email: str):
    return db.query(models.Admin).filter(models.Admin.email == email).first()


def create_admin(db: Session, email: str, password: str):
    db_admin = models.Admin(
        email=email,
        password=hashing.get_hashed(password)
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


# CRUD for Checkout

def get_checkout(db: Session, checkout_id: str):
    return db.query(models.Checkout).filter(models.Checkout.recycleTypeID == checkout_id).first()


def get_checkouts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Checkout).offset(skip).limit(limit).all()


def create_checkout(db: Session, checkout: schemas.CheckoutCreate):
    db_checkout = models.Checkout(
        recycleTypeID=checkout.recycleTypeID,
        quantity=checkout.quantity,
        total=checkout.total,
        address=checkout.address,
        paymentMethod=checkout.paymentMethod
    )
    db.add(db_checkout)
    db.commit()
    db.refresh(db_checkout)
    return db_checkout


def delete_checkout(db: Session, checkout_id: str):
    db_checkout = db.query(models.Checkout).filter(models.Checkout.recycleTypeID == checkout_id).first()
    if db_checkout:
        db.delete(db_checkout)
        db.commit()
        return True
    else:
        return False


# crud.py



def create_item(db: Session, item: ItemCreate):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def update_item(db: Session, item_id: int, item_update: ItemUpdate):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        for key, value in item_update.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item
    return None
