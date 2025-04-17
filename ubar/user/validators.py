import re

from django.core.exceptions import ValidationError


def phone_validator(phone: str, VE=ValidationError) -> str:
    if not re.match(r"^09\d{9}$", phone):
        raise VE("Phone number must contain only 11 digits and starts with 09")
    return phone


def national_code_validator(national_code: str):
    if not re.match(r"^\d{10}$", national_code):
        raise ValidationError("Invalid national code.")
    return national_code
