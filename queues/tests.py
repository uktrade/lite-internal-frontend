from unittest import TestCase

from queues.helpers import get_assigned_users_from_cases


class QueuesTests(TestCase):

    def test_get_assigned_users_from_cases(self):
        case_ids = ['adb55711-7fd4-43e1-8e3c-eef84057a846']
        case_assignments = [
            {
                'case': 'adb55711-7fd4-43e1-8e3c-eef84057a846',
                'users': [{'id': '1rylan-1102-441f-a7b4-d55e83989b3b', 'first_name': 'Matt', 'last_name': 'Berninger',
                           'email': 'matt.berninger@mail.com'}]
            },
            {
                'case': 'completely-random-case-id-that-we-dont-want!',
                'users': [{'id': '373e0d9c-1102-441f-a7b4-123234235345', 'first_name': 'Aaron', 'last_name': 'Dessner',
                           'email': 'aaron.dessner@mail.com'}]
            }
        ]
        correct_outcome = [{'id': '1rylan-1102-441f-a7b4-d55e83989b3b', 'first_name': 'Matt', 'last_name': 'Berninger',
                            'email': 'matt.berninger@mail.com'}]

        self.assertEqual(correct_outcome, get_assigned_users_from_cases(case_ids, case_assignments))
