from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_single_form

from letter_templates import helpers
from letter_templates.forms import edit_letter_template
from letter_templates.services import get_letter_paragraphs, get_letter_templates, get_letter_template, \
    put_letter_template
from picklists.services import get_picklists


class LetterTemplatesList(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'letter_templates': get_letter_templates(request)
        }
        return render(request, 'letter_templates/letter_templates.html', context)


class LetterTemplateDetail(TemplateView):
    def get(self, request, **kwargs):
        letter_template_id = str(kwargs['pk'])
        letter_template = get_letter_template(request, letter_template_id)
        letter_paragraphs = get_letter_paragraphs(request, letter_template['letter_paragraphs'])

        context = {
            'letter_template': letter_template,
            'preview': helpers.generate_preview(letter_template['layout']['id'], letter_paragraphs)
        }
        return render(request, 'letter_templates/letter_template.html', context)


class LetterTemplateEdit(TemplateView):
    def get(self, request, **kwargs):
        letter_template_id = str(kwargs['pk'])
        letter_template = get_letter_template(request, letter_template_id)

        # Manipulate data from API to make it work with forms
        existing_form_data = letter_template
        existing_form_data['restricted_to'] = [x['key'] for x in existing_form_data['restricted_to']]

        return form_page(request, edit_letter_template(letter_template), data=existing_form_data)

    def post(self, request, **kwargs):
        letter_template_id = str(kwargs['pk'])
        letter_template = get_letter_template(request, letter_template_id)

        # Override case restrictions to use getlist
        override_data = request.POST.copy()
        override_data['restricted_to'] = override_data.getlist('restricted_to')

        response, _ = submit_single_form(request,
                                         edit_letter_template(letter_template),
                                         put_letter_template,
                                         pk=letter_template_id,
                                         override_data=override_data)

        if response:
            return response

        return redirect(reverse('letter_templates:letter_template', kwargs={'pk': letter_template_id}))


class LetterTemplateEditLetterParagraphs(TemplateView):
    def get(self, request, **kwargs):
        letter_template_id = str(kwargs['pk'])
        letter_template = get_letter_template(request, letter_template_id)

        if kwargs.get('override_paragraphs'):
            letter_template['letter_paragraphs'] = kwargs.get('override_paragraphs')

        letter_paragraphs = get_letter_paragraphs(request, letter_template['letter_paragraphs'])
        letter_paragraphs = self.sort_letter_paragraphs(letter_paragraphs, letter_template['letter_paragraphs'])

        context = {
            'letter_template': letter_template,
            'letter_paragraphs': letter_paragraphs
        }
        return render(request, 'letter_templates/edit_letter_paragraphs.html', context)

    @staticmethod
    def sort_letter_paragraphs(paragraphs, ids):
        """Order a list of letter paragraphs in the same order as a list of IDs."""
        paragraphs_by_id = {p["id"]: p for p in paragraphs}
        return [paragraphs_by_id[id] for id in ids if id in paragraphs_by_id]

    def post(self, request, **kwargs):
        letter_template_id = str(kwargs['pk'])
        action = request.POST.get('action')
        existing_letter_paragraphs = request.POST.getlist('letter_paragraphs')

        if action == 'add_letter_paragraph':
            all_letter_paragraphs = get_picklists(request, 'letter_paragraph')

            context = {
                'letter_paragraphs': [x for x in all_letter_paragraphs['picklist_items'] if
                                      x['id'] not in existing_letter_paragraphs],
                'existing_letter_paragraphs': existing_letter_paragraphs
            }
            return render(request, 'letter_templates/letter_paragraphs.html', context)

        elif action == 'return_to_preview':
            return self.get(request, override_paragraphs=request.POST.getlist('letter_paragraphs'), **kwargs)

        elif 'delete' in action:
            pk_to_delete = action.split('.')[1]
            existing_letter_paragraphs.remove(pk_to_delete)

            return self.get(request, override_paragraphs=existing_letter_paragraphs, **kwargs)

        put_letter_template(request, letter_template_id,
                            {'letter_paragraphs': request.POST.getlist('letter_paragraphs')})
        return redirect(reverse('letter_templates:letter_template', kwargs={'pk': letter_template_id}))
