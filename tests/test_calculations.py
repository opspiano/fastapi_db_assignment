import uuid
import pytest
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal, engine, Base
from app.factory import CalculationFactory
from app.models import (
    User,
    Calculation,
    AddCalculation,
    SubtractCalculation,
    MultiplyCalculation,
    DivideCalculation,
)
from app.schemas import CalculationCreate, CalculationRead, CalculationType
from app.security import hash_password


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield


def test_factory_add():
    calc = CalculationFactory.create_calculation("Add", 10, 5)
    assert isinstance(calc, AddCalculation)
    assert calc.type == "Add"
    assert calc.result == 15.0


def test_factory_subtract():
    calc = CalculationFactory.create_calculation("Sub", 10, 4)
    assert isinstance(calc, SubtractCalculation)
    assert calc.type == "Sub"
    assert calc.result == 6.0


def test_factory_multiply():
    calc = CalculationFactory.create_calculation("Multiply", 3, 7)
    assert isinstance(calc, MultiplyCalculation)
    assert calc.type == "Multiply"
    assert calc.result == 21.0


def test_factory_divide():
    calc = CalculationFactory.create_calculation("Divide", 20, 4)
    assert isinstance(calc, DivideCalculation)
    assert calc.type == "Divide"
    assert calc.result == 5.0


def test_factory_divide_by_zero():
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        CalculationFactory.create_calculation("Divide", 10, 0)


def test_factory_invalid_type():
    with pytest.raises(ValueError, match="Unsupported calculation type"):
        CalculationFactory.create_calculation("Modulus", 10, 3)


def test_schema_calculation_create_valid():
    payload = CalculationCreate(a=12.5, b=2.5, type="Add")
    assert payload.a == 12.5
    assert payload.b == 2.5
    assert payload.type == CalculationType.ADD


def test_schema_calculation_create_zero_divisor():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=0, type="Divide")


def test_schema_calculation_create_invalid_type():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=5, type="Power")


def test_schema_calculation_create_invalid_operands():
    with pytest.raises(ValidationError):
        CalculationCreate(a="not_a_number", b=5, type="Add")


def test_schema_calculation_read_serialization():
    calc = CalculationFactory.create_calculation("Multiply", 4, 6)
    calc.id = 1
    schema_obj = CalculationRead.model_validate(calc)
    assert schema_obj.id == 1
    assert schema_obj.a == 4.0
    assert schema_obj.b == 6.0
    assert schema_obj.type == CalculationType.MULTIPLY
    assert schema_obj.result == 24.0


def test_db_insert_and_retrieve_calculation_with_user():
    db = SessionLocal()
    try:
        unique_suffix = uuid.uuid4().hex[:8]
        user = User(
            username=f"calcuser_{unique_suffix}",
            email=f"calcuser_{unique_suffix}@example.com",
            password_hash=hash_password("StrongPass123!"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        schema_in = CalculationCreate(a=15, b=3, type="Divide", user_id=user.id)
        calc = CalculationFactory.create_calculation(
            calc_type=schema_in.type.value,
            a=schema_in.a,
            b=schema_in.b,
            user_id=schema_in.user_id,
        )
        db.add(calc)
        db.commit()
        db.refresh(calc)

        retrieved = db.query(Calculation).filter(Calculation.id == calc.id).first()
        assert retrieved is not None
        assert isinstance(retrieved, DivideCalculation)
        assert retrieved.a == 15.0
        assert retrieved.b == 3.0
        assert retrieved.result == 5.0
        assert retrieved.user_id == user.id
        assert len(user.calculations) == 1
    finally:
        db.close()


def test_db_all_operations_persistence():
    db = SessionLocal()
    try:
        cases = [
            ("Add", 8, 2, 10.0),
            ("Sub", 8, 2, 6.0),
            ("Multiply", 8, 2, 16.0),
            ("Divide", 8, 2, 4.0),
        ]
        for op_type, a, b, expected in cases:
            calc = CalculationFactory.create_calculation(op_type, a, b)
            db.add(calc)
            db.commit()
            db.refresh(calc)
            assert calc.id is not None
            assert calc.result == expected
    finally:
        db.close()


def test_db_invalid_foreign_key():
    db = SessionLocal()
    try:
        invalid_calc = CalculationFactory.create_calculation(
            "Add", 1, 2, user_id=999999999
        )
        db.add(invalid_calc)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()
    finally:
        db.close()
