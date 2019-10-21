from unittest import TestCase

from letter_templates.templatetags.variable_highlight import ALT_OPEN_TAG, CLOSE_TAG, OPEN_TAG, variable_highlight
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

    def test_variable_highlight(self):
        """
        Ensure that variable_highlight returns the correct value
        """
        test_input = '{% if True %}{{ applicant.name }}{% endif %}' * 2
        expected_output = (ALT_OPEN_TAG + '{% if True %}' + CLOSE_TAG + OPEN_TAG +
                           '{{ applicant.name }}' + CLOSE_TAG + ALT_OPEN_TAG + '{% endif %}' + CLOSE_TAG) * 2

        assert variable_highlight(test_input) == expected_output
