from typing import Dict
import math
from django.conf import settings
from services.helpers.utils import Utils
from services.helpers.kpi_config import KPIConfig
from modules.kpi.quota_template.consts import Aspect
from .consts import FormulaDirection, AchieveStatus


class QuotaResultRule:
    @staticmethod
    def get_status(conditions: Dict) -> str:
        for key in conditions:
            if conditions[key] is True:
                return key
        return AchieveStatus.BAD

    @staticmethod
    def get_invalid_cond(conds, params) -> str:
        for cond in conds:
            if not Utils.parse_exp(cond[0], params):
                return cond[1]
        return ""

    @staticmethod
    def get_result_exceed(direction: int):
        def inner(
            weight: float, achieve: float, expected: float, minimum: float
        ) -> float:
            if direction == FormulaDirection.YESNO:
                return True, 0
            elif direction == FormulaDirection.NORMAL:
                if achieve <= expected:
                    return True, 0
                formula = "QUOTA_EXCEED_NORMAL_FORMULA"
            else:
                if achieve >= expected:
                    return True, 0
                formula = "QUOTA_EXCEED_INVERSE_FORMULA"

            formula_dict = KPIConfig.get(formula)
            params = dict(
                weight=weight, achieve=achieve, expected=expected, minimum=minimum
            )
            if err := QuotaResultRule.get_invalid_cond(formula_dict["cond"], params):
                return False, err

            result = Utils.parse_exp(formula_dict["rule"], params)

            if result < 0:
                return True, 0

            max_result = weight * KPIConfig.get("QUOTA_MAXIMUM_EXCEED_WEIGHT") / 100
            if result > max_result:
                return True, max_result

            return True, result

        return inner

    @staticmethod
    def __normal(
        weight: float,
        minimum: float,
        expected: float,
        quota_minimum_bonus_threshold: float,
    ) -> Dict:
        def inner(achieve: float, direction: int, aspect: int):
            conditions = {
                AchieveStatus.BAD: achieve < minimum,
                AchieveStatus.GOOD: minimum <= achieve < expected,
                AchieveStatus.BEST: achieve >= expected,
            }

            status = QuotaResultRule.get_status(conditions)
            formula_dict = KPIConfig.get("QUOTA_RESULT_NORMAL_FORMULA")
            exp = formula_dict["rule"]
            X = quota_minimum_bonus_threshold / 100
            params = dict(
                X=X, weight=weight, achieve=achieve, minimum=minimum, expected=expected
            )

            if err := QuotaResultRule.get_invalid_cond(formula_dict["cond"], params):
                return False, err

            ok, result_exceed = QuotaResultRule.get_result_exceed(direction)(
                weight, achieve, expected, minimum
            )

            if not ok:
                return False, result_exceed

            values = {
                AchieveStatus.BAD: (0, 0),
                AchieveStatus.GOOD: (Utils.parse_exp(exp, params), 0),
                AchieveStatus.BEST: (
                    weight,
                    result_exceed,
                ),
            }

            results = values[status]

            results = {
                "result": results[0],
                "result_exceed": results[1] if aspect == Aspect.FINANCIAL else 0,
                "result_type": status,
            }
            return True, results

        return inner

    @staticmethod
    def __inverse(
        weight: float,
        minimum: float,
        expected: float,
        quota_minimum_bonus_threshold: float,
    ) -> Dict:
        def inner(achieve: float, direction: int, aspect: int):
            conditions = {
                AchieveStatus.BAD: achieve > minimum,
                AchieveStatus.GOOD: expected < achieve <= minimum,
                AchieveStatus.BEST: achieve <= expected,
            }

            status = QuotaResultRule.get_status(conditions)
            formula_dict = KPIConfig.get("QUOTA_RESULT_INVERSE_FORMULA")

            exp = formula_dict["rule"]
            X = quota_minimum_bonus_threshold / 100
            params = dict(
                X=X, weight=weight, achieve=achieve, minimum=minimum, expected=expected
            )

            if err := QuotaResultRule.get_invalid_cond(formula_dict["cond"], params):
                return False, err

            ok, result_exceed = QuotaResultRule.get_result_exceed(direction)(
                weight, achieve, expected, minimum
            )
            if not ok:
                return False, result_exceed

            values = {
                AchieveStatus.BAD: (0, 0),
                AchieveStatus.GOOD: (Utils.parse_exp(exp, params), 0),
                AchieveStatus.BEST: (
                    weight,
                    result_exceed,
                ),
            }

            results = values[status]

            results = {
                "result": results[0],
                "result_exceed": results[1] if aspect == Aspect.FINANCIAL else 0,
                "result_type": status,
            }
            return True, results

        return inner

    @staticmethod
    def __yesno(
        weight: float,
        _minimum: float,
        _expected: float,
        _quota_minimum_bonus_threshold: float,
    ) -> Dict:
        def inner(achieve: float, _direction: int, _aspect: int):
            result = 0
            result_exceed = 0
            result_type = AchieveStatus.BAD

            if math.isclose(achieve, 1.0):
                result = weight
                result_type = AchieveStatus.BEST

            results = {
                "result": result,
                "result_exceed": result_exceed,
                "result_type": result_type,
            }
            return True, results

        return inner

    @staticmethod
    def result_calculator_factory(formula_direction: int):
        def fallback(
            _weight: float,
            _minimum: float,
            _expected: float,
            _quota_minimum_bonus_threshold: float,
        ) -> int:
            def inner(_achieve=0, _direction=0, _aspect=0):
                return {
                    "result": 0,
                    "result_exceed": 0,
                    "result_type": AchieveStatus.BAD,
                }

            return inner

        methods = {
            FormulaDirection.NORMAL: QuotaResultRule.__normal,
            FormulaDirection.INVERSE: QuotaResultRule.__inverse,
            FormulaDirection.YESNO: QuotaResultRule.__yesno,
        }
        return methods.get(formula_direction, fallback)
