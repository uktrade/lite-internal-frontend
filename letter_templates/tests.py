from unittest import TestCase

from letter_templates.views.manage import LetterTemplateEditLetterParagraphs


class LetterTemplateEditLetterParagraphsTestCase(TestCase):
    def test_sort_letter_paragraphs(self):
        ids = ["abc", "def", "uvw", "xyz"]
        result = LetterTemplateEditLetterParagraphs.sort_letter_paragraphs([
                {"id": "xyz", "label": "last"},
                {"id": "abc", "label": "first"},
                {"id": "uvw", "label": "third"},
                {"id": "def", "label": "second"},
                {"id": "klm", "label": "not in result"},
            ],
            ids + ["nop"],
        )
        result_ids = [r["id"] for r in result]
        self.assertEqual(ids, result_ids)
