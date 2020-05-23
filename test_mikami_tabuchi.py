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

    def test_corner2(self):
        l0 = Line(Point(0, 6, 3), Point(0, 6, 5), None)
        l1 = Line(Point(0, 3, 2), Point(0, 14, 2), None)
        self.false_case(l0, l1)

    def test_point(self):
        l0 = Line(Point(0, 0, 1), Point(0, 1, 1), None)
        l1 = Line(Point(0, 0, 1), Point(0, 0, 1), None)
        self.true_case(l0, l1, Point(0, 0, 1))


class TestBacktracking(unittest.TestCase):
    def test_basic(self):
        p0 = Point(0, 6, 1)
        l0 = Line(p0, Point(0, 6, 5), p0)
        self.assertTupleEqual(l0.backtrack(), (p0, [l0]))

    def test_complex(self):
        p0 = Point(0, 6, 1)
        l0 = Line(p0, Point(0, 6, 5), p0)
        l1 = Line(Point(0, 3, 2), Point(0, 14, 2), l0)
        l2 = Line(Point(0, 12, 1), Point(0, 12, 4), l1)
        l3 = Line(Point(0, 11, 4), Point(0, 19, 4), l2)

        self.assertTupleEqual(l3.backtrack(), (p0, [l3, l2, l1, l0]))

    def test_none(self):
        p0 = Point(0, 6, 1)
        l0 = Line(p0, Point(0, 6, 5), None)
        with self.assertRaises(AssertionError):
            l0.backtrack()


class TestBuiltPath(unittest.TestCase):
    def test_basic(self):
        # p0 -> l0
        p0 = Point(0, 6, 1)
        l0 = Line(p0, Point(0, 6, 5), p0)

        # p1 -> l1
        p1 = Point(0, 14, 2)
        l1 = Line(Point(0, 3, 2), p1, p1)

        # p0 -> l0,l1 -> p1
        self.assertListEqual(build_path(l0, l1), [
            p0, Point(0, 6, 2), p1
        ])

    def test_big(self):
        # p0 -> l0 -> l1
        p0 = Point(0, 6, 1)
        l0 = Line(p0, Point(0, 6, 5), p0)
        l1 = Line(Point(0, 3, 2), Point(0, 14, 2), l0)

        # p1 -> l3 -> l2
        p1 = Point(0, 19, 4)
        l3 = Line(Point(0, 11, 4), p1, p1)
        l2 = Line(Point(0, 12, 1), Point(0, 12, 4), l3)

        # p0 -> l0,l1 -> l1,l2 -> l2,l3 -> p1
        self.assertListEqual(build_path(l1, l2), [
            p0, Point(0, 6, 2), Point(0, 12, 2), Point(0, 12, 4), p1
        ])

    def test_failure(self):
        # p0 -> l0
        p0 = Point(0, 6, 3)
        l0 = Line(p0, Point(0, 6, 5), p0)

        # p1 -> l1
        p1 = Point(0, 14, 2)
        l1 = Line(Point(0, 3, 2), p1, p1)

        # p0 -> no intersection(l0,l1) ->? p1
        with self.assertRaises(AssertionError):
            build_path(l0, l1)


if __name__ == "__main__":
    unittest.main()
