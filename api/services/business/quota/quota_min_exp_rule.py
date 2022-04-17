from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError
from .consts import FormulaDirection


class QuotaMinExpdRule:
    @staticmethod
    def ensure_constrain(formula_direction: int, minimum: float, expected: float):
        options = {
            FormulaDirection.NORMAL: QuotaMinExpdRule.__normal,
            FormulaDirection.INVERSE: QuotaMinExpdRule.__inverse,
            FormulaDirection.YESNO: QuotaMinExpdRule.__yesno,
        }
        options[formula_direction](minimum, expected)

    @staticmethod
    def __normal(minimum: float, expected: float):
        error_message = {
            "minimum": _("Minimum value can not be larger than expected value")
        }
        if minimum > expected:
            raise ValidationError(error_message)

    @staticmethod
    def __inverse(minimum: float, expected: float):
        error_message = {
            "minimum": _("Minimum value can not be smaller than expected value")
        }
        if minimum < expected:
            raise ValidationError(error_message)

    @staticmethod
    def __yesno(minimum: float, expected: float):
        message = _("Please use 0 or 1 for this input")

        allowed_value = [0, 1]

        if minimum not in allowed_value:
            raise ValidationError({"minimum": message})

        if expected not in allowed_value:
            raise ValidationError({"expected": message})
