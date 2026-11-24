from typing import Optional, Dict, Type
from app.models import (
    Calculation,
    AddCalculation,
    SubtractCalculation,
    MultiplyCalculation,
    DivideCalculation,
)


class CalculationFactory:
    _operations: Dict[str, Type[Calculation]] = {
        "Add": AddCalculation,
        "Sub": SubtractCalculation,
        "Multiply": MultiplyCalculation,
        "Divide": DivideCalculation,
    }

    @classmethod
    def create_calculation(
        cls,
        calc_type: str,
        a: float,
        b: float,
        user_id: Optional[int] = None,
    ) -> Calculation:
        normalized_type = "Sub" if calc_type == "Subtract" else calc_type
        operation_cls = cls._operations.get(normalized_type)
        if operation_cls is None:
            raise ValueError(
                f"Unsupported calculation type: '{calc_type}'. "
                f"Expected one of {list(cls._operations.keys())}."
            )

        instance = operation_cls(
            a=float(a),
            b=float(b),
            type=normalized_type,
            user_id=user_id,
        )
        instance.result = instance.compute()
        return instance
