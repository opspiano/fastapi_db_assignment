from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app.factory import CalculationFactory
from app.models import User, Calculation
from app.schemas import (
    UserCreate,
    UserRead,
    UserLogin,
    CalculationCreate,
    CalculationUpdate,
    CalculationRead,
)
from app.security import hash_password, verify_password

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "running"}


@app.post("/users/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/users/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return {
        "message": "Login successful",
        "user_id": db_user.id,
        "username": db_user.username,
    }


@app.post("/users/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)


@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return db_user


@app.get("/calculations", response_model=List[CalculationRead])
def browse_calculations(db: Session = Depends(get_db)):
    return db.query(Calculation).all()


@app.get("/calculations/{calc_id}", response_model=CalculationRead)
def read_calculation(calc_id: int, db: Session = Depends(get_db)):
    db_calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not db_calc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )
    return db_calc


@app.post("/calculations", response_model=CalculationRead, status_code=status.HTTP_201_CREATED)
def add_calculation(calc: CalculationCreate, db: Session = Depends(get_db)):
    if calc.user_id is not None:
        user = db.query(User).filter(User.id == calc.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

    try:
        db_calc = CalculationFactory.create_calculation(
            calc_type=calc.type.value,
            a=calc.a,
            b=calc.b,
            user_id=calc.user_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc


@app.put("/calculations/{calc_id}", response_model=CalculationRead)
def edit_calculation(calc_id: int, calc_update: CalculationUpdate, db: Session = Depends(get_db)):
    db_calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not db_calc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    new_a = calc_update.a if calc_update.a is not None else db_calc.a
    new_b = calc_update.b if calc_update.b is not None else db_calc.b
    new_type = calc_update.type.value if calc_update.type is not None else db_calc.type

    try:
        temp_calc = CalculationFactory.create_calculation(new_type, new_a, new_b)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    db.query(Calculation).filter(Calculation.id == calc_id).update({
        "a": new_a,
        "b": new_b,
        "type": new_type,
        "result": temp_calc.result,
    })
    db.commit()
    db.expire_all()
    return db.query(Calculation).filter(Calculation.id == calc_id).first()


@app.delete("/calculations/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(calc_id: int, db: Session = Depends(get_db)):
    db_calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not db_calc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )
    db.delete(db_calc)
    db.commit()
    return None
