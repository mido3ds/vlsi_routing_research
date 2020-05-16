import unittest
from mikami_tabuchi import *


class TestIntersection(unittest.TestCase):
    def true_case(self, l0, l1, p):
        self.assertTrue(l0.intersects(l1))
        self.assertEqual(l0.intersection(l1), p)

    def false_case(self, l0, l1):
        self.assertFalse(l0.intersects(l1))
        with self.assertRaises(AssertionError):
            l0.intersection(l1)

    def test_basic(self):
        l0 = Line(Point(0, 1, 1), Point(0, 3, 1), None)
        l1 = Line(Point(0, 2, 0), Point(0, 2, 3), None)
        p = Point(0, 2, 1)
        self.true_case(l0, l1, p)

        l0 = Line(Point(0, 4, 2), Point(0, 4, 7), None)
        l1 = Line(Point(0, 0, 5), Point(0, 5, 5), None)
        p = Point(0, 4, 5)
        self.true_case(l0, l1, p)

        l0 = Line(Point(0, 12, 0), Point(0, 12, 14), None)
        l1 = Line(Point(0, 0, 4), Point(0, 26, 4), None)
        p = Point(0, 12, 4)
        self.true_case(l0, l1, p)

        l0 = Line(Point(0, 3, 1), Point(0, 1, 1), None)
        l1 = Line(Point(0, 2, 0), Point(0, 2, 3), None)
        p = Point(0, 2, 1)
        self.true_case(l0, l1, p)

        l0 = Line(Point(0, 4, 7), Point(0, 4, 2), None)
        l1 = Line(Point(0, 0, 5), Point(0, 5, 5), None)
        p = Point(0, 4, 5)
        self.true_case(l0, l1, p)

        l0 = Line(Point(0, 12, 14), Point(0, 12, 0), None)
        l1 = Line(Point(0, 0, 4), Point(0, 26, 4), None)
        p = Point(0, 12, 4)
        self.true_case(l0, l1, p)

        l0 = Line(Point(0, 3, 1), Point(0, 1, 1), None)
        l1 = Line(Point(0, 2, 3), Point(0, 2, 0), None)
        p = Point(0, 2, 1)
        self.true_case(l0, l1, p)

        l0 = Line(Point(0, 4, 7), Point(0, 4, 2), None)
        l1 = Line(Point(0, 5, 5), Point(0, 0, 5), None)
        p = Point(0, 4, 5)
        self.true_case(l0, l1, p)

        l0 = Line(Point(0, 12, 14), Point(0, 12, 0), None)
        l1 = Line(Point(0, 26, 4), Point(0, 0, 4), None)
        p = Point(0, 12, 4)
        self.true_case(l0, l1, p)

    def test_corner(self):
        l0 = Line(Point(0, 26, 4), Point(0, 21, 4), None)
        l1 = Line(Point(0, 26, 4), Point(0, 26, 6), None)
        p = Point(0, 26, 4)

        self.true_case(l0, l1, p)

        l0 = Line(Point(0, 15, 3), Point(0, 15, 3), None)
        l1 = Line(Point(0, 15, 3), Point(0, 15, 3), None)
        p = Point(0, 15, 3)

        self.true_case(l0, l1, p)

    def test_false(self):
        l0 = Line(Point(0, 15, 3), Point(0, 15, 6), None)
        l1 = Line(Point(0, 13, 11), Point(0, 3, 11), None)
        self.false_case(l0, l1)


if __name__ == "__main__":
    unittest.main()
