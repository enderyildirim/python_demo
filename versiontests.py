import unittest

from version import Version


class VersionTests(unittest.TestCase):

    def test_constructor_parameters_validity(self):
        with self.assertRaises(AssertionError):
            Version(-1, 0, 0)
        with self.assertRaises(AssertionError):
            Version(0, -1, 0)
        with self.assertRaises(AssertionError):
            Version(0, 0, -1)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, max_major=-1)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, max_minor=-1)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, max_micro=-1)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, min_major=-1)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, min_minor=-1)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, min_micro=-1)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, major_inc=0)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, minor_inc=0)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, micro_inc=0)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, major_inc=-1)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, minor_inc=-1)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, micro_inc=-1)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, major_dec=0)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, minor_dec=0)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, micro_dec=0)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, major_dec=-1)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, minor_dec=-1)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, micro_dec=-1)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, max_major=5, min_major=5)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, max_minor=5, min_minor=5)
        with self.assertRaises(AssertionError):
            Version(0, 0, 0, max_micro=5, min_micro=5)

    def test_equality(self):
        self.assertTrue(Version() == Version())
        self.assertTrue(Version() == Version(0, 0, 0))
        self.assertTrue(Version().parse("0.0.0") == Version(0, 0, 0))
        self.assertTrue(Version().parse("0.0.0") == Version())
        self.assertTrue(Version().parse("1.1.1") == Version(1, 1, 1))
        self.assertTrue(Version().parse("9.9.99") == Version(9, 9, 99))
        self.assertTrue(Version().parse("9.9.00") == Version(9, 9, 0))
        self.assertTrue(Version().parse("9.9.000") == Version(9, 9, 0))
        self.assertTrue(Version().parse("9.9.099") == Version(9, 9, 99))
        self.assertTrue(Version().parse("09.09.099") == Version(9, 9, 99))
        self.assertTrue(Version().parse("0.9.099") == Version(0, 9, 99))
        self.assertTrue(Version().parse("9.09.099") == Version(9, 9, 99))
        self.assertTrue(Version().parse("9.00.099") == Version(9, 0, 99))
        self.assertTrue(Version().parse("9.000.099") == Version(9, 0, 99))
        self.assertEqual(Version(), Version())
        self.assertEqual(Version(), Version(0, 0, 0))
        self.assertEqual(Version().parse("0.0.0"), Version(0, 0, 0))
        self.assertEqual(Version().parse("0.0.0"), Version())
        self.assertEqual(Version().parse("1.1.1"), Version(1, 1, 1))
        self.assertEqual(Version().parse("9.9.99"), Version(9, 9, 99))
        self.assertEqual(Version().parse("9.9.00"), Version(9, 9, 0))
        self.assertEqual(Version().parse("9.9.000"), Version(9, 9, 0))
        self.assertEqual(Version().parse("9.9.099"), Version(9, 9, 99))
        self.assertEqual(Version().parse("09.09.099"), Version(9, 9, 99))
        self.assertEqual(Version().parse("0.9.099"), Version(0, 9, 99))
        self.assertEqual(Version().parse("9.09.099"), Version(9, 9, 99))
        self.assertEqual(Version().parse("9.00.099"), Version(9, 0, 99))
        self.assertEqual(Version().parse("9.000.099"), Version(9, 0, 99))

    def test_compares(self):
        self.assertTrue(Version(1, 0, 0) > Version())
        self.assertTrue(Version(0, 1, 0) > Version())
        self.assertTrue(Version(0, 0, 1) > Version())
        self.assertTrue(Version(1, 0, 1) > Version())
        self.assertTrue(Version(1, 1, 0) > Version())
        self.assertTrue(Version(1, 1, 1) > Version())
        self.assertTrue(Version(0, 1, 1) > Version())
        self.assertTrue(Version(1, 0, 0) > Version(0, 0, 1))
        self.assertTrue(Version(0, 1, 0) > Version(0, 0, 1))
        self.assertTrue(Version(1, 1, 0) > Version(0, 0, 1))
        self.assertTrue(Version(0, 1, 1) > Version(0, 0, 1))

        self.assertTrue(Version().parse("1.0.90") > Version().parse("1.0.89"))
        self.assertTrue(Version().parse("9.99.999") > Version().parse("9.99.998"))
        self.assertTrue(Version().parse("9.99.999") > Version().parse("1.99.999"))
        self.assertTrue(Version().parse("1.0.90") < Version().parse("1.0.91"))
        self.assertTrue(Version().parse("1.0.9") < Version().parse("1.0.90"))
        self.assertTrue(Version().parse("0.0.9") < Version().parse("0.0.90"))
