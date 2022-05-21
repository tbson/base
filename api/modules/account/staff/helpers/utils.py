from django.db.models import QuerySet
from modules.account.staff.models import Staff
from modules.account.staff.helpers.srs import StaffSr
from modules.account.user.helpers.utils import UserUtils


class StaffUtils:
    @staticmethod
    def seeding(index: int, single: bool = False, save: bool = True) -> QuerySet:

        if index == 0:
            raise Exception("Indext must be start with 1.")

        def get_data(i: int) -> dict:
            phone_number = "+8490669652{}".format(i)
            if i >= 10:
                phone_number = "+849066965{}".format(i)
            test_password = "SamplePassword123!@#"
            data = {
                "email": "test{}@gmail.com".format(i),
                "phone_number": phone_number,
                "first_name": f"first{i}",
                "last_name": f"last{i}",
                "password": test_password,
            }

            if save is False:
                return data

            try:
                instance = Staff.objects.get(user__username=data["email"])
            except Staff.DoesNotExist:
                instance = StaffUtils.create_staff(data)

            return instance

        def get_list_data(index):
            return [get_data(i) for i in range(1, index + 1)]

        return get_data(index) if single is True else get_list_data(index)

    @staticmethod
    def create_staff(data: dict) -> QuerySet:
        user = UserUtils.create_user(data)

        # Create staff
        staff_data = {
            "user": user.pk,
        }
        sr = StaffSr(data=staff_data)
        sr.is_valid(raise_exception=True)
        return sr.save()

    @staticmethod
    def update_staff(staff: QuerySet, data: dict) -> QuerySet:
        user = UserUtils.update_user(staff.user, data)

        # Create staff
        staff_data = {
            "user": user.pk,
        }
        sr = StaffSr(staff, data=staff_data, partial=True)
        sr.is_valid(raise_exception=True)
        return sr.save()