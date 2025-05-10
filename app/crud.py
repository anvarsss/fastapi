from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password, role="user")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_resource(db: Session, resource: schemas.ResourceCreate, owner_id: int):
    db_resource = models.Resource(**resource.dict(), owner_id=owner_id)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def get_resources(db: Session):
    return db.query(models.Resource).all()

def create_booking(db: Session, booking: schemas.BookingCreate, user_id: int):
    overlapping = db.query(models.Booking).filter(
        models.Booking.resource_id == booking.resource_id,
        models.Booking.end_time > booking.start_time,
        models.Booking.start_time < booking.end_time
    ).first()
    if overlapping:
        raise HTTPException(status_code=400, detail="Resource not available at this time.")
    db_booking = models.Booking(**booking.dict(), user_id=user_id)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_bookings(db: Session):
    return db.query(models.Booking).all()