import re
from typing import Dict, Optional
from src.libraries.model import Model
from src.models import models
from dataclasses import dataclass


class ValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


@dataclass
class ValidationResult:
    passed: Optional[dict]
    old: Optional[dict]
    errors: Optional[dict]


class InputField:
    def __init__(self, value: str, validation: str | list[str | tuple[str, int | str]]):
        self.value = value.strip()
        self.validations = validation

        if isinstance(self.validations, str):
            self.validations = self._process_validations(self.validations.split("|"))

        self.validations = tuple(self.validations)

    @staticmethod
    def _process_validations(validations: list) -> list:
        processed_validations = []

        for validation in validations:
            if ":" in validation:
                key, val = validation.split(":")
                # TODO: fix bug in _match method 'and key != "match"'
                val = int(val) if val.isdigit() and key != "match" else val
                processed_validations.append((key, val))
            else:
                processed_validations.append(validation)
        return processed_validations


class ValidatorMixin:
    def validate(self, input_fields: Dict[str, InputField]) -> ValidationResult:
        validated_data = {
            "passed": {},
            "old": {},
            "errors": {}
        }

        for field_name, field in input_fields.items():
            self.__validate_field(validated_data, field_name, field)

        return ValidationResult(
            passed=validated_data["passed"] if validated_data["passed"] else None,
            old=validated_data["old"] if validated_data["old"] else None,
            errors=validated_data["errors"] if validated_data["errors"] else None
        )

    def available_validations(self) -> tuple:
        validations = [
            method.lstrip("_") for method in dir(self)
            if re.match(r"_[a-z]+", method) and callable(getattr(self, method))
        ]
        return tuple(validations)

    def _required(self, field: str, value: str) -> str:
        if value == "":
            raise ValidationError(self.__format(field, "is required."))
        return value

    def _length(self, field: str, value: str, le: int) -> str:
        if value and len(value) != le:
            raise ValidationError(self.__format(field, f"must consist of {le} characters."))
        return value

    @staticmethod
    def _match(field: str, subject: str, match: str) -> str:
        if subject and subject != match:
            raise ValidationError(f"{field.capitalize().replace("_", " ")} do not match.")
        return subject

    def _unique(self, field: str, value: str, model_name: str) -> str:
        if hasattr(models, model_name):
            model: type(Model) = getattr(models, model_name)
        else:
            raise ValidationError(f"\"{model_name}\" model does not exist.")

        if value and model.find_by(condition=f"{field} = ?", parameters=[value,], limit=1):
            raise ValidationError(self.__format(field, "is taken."))
        return value

    def _numeric(self, field: str, value: str) -> str:
        if value and not value.isdigit():
            raise ValidationError(self.__format(field, "must consist of digits only."))
        return value

    def _min(self, field: str, value: str, __min: int):
        if value and len(value) < __min:
            raise ValidationError(self.__format(field, f"must consist of at least {__min} characters."))
        return value

    @staticmethod
    def __format(field: str, message: str) -> str:
        return f"{field.replace("_", " ").capitalize()} {message}"

    def __validate_field(self, validated_data: dict, field_name: str, field: InputField):
        for validation in field.validations:
            option = validation if isinstance(validation, str) else validation[0]

            if option not in self.available_validations():
                raise ValidationError(f"{self.__class__.__name__} does not have option: \"{validation}\"")

            try:
                self.__call_validation(validated_data, field_name, field, validation)
            except ValidationError as err:
                validated_data["errors"][field_name] = err
                validated_data["old"][field_name] = field.value

    def __call_validation(self, validated_data: dict, field_name: str, field: InputField, validation: str | tuple):
        if isinstance(validation, str):
            method = getattr(self, f"_{validation}")
            validated_data["passed"][field_name] = method(field_name, field.value)
        else:
            method = getattr(self, f"_{validation[0]}")
            validated_data["passed"][field_name] = method(field_name, field.value, validation[1])
