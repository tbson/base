class FormulaDirection:
    NORMAL = 0
    INVERSE = 1
    YESNO = 2


class AchieveStatus:
    ALERT = 0
    BAD = 1
    GOOD = 2
    BEST = 3


ACHIEVE_STATUS_CHOICES = (
    (AchieveStatus.ALERT, "Báo động đỏ"),
    (AchieveStatus.BAD, "Chưa hoàn thành"),
    (AchieveStatus.GOOD, "Hoàn thành"),
    (AchieveStatus.BEST, "Xuất sắc"),
)

ACHIEVE_STATUS_DICT = dict(ACHIEVE_STATUS_CHOICES)

ACHIEVE_STATUS_OPTIONS = [
    {"value": item[0], "label": item[1]} for item in ACHIEVE_STATUS_CHOICES
]
