from unittest import TestCase

from cases.helpers.advice import order_grouped_advice


class CaseTests(TestCase):
    def test_order_grouped_advice(self):
        initial_order = {
            1: {"type": {"key": "refuse"}},
            2: {"type": {"key": "approve"}},
            3: {"type": {"key": "no_licence_required"}},
            4: {"type": {"key": "refuse"}},
            5: {"type": {"key": "conflicting"}},
            6: {"type": {"key": "no_advice"}},
            7: {"type": {"key": "not_applicable"}},
        }

        ordered = list(order_grouped_advice(initial_order).keys())

        self.assertEqual(ordered[0], 5)
        self.assertEqual(ordered[1], 2)
        self.assertEqual(ordered[2], 3)
        self.assertEqual(ordered[3], 7)
        self.assertEqual(ordered[4], 1)
        self.assertEqual(ordered[5], 4)
        self.assertEqual(ordered[6], 6)
