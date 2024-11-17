import unittest
from reop import Result, Option, result_wrapper, option_wrapper

class TestSafepy(unittest.TestCase):
    # Test Result functionality
    def test_result_ok(self):
        @result_wrapper
        def add(a, b):
            return a + b

        res = add(2, 3)
        self.assertTrue(res.is_ok)
        self.assertEqual(res.unwrap(), 5)

    def test_result_err(self):
        @result_wrapper
        def divide(a, b):
            return a / b

        res = divide(10, 0)
        self.assertTrue(res.is_err)
        self.assertIsInstance(res.unwrap_err(), ZeroDivisionError)

    # Test Option functionality
    def test_option_some(self):
        @option_wrapper
        def find_value(key, data):
            return data.get(key)

        opt = find_value("a", {"a": 42})
        self.assertTrue(opt.is_some)
        self.assertEqual(opt.unwrap(), 42)

    def test_option_none(self):
        @option_wrapper
        def find_value(key, data):
            return data.get(key)

        opt = find_value("b", {"a": 42})
        self.assertTrue(opt.is_none)
        self.assertEqual(opt.unwrap_or(0), 0)

    def test_option_map(self):
        opt = Option(10).map(lambda x: x * 2)
        self.assertTrue(opt.is_some)
        self.assertEqual(opt.unwrap(), 20)

    def test_option_and_then(self):
        def add_one(x):
            return Option(x + 1)

        opt = Option(5).and_then(add_one).and_then(add_one)
        self.assertTrue(opt.is_some)
        self.assertEqual(opt.unwrap(), 7)


if __name__ == "__main__":
    unittest.main()
