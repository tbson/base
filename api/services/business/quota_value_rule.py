from django.db.models import QuerySet
from services.helpers.utils import Utils


class QuotaValueRule:
    @staticmethod
    def is_edit_old_record(quota_value: QuerySet) -> bool:
        today = Utils.today()
        return quota_value.created_at.date() < today

    @staticmethod
    def is_enough_today(quota_value: QuerySet) -> bool:
        today = Utils.today()
        model = type(quota_value)
        return bool(
            model.objects.filter(
                quota_id=quota_value.quota_id, created_at__date=today
            ).count()
        )

    @staticmethod
    def get_achieve(quota: QuerySet) -> float:
        quota_value = quota.quota_values.order_by("-id").first()
        if not quota_value:
            return 0
        return quota_value.value
