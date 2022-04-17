from services.helpers.kpi_config import KPIConfig
from .consts import AchieveStatus
from .quota_result_rule import QuotaResultRule


class AssignmentResultRule:
    @staticmethod
    def get_result_type(result: float) -> int:
        ASSIGNMENT_STATUS = KPIConfig.get("ASSIGNMENT_STATUS")
        ALERT = ASSIGNMENT_STATUS[0]
        BAD = ASSIGNMENT_STATUS[1]
        GOOD = ASSIGNMENT_STATUS[2]

        conditions = {
            AchieveStatus.ALERT: result < ALERT,
            AchieveStatus.BAD: ALERT <= result < BAD,
            AchieveStatus.GOOD: BAD <= result < GOOD,
            AchieveStatus.BEST: result >= GOOD,
        }

        return QuotaResultRule.get_status(conditions)
