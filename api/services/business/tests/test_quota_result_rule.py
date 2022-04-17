from django.test import SimpleTestCase
from services.helpers.kpi_config import KPIConfig
from modules.kpi.quota_template.consts import Aspect
from ..quota.consts import FormulaDirection, AchieveStatus
from ..quota.quota_result_rule import QuotaResultRule


class GetResultExceedNormal(SimpleTestCase):
    def setUp(self):
        self.direction = FormulaDirection.NORMAL
        KPIConfig.load()

    def test_no_exceed_1(self):
        weight = 40
        achieve = 50
        expected = 50
        _ok, output = QuotaResultRule.get_result_exceed(self.direction)(
            weight, achieve, expected, 0
        )
        eput = 0
        self.assertAlmostEqual(output, eput)

    def test_no_exceed_2(self):
        weight = 40
        achieve = 50
        expected = 51
        _ok, output = QuotaResultRule.get_result_exceed(self.direction)(
            weight, achieve, expected, 0
        )
        eput = 0
        self.assertAlmostEqual(output, eput)

    def test_normal_exceed(self):
        weight = 40
        achieve = 60
        expected = 50
        _ok, output = QuotaResultRule.get_result_exceed(self.direction)(
            weight, achieve, expected, 0
        )
        eput = 8
        self.assertAlmostEqual(output, eput)

    def test_max_exceed(self):
        weight = 40
        achieve = 101
        expected = 50
        _ok, output = QuotaResultRule.get_result_exceed(self.direction)(
            weight, achieve, expected, 0
        )
        eput = 40
        self.assertAlmostEqual(output, eput)


class GetResultExceedInverse(SimpleTestCase):
    def setUp(self):
        self.direction = FormulaDirection.INVERSE
        KPIConfig.load()

    def test_no_exceed_1(self):
        weight = 40
        achieve = 50
        expected = 50
        _ok, output = QuotaResultRule.get_result_exceed(self.direction)(
            weight, achieve, expected, 0
        )
        eput = 0
        self.assertAlmostEqual(output, eput)

    def test_no_exceed_2(self):
        weight = 40
        achieve = 51
        expected = 50
        _ok, output = QuotaResultRule.get_result_exceed(self.direction)(
            weight, achieve, expected, 0
        )
        eput = 0
        self.assertAlmostEqual(output, eput)

    def test_normal_exceed(self):
        weight = 40
        achieve = 50
        expected = 80
        _ok, output = QuotaResultRule.get_result_exceed(self.direction)(
            weight, achieve, expected, 0
        )
        eput = 15
        self.assertAlmostEqual(output, eput)

    def test_max_exceed(self):
        weight = 40
        achieve = -4
        expected = 50
        _ok, output = QuotaResultRule.get_result_exceed(self.direction)(
            weight, achieve, expected, 0
        )
        eput = 40
        self.assertAlmostEqual(output, eput)


class GetResultExceedYesno(SimpleTestCase):
    def setUp(self):
        self.direction = FormulaDirection.YESNO
        KPIConfig.load()

    def test_yes(self):
        weight = 40
        achieve = 1
        expected = 1
        _ok, output = QuotaResultRule.get_result_exceed(self.direction)(
            weight, achieve, expected, 0
        )
        eput = 0
        self.assertAlmostEqual(output, eput)

    def test_no(self):
        weight = 40
        achieve = 0
        expected = 1
        _ok, output = QuotaResultRule.get_result_exceed(self.direction)(
            weight, achieve, expected, 0
        )
        eput = 0
        self.assertAlmostEqual(output, eput)


class Fallback(SimpleTestCase):
    def setUp(self):
        self.weight = 51
        self.minimum = 5.0
        self.expected = 8.0
        self.direction = 999
        self.quota_minimum_bonus_threshold = 80

    def test_happy_case(self):
        calculator = QuotaResultRule.result_calculator_factory(self.direction)
        result = calculator(
            self.weight, self.minimum, self.expected, self.quota_minimum_bonus_threshold
        )()
        self.assertAlmostEqual(result["result"], 0)
        self.assertAlmostEqual(result["result_exceed"], 0)
        self.assertEqual(result["result_type"], AchieveStatus.BAD)


class Normal(SimpleTestCase):
    def setUp(self):
        self.weight = 51
        self.minimum = 5.0
        self.expected = 8.0
        self.direction = FormulaDirection.NORMAL
        self.quota_minimum_bonus_threshold = 80

    def test_bad(self):
        calculator = QuotaResultRule.result_calculator_factory(self.direction)
        achieve = 4.1

        _ok, result = calculator(
            self.weight, self.minimum, self.expected, self.quota_minimum_bonus_threshold
        )(achieve, self.direction, Aspect.FINANCIAL)
        self.assertAlmostEqual(result["result"], 0)
        self.assertAlmostEqual(result["result_exceed"], 0)
        self.assertEqual(result["result_type"], AchieveStatus.BAD)

    def test_good(self):
        calculator = QuotaResultRule.result_calculator_factory(self.direction)
        achieve = 5.1

        _ok, result = calculator(
            self.weight, self.minimum, self.expected, self.quota_minimum_bonus_threshold
        )(achieve, self.direction, Aspect.FINANCIAL)
        self.assertAlmostEqual(result["result"], 41.14)
        self.assertAlmostEqual(result["result_exceed"], 0)
        self.assertEqual(result["result_type"], AchieveStatus.GOOD)

    def test_best(self):
        calculator = QuotaResultRule.result_calculator_factory(self.direction)
        achieve = 8.1

        _ok, result = calculator(
            self.weight, self.minimum, self.expected, self.quota_minimum_bonus_threshold
        )(achieve, self.direction, Aspect.FINANCIAL)
        self.assertAlmostEqual(result["result"], 51)
        self.assertAlmostEqual(result["result_exceed"], 0.6374999999999977)
        self.assertEqual(result["result_type"], AchieveStatus.BEST)

    def test_best_non_financial(self):
        calculator = QuotaResultRule.result_calculator_factory(self.direction)
        achieve = 8.1

        _ok, result = calculator(
            self.weight, self.minimum, self.expected, self.quota_minimum_bonus_threshold
        )(achieve, self.direction, Aspect.CUSTOMER)
        self.assertAlmostEqual(result["result"], 51)
        self.assertAlmostEqual(result["result_exceed"], 0)
        self.assertEqual(result["result_type"], AchieveStatus.BEST)


class Inverse(SimpleTestCase):
    def setUp(self):
        self.weight = 51
        self.minimum = 8.0
        self.expected = 5.0
        self.direction = FormulaDirection.INVERSE
        self.quota_minimum_bonus_threshold = 80

    def test_bad(self):
        calculator = QuotaResultRule.result_calculator_factory(self.direction)
        achieve = 8.1

        _ok, result = calculator(
            self.weight, self.minimum, self.expected, self.quota_minimum_bonus_threshold
        )(achieve, self.direction, Aspect.FINANCIAL)
        self.assertAlmostEqual(result["result"], 0)
        self.assertAlmostEqual(result["result_exceed"], 0)
        self.assertEqual(result["result_type"], AchieveStatus.BAD)

    def test_good(self):
        calculator = QuotaResultRule.result_calculator_factory(self.direction)
        achieve = 5.1

        _ok, result = calculator(
            self.weight, self.minimum, self.expected, self.quota_minimum_bonus_threshold
        )(achieve, self.direction, Aspect.FINANCIAL)
        self.assertAlmostEqual(result["result"], 50.66)
        self.assertAlmostEqual(result["result_exceed"], 0)
        self.assertEqual(result["result_type"], AchieveStatus.GOOD)

    def test_best(self):
        calculator = QuotaResultRule.result_calculator_factory(self.direction)
        achieve = 4.1

        _ok, result = calculator(
            self.weight, self.minimum, self.expected, self.quota_minimum_bonus_threshold
        )(achieve, self.direction, Aspect.FINANCIAL)
        self.assertAlmostEqual(result["result"], 51)
        self.assertAlmostEqual(result["result_exceed"], 9.18)
        self.assertEqual(result["result_type"], AchieveStatus.BEST)


class YesNo(SimpleTestCase):
    def setUp(self):
        self.direction = FormulaDirection.YESNO
        self.weight = 51
        self.minimum = 1
        self.expected = 1
        self.quota_minimum_bonus_threshold = 80

    def test_no(self):
        calculator = QuotaResultRule.result_calculator_factory(self.direction)
        achieve = 0.0

        _ok, result = calculator(
            self.weight, self.minimum, self.expected, self.quota_minimum_bonus_threshold
        )(achieve, self.direction, Aspect.FINANCIAL)
        self.assertAlmostEqual(result["result"], 0)
        self.assertAlmostEqual(result["result_exceed"], 0)
        self.assertEqual(result["result_type"], AchieveStatus.BAD)

    def test_yes(self):
        calculator = QuotaResultRule.result_calculator_factory(self.direction)
        achieve = 1.0

        _ok, result = calculator(
            self.weight, self.minimum, self.expected, self.quota_minimum_bonus_threshold
        )(achieve, self.direction, Aspect.FINANCIAL)
        self.assertAlmostEqual(result["result"], 51)
        self.assertAlmostEqual(result["result_exceed"], 0)
        self.assertEqual(result["result_type"], AchieveStatus.BEST)
