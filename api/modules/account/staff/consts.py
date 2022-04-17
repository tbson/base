class StaffType:
    OFFICIAL = 1
    PROBATION = 2
    CONTRACTING = 3
    QUIT = 4
    MATERNITY = 5
    SECONDMENT = 6


STAFF_TYPE_CHOICES = (
    (StaffType.OFFICIAL, "Chính thức"),
    (StaffType.PROBATION, "Thử việc"),
    (StaffType.CONTRACTING, "Khoán / hợp đồng"),
    (StaffType.QUIT, "Nghỉ việc"),
    (StaffType.MATERNITY, "Nghỉ thai sản"),
    (StaffType.SECONDMENT, "Biệt phái"),
)

STAFF_TYPE_DICT = dict(STAFF_TYPE_CHOICES)

STAFF_TYPE_OPTIONS = [
    {"value": item[0], "label": item[1]} for item in STAFF_TYPE_CHOICES
]
