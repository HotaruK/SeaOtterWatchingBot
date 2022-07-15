from unittest import TestCase
from main import _get_base_time_events
from datetime import datetime


class InnerMethodsTestCase(TestCase):
    def test_get_base_time_events(self):
        now = datetime(2022, 3, 4, 15, 0, 0)
        r1, r2 = _get_base_time_events(now)
        self.assertEqual(r1, "2022/03/04 15:00:00")
        self.assertEqual(r2, "2022/03/04 15:30:00")

        now2 = datetime(2022, 3, 4, 15, 1, 22)
        r3, r4 = _get_base_time_events(now2)
        self.assertEqual(r3, "2022/03/04 15:00:00")
        self.assertEqual(r4, "2022/03/04 15:30:00")

        now3 = datetime(2022, 3, 4, 15, 30, 51)
        r5, r6 = _get_base_time_events(now3)
        self.assertEqual(r5, "2022/03/04 15:30:00")
        self.assertEqual(r6, "2022/03/04 16:00:00")

        now4 = datetime(2022, 3, 4, 15, 45, 51)
        r7, r8 = _get_base_time_events(now4)
        self.assertEqual(r7, "2022/03/04 15:30:00")
        self.assertEqual(r8, "2022/03/04 16:00:00")

        now5 = datetime(2022, 3, 4, 15, 29, 51)
        r9, r10 = _get_base_time_events(now5)
        self.assertEqual(r9, "2022/03/04 15:00:00")
        self.assertEqual(r10, "2022/03/04 15:30:00")
