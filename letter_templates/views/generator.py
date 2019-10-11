from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_paged_form

from letter_templates import helpers
from letter_templates.forms import add_letter_template
from letter_templates.services import get_letter_paragraphs, post_letter_templates
from picklists.services import get_picklists


def generate_preview(request, letter_paragraphs, name, layout, restricted_to):
    letter_paragraphs = get_letter_paragraphs(request, letter_paragraphs)

    preview = helpers.generate_preview(layout, letter_paragraphs)

    return render(request, 'letter_templates/preview.html', {
        'preview': preview,
        'name': name,
        'layout': layout,
        'restricted_to': restricted_to,
        'letter_paragraphs': letter_paragraphs
    })


def generate_generator(request, letter_paragraphs, name, layout, restricted_to):
    letter_paragraphs = get_letter_paragraphs(request, letter_paragraphs)
    return render(request, 'letter_templates/generator.html', {'letter_paragraphs': letter_paragraphs,
                                                               'name': name,
                                                               'layout': layout,
                                                               'restricted_to': restricted_to})


class Add(TemplateView):

    def get(self, request, **kwargs):
        return form_page(request, add_letter_template().forms[0])

    def post(self, request, **kwargs):
        response, _ = submit_paged_form(request, add_letter_template(), post_letter_templates)

        if response:
            return response

        return generate_generator(request,
                                  letter_paragraphs=[],
                                  name=request.POST.get('name'),
                                  layout=request.POST.get('layout'),
                                  restricted_to=request.POST.getlist('restricted_to'))


class LetterParagraphs(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        data = request.POST.copy()
        name = data.get('name')
        layout = data.get('layout')
        restricted_to = data.getlist('restricted_to')
        action = data.get('action')
        existing_letter_paragraphs = data.getlist('letter_paragraphs')

        if action == 'add_letter_paragraph':
            all_letter_paragraphs = get_picklists(request, 'letter_paragraph')
            context = {
                'name': name,
                'layout': layout,
                'restricted_to': restricted_to,
                'letter_paragraphs': [x for x in all_letter_paragraphs['picklist_items'] if
                                      x['id'] not in existing_letter_paragraphs],
                'existing_letter_paragraphs': existing_letter_paragraphs
            }
            return render(request, 'letter_templates/letter_paragraphs.html', context)
        elif action == 'preview':
            return generate_preview(request,
                                    existing_letter_paragraphs,
                                    name=name,
                                    layout=layout,
                                    restricted_to=restricted_to)
        elif 'delete' in action:
            pk_to_delete = action.split('.')[1]
            existing_letter_paragraphs.remove(pk_to_delete)

        return generate_generator(request,
                                  letter_paragraphs=existing_letter_paragraphs,
                                  name=name,
                                  layout=layout,
                                  restricted_to=restricted_to)


class Preview(TemplateView):
    def post(self, request, **kwargs):
        post_letter_templates(request, request.POST)

        messages.success(request, 'The letter template was created successfully')
        return redirect('letter_templates:letter_templates')
