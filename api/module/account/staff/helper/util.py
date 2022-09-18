from custom_type import query_set, query_obj
from service.framework_service import Group, Permission
from module.account.helper.sr import GroupSr
from module.account.staff.models import Staff
from module.account.staff.helper.sr import StaffSr
from module.account.user.helper.util import UserUtil


class StaffUtil:
    @staticmethod
    def seeding(index: int, single: bool = False, save: bool = True) -> query_set:

        if index == 0:
            raise Exception("Indext must be start with 1.")

        def get_data(i: int) -> dict:
            phone_number = f"+849066965{i}" if i >= 10 else f"+8490669652{i}"
            test_password = UserUtil.get_default_test_pwd()
            data = {
                "email": f"test{i}@gmail.com",
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
                instance = StaffUtil.create_staff(data)
                group, _ = Group.objects.get_or_create(name="test")
                group.permissions.set(Permission.objects.all())
                instance.user.groups.set([group])

            return instance

        def get_list_data(index):
            return [get_data(i) for i in range(1, index + 1)]

        return get_data(index) if single is True else get_list_data(index)

    @staticmethod
    def create_staff(data: dict) -> query_obj:
        user = UserUtil.create_user(data)

        # Create staff
        staff_data = data | {"user": user.pk}
        sr = StaffSr(data=staff_data)
        sr.is_valid(raise_exception=True)
        return sr.save()

    @staticmethod
    def update_staff(staff: query_obj, data: dict) -> query_obj:
        user = UserUtil.update_user(staff.user, data)

        # Update staff
        staff_data = data | {"user": user.pk}
        sr = StaffSr(staff, data=staff_data, partial=True)
        sr.is_valid(raise_exception=True)
        return sr.save()

    @staticmethod
    def get_list_group() -> list:
        raw_data = GroupSr(Group.objects.exclude(name="customer"), many=True).data
        return [{"value": group["id"], "label": group["name"]} for group in raw_data]
