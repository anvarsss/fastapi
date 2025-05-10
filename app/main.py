from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import database, models, schemas, crud, auth

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user.password = auth.get_password_hash(user.password)
    return crud.create_user(db, user)

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/resources/", response_model=schemas.ResourceOut)
def create_resource(resource: schemas.ResourceCreate, current_user=Depends(auth.get_current_user), db: Session = Depends(auth.get_db)):
    return crud.create_resource(db, resource, owner_id=current_user.id)

@app.get("/resources/", response_model=list[schemas.ResourceOut])
def list_resources(db: Session = Depends(auth.get_db)):
    return crud.get_resources(db)

@app.post("/bookings/", response_model=schemas.BookingOut)
def book(booking: schemas.BookingCreate, current_user=Depends(auth.get_current_user), db: Session = Depends(auth.get_db)):
    return crud.create_booking(db, booking, user_id=current_user.id)

@app.get("/bookings/", response_model=list[schemas.BookingOut])
def get_bookings(db: Session = Depends(auth.get_db)):
    return crud.get_bookings(db)