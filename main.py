from datetime import datetime, timedelta

import jwt
import secrets
from fastapi import Depends, FastAPI, HTTPException, Security, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.testing import db

from authentication import schemas, models, crud
from authentication.crud import verify_password
from authentication.database import SessionLocal, engine
from authentication.hashing import get_hashed

# Generates a strong random secret key of 32 bytes (256 bits)
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

# create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        # Decode the JWT token to get the user ID
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except jwt:
        raise HTTPException(status_code=401, detail="Invalid token")
    return crud.get_user(db, id=user_id)


@app.get("/")
async def root():
    return {"message": "Welcome to Boolean Autocrats API",
            "Developers": "Arlene Osler, Tumelo Tsamai, Amos Thando Mpofu"}


@app.post("/create_user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # try retrieving this user by email and if we get back a user then the user already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=404, detail="Email already registered")
    return crud.create_user(db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.__dict__


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.delete("/users/deleteUser/{user_ID}", response_model=schemas.User)
def remove_user(user_ID: int, db: Session = Depends(get_db)):
    is_deleted = crud.delete_user(db, id=user_ID)
    if is_deleted:
        return {"message": "Successfully deleted user"}
    else:
        raise HTTPException(status_code=400, detail="User could not be deleted")


# Login route
@app.post("/login")
def login(email: str = Query(...), password: str = Query(...), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=402, detail="Email not registered")
    if not verify_password(plain_password=password, hashed_password=user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {"name": user.name, "surname":user.surname}


@app.post("/create_cart", response_model=schemas.Cart)
def create_cart(cart: schemas.CartCreate, db: Session = Depends(get_db),
                current_user: schemas.User = Depends(get_current_user)):
    try:
        return crud.create_cart(db=db, cart=cart, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/carts/{cart_id}", response_model=schemas.Cart)
def read_cart(cart_id: int, db: Session = Depends(get_db)):
    db_cart = crud.get_cart(db=db, cart_id=cart_id)
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db_cart


@app.get("/carts/", response_model=list[schemas.Cart])
def read_carts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_carts(db=db, skip=skip, limit=limit)


@app.delete("/carts/{cart_id}", response_model=schemas.Cart)
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_cart(db=db, cart_id=cart_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# CRUD for Invoices
@app.post("/invoices/", response_model=schemas.Invoice)
def create_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_invoice(db=db, invoice=invoice)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/invoices/{invoice_id}", response_model=schemas.Invoice)
def read_invoice(invoice_id: int, db: Session = Depends(get_db)):
    db_invoice = crud.get_invoice(db=db, invoice_id=invoice_id)
    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return db_invoice


@app.get("/invoices/", response_model=list[schemas.Invoice])
def read_invoices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_invoices(db=db, skip=skip, limit=limit)


@app.delete("/invoices/{invoice_id}", response_model=schemas.Invoice)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_invoice(db=db, invoice_id=invoice_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# CRUD for Checkout
@app.post("/checkout/", response_model=schemas.Checkout)
def create_checkout(checkout: schemas.CheckoutCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_checkout(db=db, checkout=checkout)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/checkout/{checkout_id}", response_model=schemas.Checkout)
def read_checkout(checkout_id: int, db: Session = Depends(get_db)):
    db_checkout = crud.get_checkout(db=db, checkout_id=checkout_id)
    if not db_checkout:
        raise HTTPException(status_code=404, detail="Checkout not found")
    return db_checkout


@app.get("/checkout/", response_model=list[schemas.Checkout])
def read_checkouts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_checkouts(db=db, skip=skip, limit=limit)


@app.delete("/checkout/{checkout_id}", response_model=schemas.Checkout)
def delete_checkout(checkout_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_checkout(db=db, checkout_id=checkout_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# CRUD for Admin

@app.post("/admin/", response_model=schemas.Admin)
def create_admin(email: str, password: str, db: Session = Depends(get_db)):
    try:
        return crud.create_admin(db=db, email=email, password=password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Create an item
@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

# Get a single item by ID
@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Get all items
@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db, skip=skip, limit=limit)

# Update an item
@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item_update: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db, item_id, item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Delete an item
@app.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

