from django.shortcuts import render
from django.views.generic import TemplateView

from letter_templates.helpers import get_template_content
from letter_templates.services import get_letter_paragraphs
from picklists.services import get_picklists


def get_order_paragraphs_page(request, template_content):
    letter_paragraphs = get_letter_paragraphs(request, template_content['letter_paragraphs'])
    return render(request, 'letter_templates/order_letter_paragraphs.html',
                  {
                      'letter_paragraphs': letter_paragraphs,
                      'name': template_content['name'],
                      'layout': template_content['layout'],
                      'restricted_to': template_content['restricted_to']
                  })


class LetterParagraphs(TemplateView):
    @staticmethod
    def _add_letter_paragraph(request, template_content):
        all_letter_paragraphs = get_picklists(request, 'letter_paragraph')
        context = {
            'name': template_content['name'],
            'layout': template_content['layout'],
            'restricted_to': template_content['restricted_to'],
            'letter_paragraphs': [x for x in all_letter_paragraphs['picklist_items'] if
                                  x['id'] not in template_content['letter_paragraphs']],
            'existing_letter_paragraphs': template_content['letter_paragraphs']
        }
        return render(request, 'letter_templates/add_letter_paragraphs.html', context)

    @staticmethod
    def _remove_letter_paragraph(template_content):
        pk_to_delete = template_content['action'].split('.')[1]
        template_content['letter_paragraphs'].remove(pk_to_delete)

    def post(self, request):
        template_content = get_template_content(request)
        if template_content['action'] == 'add_letter_paragraph':
            self._add_letter_paragraph(request, template_content)
        elif 'delete' in template_content['action']:
            self._remove_letter_paragraph(template_content)
        return get_order_paragraphs_page(request, template_content)
