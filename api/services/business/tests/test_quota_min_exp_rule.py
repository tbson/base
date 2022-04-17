from django.test import SimpleTestCase
from rest_framework.serializers import ValidationError
from ..quota.consts import FormulaDirection
from ..quota.quota_min_exp_rule import QuotaMinExpdRule


class Normal(SimpleTestCase):
    def setUp(self):
        self.formula_direction = FormulaDirection.NORMAL

    def test_happy_case(self):
        minimum = 5.0
        expected = 8.0

        QuotaMinExpdRule.ensure_constrain(self.formula_direction, minimum, expected)
        self.assertEqual(0, 0)

    def test_wrong_value(self):
        minimum = 9.0
        expected = 8.0

        with self.assertRaises(ValidationError):
            QuotaMinExpdRule.ensure_constrain(self.formula_direction, minimum, expected)


class Inverse(SimpleTestCase):
    def setUp(self):
        self.formula_direction = FormulaDirection.INVERSE

    def test_happy_case(self):
        minimum = 9.0
        expected = 8.0

        QuotaMinExpdRule.ensure_constrain(self.formula_direction, minimum, expected)
        self.assertEqual(0, 0)

    def test_wrong_value(self):
        minimum = 5.0
        expected = 8.0

        with self.assertRaises(ValidationError):
            QuotaMinExpdRule.ensure_constrain(self.formula_direction, minimum, expected)


class YesNo(SimpleTestCase):
    def setUp(self):
        self.formula_direction = FormulaDirection.YESNO

    def test_happy_case(self):
        minimum = 0
        expected = 1

        QuotaMinExpdRule.ensure_constrain(self.formula_direction, minimum, expected)
        self.assertEqual(0, 0)

    def test_wrong_minimum(self):
        minimum = 2
        expected = 1

        with self.assertRaises(ValidationError):
            QuotaMinExpdRule.ensure_constrain(self.formula_direction, minimum, expected)

    def test_wrong_expected(self):
        minimum = 1
        expected = 2

        with self.assertRaises(ValidationError):
            QuotaMinExpdRule.ensure_constrain(self.formula_direction, minimum, expected)
