from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    calculations = relationship(
        "Calculation",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    type = Column(String, nullable=False, index=True)
    result = Column(Float, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="calculations")

    __mapper_args__ = {
        "polymorphic_identity": "calculation",
        "polymorphic_on": type,
    }

    def compute(self) -> float:
        raise NotImplementedError("Subclasses must implement compute()")


class AddCalculation(Calculation):
    __mapper_args__ = {
        "polymorphic_identity": "Add",
    }

    def compute(self) -> float:
        return float(self.a + self.b)


class SubtractCalculation(Calculation):
    __mapper_args__ = {
        "polymorphic_identity": "Sub",
    }

    def compute(self) -> float:
        return float(self.a - self.b)


class MultiplyCalculation(Calculation):
    __mapper_args__ = {
        "polymorphic_identity": "Multiply",
    }

    def compute(self) -> float:
        return float(self.a * self.b)


class DivideCalculation(Calculation):
    __mapper_args__ = {
        "polymorphic_identity": "Divide",
    }

    def compute(self) -> float:
        if self.b == 0:
            raise ValueError("Division by zero is not allowed")
        return float(self.a / self.b)
