from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, model_validator


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    username: str
    password: str


class CalculationType(str, Enum):
    ADD = "Add"
    SUB = "Sub"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"


class CalculationBase(BaseModel):
    a: float
    b: float
    type: CalculationType


class CalculationCreate(CalculationBase):
    user_id: Optional[int] = None

    @model_validator(mode="after")
    def check_divide_by_zero(self):
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("Division by zero is not allowed")
        return self


class CalculationUpdate(BaseModel):
    a: Optional[float] = None
    b: Optional[float] = None
    type: Optional[CalculationType] = None


class CalculationRead(CalculationBase):
    id: int
    result: float
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
