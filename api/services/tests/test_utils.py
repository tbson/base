from django.test import SimpleTestCase
from services.helpers.utils import Utils

# Create your tests here.


class GetNextUidOrder(SimpleTestCase):
    def test_normal_case(self):
        uid = "1HN001A5"
        output = Utils.get_next_uid_index(uid)
        eput = 6
        self.assertEqual(output, eput)

    def test_missing_uid(self):
        uid = ""
        output = Utils.get_next_uid_index(uid)
        eput = 1
        self.assertEqual(output, eput)


class IsSemiContain(SimpleTestCase):
    def test_normal_case(self):
        parent = [1, 2, 3]
        child = [1, 6]
        output = Utils.is_semi_contain(parent, child)
        eput = True
        self.assertEqual(output, eput)

    def test_normal_case_but_child_larger_than_parent(self):
        parent = [1, 2, 3]
        child = [1, 6, 3, 5]
        output = Utils.is_semi_contain(parent, child)
        eput = True
        self.assertEqual(output, eput)

    def test_sub_set(self):
        parent = [1, 2, 3]
        child = [1, 3]
        output = Utils.is_semi_contain(parent, child)
        eput = False
        self.assertEqual(output, eput)

    def test_no_intersection(self):
        parent = [1, 2, 3]
        child = [4, 5]
        output = Utils.is_semi_contain(parent, child)
        eput = False
        self.assertEqual(output, eput)


class RemoveSpecialChars(SimpleTestCase):
    def test_normal_case(self):
        input = "abc"
        output = Utils.remove_special_chars(input)
        eput = "abc"
        self.assertEqual(output, eput)

    def test_special_case(self):
        input = " abc* "
        output = Utils.remove_special_chars(input)
        eput = "abc"
        self.assertEqual(output, eput)

    def test_special_case_upper(self):
        input = " abc* "
        output = Utils.remove_special_chars(input, True)
        eput = "ABC"
        self.assertEqual(output, eput)


class PasswordValidate(SimpleTestCase):
    def test_happy_case(self):
        input = "1Abcdefg"
        output = Utils.password_validate(input)
        eput = []
        self.assertEqual(output, eput)

    def test_too_short(self):
        input = "1Abcdef"
        output = Utils.password_validate(input)
        self.assertEqual(len(output), 1)

    def test_no_number(self):
        input = "Abcdefgh"
        output = Utils.password_validate(input)
        self.assertEqual(len(output), 1)

    def test_no_upper(self):
        input = "1abcdefgh"
        output = Utils.password_validate(input)
        self.assertEqual(len(output), 1)


class DigitToBool(SimpleTestCase):
    def test_happy_case_str_0(self):
        input = "0"
        output = Utils.digit_to_bool(input)
        eput = False
        self.assertEqual(output, eput)

    def test_happy_case_str_1(self):
        input = "1"
        output = Utils.digit_to_bool(input)
        eput = True
        self.assertEqual(output, eput)

    def test_happy_case_int_0(self):
        input = 0
        output = Utils.digit_to_bool(input)
        eput = False
        self.assertEqual(output, eput)

    def test_happy_case_int_1(self):
        input = 1
        output = Utils.digit_to_bool(input)
        eput = True
        self.assertEqual(output, eput)

    def test_none(self):
        input = None
        output = Utils.digit_to_bool(input)
        eput = False
        self.assertEqual(output, eput)

    def test_empty_string(self):
        input = ""
        output = Utils.digit_to_bool(input)
        eput = False
        self.assertEqual(output, eput)

    def test_other_string(self):
        input = "hello"
        output = Utils.digit_to_bool(input)
        eput = False
        self.assertEqual(output, eput)

    def test_other_int(self):
        input = 3
        output = Utils.digit_to_bool(input)
        eput = False
        self.assertEqual(output, eput)


class DateStrStripMillisecs(SimpleTestCase):
    def test_happy_case(self):
        input = "2020-02-27T12:15:01.623+07:00"
        output = Utils.date_str_strip_millisecs(input)
        eput = "2020-02-27T12:15:01+07:00"
        self.assertEqual(output, eput)

    def test_bad_format(self):
        input = "2020-2-27T12:15:01.623+07:00"
        output = Utils.date_str_strip_millisecs(input)
        eput = None
        self.assertEqual(output, eput)

    def test_none(self):
        input = None
        output = Utils.date_str_strip_millisecs(input)
        eput = None
        self.assertEqual(output, eput)


class MaskPhoneNumber(SimpleTestCase):
    def test_happy_case(self):
        input = "+84906696527"
        output = Utils.mask_prefix(input)
        eput = "********6527"
        self.assertEqual(output, eput)

    def test_happy_case_1(self):
        input = "+84906696527"
        mask_length = 5
        output = Utils.mask_prefix(input, mask_length)
        eput = "*******96527"
        self.assertEqual(output, eput)

    def test_happy_case_2(self):
        input = "+84906696527"
        mask_length = 6
        output = Utils.mask_prefix(input, mask_length)
        eput = "******696527"
        self.assertEqual(output, eput)


class MaskEmail(SimpleTestCase):
    def test_name_1(self):
        input = "a@gmail.com"
        output = Utils.mask_email(input)
        eput = "*@gmail.com"
        self.assertEqual(output, eput)

    def test_name_2(self):
        input = "ab@gmail.com"
        output = Utils.mask_email(input)
        eput = "*b@gmail.com"
        self.assertEqual(output, eput)

    def test_name_3(self):
        input = "abc@gmail.com"
        output = Utils.mask_email(input)
        eput = "*bc@gmail.com"
        self.assertEqual(output, eput)

    def test_name_4(self):
        input = "abcd@gmail.com"
        output = Utils.mask_email(input)
        eput = "**cd@gmail.com"
        self.assertEqual(output, eput)

    def test_name_5(self):
        input = "abcde@gmail.com"
        output = Utils.mask_email(input)
        eput = "*bcde@gmail.com"
        self.assertEqual(output, eput)

    def test_name_6(self):
        input = "abcdef@gmail.com"
        output = Utils.mask_email(input)
        eput = "**cdef@gmail.com"
        self.assertEqual(output, eput)

    def test_name_7(self):
        input = "abcdefg@gmail.com"
        output = Utils.mask_email(input)
        eput = "***defg@gmail.com"
        self.assertEqual(output, eput)


class IsBooleanDict(SimpleTestCase):
    def test_all_boolean(self):
        input = {
            "key1": True,
            "key2": False,
            "key3": True,
        }
        output = Utils.is_boolean_dict(input)
        eput = True
        self.assertEqual(output, eput)

    def test_some_boolean(self):
        input = {
            "key1": True,
            "key2": None,
            "key3": True,
        }
        output = Utils.is_boolean_dict(input)
        eput = False
        self.assertEqual(output, eput)

    def test_empty(self):
        input = {}
        output = Utils.is_boolean_dict(input)
        eput = False
        self.assertEqual(output, eput)


class EnsureSpaceSlash(SimpleTestCase):
    def test_happy_case(self):
        input = "abc/def"
        output = Utils.ensure_space_slash(input)
        eput = "abc / def"
        self.assertEqual(output, eput)

        input = "Quy trình/ dịch vụ/ sản phẩm"
        output = Utils.ensure_space_slash(input)
        eput = "Quy trình / dịch vụ / sản phẩm"
        self.assertEqual(output, eput)


class GetTupleValue(SimpleTestCase):
    def test_happy_case(self):
        input_tuple = (
            ("key1", "value1"),
            ("key2", "value2"),
        )
        key = "key1"
        output = Utils.get_tuple_value(input_tuple, key)
        eput = "value1"
        self.assertEqual(output, eput)

    def test_not_found(self):
        input_tuple = (
            ("key1", "value1"),
            ("key2", "value2"),
        )
        key = "key3"
        output = Utils.get_tuple_value(input_tuple, key)
        eput = None
        self.assertEqual(output, eput)

    def test_not_found_with_default(self):
        input_tuple = (
            ("key1", "value1"),
            ("key2", "value2"),
        )
        key = "key3"
        output = Utils.get_tuple_value(input_tuple, key, "hello")
        eput = "hello"
        self.assertEqual(output, eput)
