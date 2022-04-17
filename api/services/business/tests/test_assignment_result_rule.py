from django.test import SimpleTestCase
from ..quota.assignment_result_rule import AssignmentResultRule
from ..quota.consts import AchieveStatus


class GetResultType(SimpleTestCase):
    def test_alert(self):
        result = AssignmentResultRule.get_result_type(0)
        self.assertEqual(result, AchieveStatus.ALERT)

        result = AssignmentResultRule.get_result_type(39)
        self.assertEqual(result, AchieveStatus.ALERT)

    def test_bad(self):
        result = AssignmentResultRule.get_result_type(40)
        self.assertEqual(result, AchieveStatus.BAD)

        result = AssignmentResultRule.get_result_type(59)
        self.assertEqual(result, AchieveStatus.BAD)

    def test_good(self):
        result = AssignmentResultRule.get_result_type(60)
        self.assertEqual(result, AchieveStatus.GOOD)

        result = AssignmentResultRule.get_result_type(89)
        self.assertEqual(result, AchieveStatus.GOOD)

    def test_best(self):
        result = AssignmentResultRule.get_result_type(90)
        self.assertEqual(result, AchieveStatus.BEST)

        result = AssignmentResultRule.get_result_type(101)
        self.assertEqual(result, AchieveStatus.BEST)
