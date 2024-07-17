import re
from typing import Dict, Optional
from src.libraries.model import Model
from src.models import models
from dataclasses import dataclass


class ValidationError(Exception):
    """Validation error :class:`Exception`."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InputField:
    """Stores information about the input."""
    def __init__(self, value: str, validation: str | list[str | tuple[str, int | str]]):
        """
        Available validations tuple :class:`ValidatorMixin`.available_validations()
        :param value: Input's value.
        :param validation: Validations to apply - "validation|validation2:3|..." or [validation, (validation1, 3), ...]
        """
        self.value = value.strip()
        self.validations = validation

        if isinstance(self.validations, str):
            self.validations = self.__process_validations(self.validations.split("|"))

        self.validations = tuple(self.validations)

    @staticmethod
    def __process_validations(validations: list) -> list:
        """Prepares validations to be applied."""
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


@dataclass
class ValidationResult:
    """
    Return class for :class:`ValidatorMixin`.validate() method.
    :var passed: :class:`InputField` values that passed validation.
    :var old: :class:`InputField` values that haven't passed validation.
    :var errors: Errors generated for each failed :class:`InputField` value.
    """
    passed: Optional[dict]
    old: Optional[dict]
    errors: Optional[dict]


class ValidatorMixin:
    """Class for validating inputs."""
    def validate(self, input_fields: Dict[str, InputField]) -> ValidationResult:
        """
        Validates :class:`InputField` values.
        :param input_fields: {"input_field_name": :class:`InputField`, ...}.
        :return: :class:`ValidationResult`.
        """
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
        """
        :return: Tuple of available validations.
        """
        validations = [
            method.lstrip("_") for method in dir(self)
            if re.match(r"_[a-z]+", method) and callable(getattr(self, method))
        ]
        return tuple(validations)

    def _required(self, field: str, value: str) -> str:
        """
        Checks if `value` is not empty.
        :param field: Field name.
        :param value: Field value.
        :return: `value` if passed.
        """
        if value == "":
            raise ValidationError(self.__format(field, "is required."))
        return value

    def _length(self, field: str, value: str, le: int) -> str:
        """
        Checks if `value` length matches.
        :param field: Field name.
        :param value: Field value.
        :param le: Length to match.
        :return: `value` if passed.
        """
        if value and len(value) != le:
            raise ValidationError(self.__format(field, f"must consist of {le} characters."))
        return value

    @staticmethod
    def _match(field: str, subject: str, match: str) -> str:
        """
        Checks if `subject` matches `match`.
        :param field: Field name.
        :param subject: Subject value.
        :param match: Match value.
        :return: `subject` if passed.
        """
        if subject and subject != match:
            raise ValidationError(f"{field.capitalize().replace("_", " ")} do not match.")
        return subject

    def _unique(self, column: str, value: str, model_name: str) -> str:
        """
        Checks if `value` is unique in database table.
        :param column: Table's column name.
        :param value: Field value.
        :param model_name: Model(:class:`Model`) name.
        :return: `value` if passed.
        """
        if hasattr(models, model_name):
            model: type(Model) = getattr(models, model_name)
        else:
            raise ValidationError(f"\"{model_name}\" model does not exist.")

        if value and model.find_by(condition=f"{column} = ?", parameters=[value, ], limit=1):
            raise ValidationError(self.__format(column, "is taken."))
        return value

    def _numeric(self, field: str, value: str) -> str:
        """
        Checks if `value` contains only digits.
        :param field: Field name.
        :param value: Field value.
        :return: `value` if passed.
        """
        if value and not value.isdigit():
            raise ValidationError(self.__format(field, "must consist of digits only."))
        return value

    def _min(self, field: str, value: str, __min: int):
        """
        Checks if `value` is at least `__min` length.
        :param field: Field name.
        :param value: Field value
        :param __min: Length to match.
        :return: `value` if passed.
        """
        if value and len(value) < __min:
            raise ValidationError(self.__format(field, f"must consist of at least {__min} characters."))
        return value

    @staticmethod
    def __format(field: str, message: str) -> str:
        """
        Formats error message.
        :param field: Field name.
        :param message: Error message.
        :return: Formated error message.
        """
        return f"{field.replace("_", " ").capitalize()} {message}"

    def __validate_field(self, validated_data: dict, field_name: str, field: InputField):
        """
        Validates :class:`InputField`.
        :param validated_data: Dictionary for storing validated data.
        :param field_name: Field name.
        :param field: :class:`InputField` object.
        """
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
        """
        Apply validation to :class:`InputField`.value.
        :param validated_data: Dictionary for storing validated data.
        :param field_name: Field name.
        :param field: :class:`InputField` object.
        :param validation: Item from :class:`InputField`.validations.
        """
        if isinstance(validation, str):
            method = getattr(self, f"_{validation}")
            validated_data["passed"][field_name] = method(field_name, field.value)
        else:
            method = getattr(self, f"_{validation[0]}")
            validated_data["passed"][field_name] = method(field_name, field.value, validation[1])
