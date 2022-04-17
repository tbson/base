from django.db.models import QuerySet


class QuotaValueActionRestrict:
    """
    Only allow owner or his/her manager managing quota value records.
    Who is manager?
    Head of current or above deparment
    """

    @staticmethod
    def is_manager(owner: QuerySet, logged_in_staff: QuerySet) -> bool:
        # System Staff
        if logged_in_staff.user.is_staff:
            return True

        # Is not a head of deparment
        if not logged_in_staff.title.head:
            return False

        # Director
        if logged_in_staff.highest:
            return True

        # Head of current or parent deparment
        return logged_in_staff.title.parent.pk in owner.title.parent_list

    @staticmethod
    def is_allow_to_list(quota: QuerySet, logged_in_staff: QuerySet) -> bool:
        owner = quota.assignment.receiver
        return bool(
            owner == logged_in_staff
            or QuotaValueActionRestrict.is_manager(owner, logged_in_staff)
        )

    @staticmethod
    def is_allow_to_retrieve(quota_value: QuerySet, logged_in_staff: QuerySet) -> bool:
        owner = quota_value.quota.assignment.receiver
        return bool(
            owner == logged_in_staff
            or QuotaValueActionRestrict.is_manager(owner, logged_in_staff)
        )

    @staticmethod
    def is_allow_to_add(quota: QuerySet, logged_in_staff: QuerySet) -> bool:
        owner = quota.assignment.receiver
        return bool(
            owner == logged_in_staff
            or QuotaValueActionRestrict.is_manager(owner, logged_in_staff)
        )

    def is_allow_to_edit_or_delete(
        quota_value: QuerySet, logged_in_staff: QuerySet
    ) -> bool:
        owner = quota_value.quota.assignment.receiver
        return bool(
            owner == logged_in_staff
            or QuotaValueActionRestrict.is_manager(owner, logged_in_staff)
        )
