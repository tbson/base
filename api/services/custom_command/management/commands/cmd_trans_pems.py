from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission


class Command(BaseCommand):
    help = "cmd_trans_pems"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Start..."))
        basic_pems = (
            ("add", "Thêm"),
            ("change", "Sửa"),
            ("delete", "Xoá"),
            ("view", "Xem"),
        )
        apps = (
            ("variable", "Cấu hình"),
            ("group", "Nhóm"),
            ("permission", "Quyền"),
            ("staff", "Nhân viên"),
            ("assignment", "Bảng giao KPI"),
            ("assignmentlog", "Log bảng giao KPI"),
            ("campaign", "Đợt giao KPI"),
            ("device", "Thiết bị nhận thông báo"),
            ("notification", "Thông báo"),
            ("position", "Sơ đồ phòng ban"),
            ("providerunit", "Đơn vị cung cấp số liệu"),
            ("quota", "Chỉ tiêu"),
            ("quotatemplate", "Thư viện KPI"),
            ("quotavalue", "Giá trị chỉ tiêu"),
            ("unit", "Đơn vị"),
            ("surveyanswer", "Câu trả lời khảo sát"),
            ("surveyassignment", "Bảng khảo sát"),
            ("surveyquestion", "Câu hỏi khảo sát"),
            ("surveyresult", "Kết quả khảo sát"),
            ("surveysession", "Phiên khảo sát"),
            ("surveysource", "Nguồn câu hỏi khảo sát"),
            ("surveysourcegroup", "Nhóm nguồn câu hỏi khảo sát"),
        )
        for basic_pem, basic_pem_label in basic_pems:
            for app, app_label in apps:
                codename = f"{basic_pem}_{app}"
                try:
                    permision = Permission.objects.get(codename=codename)
                    print(f"[+] {codename}")
                    permision.name = f"{app_label}: {basic_pem_label}"
                    permision.save()
                except Permission.DoesNotExist:
                    pass
        self.stdout.write(self.style.SUCCESS("Done!!!"))
