import os

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import engines
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from faker import Faker
from lite_forms.helpers import flatten_data
from weasyprint import HTML, CSS

from cases.documents.generator import PdfGenerator
from cases.documents.services import get_letter_templates, get_letter_template
from cases.services import get_case
from conf import settings


class PickATemplate(TemplateView):

    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case = get_case(request, case_id)

        context = {
            'title': 'Flags',
            'case': case,
            'templates': get_letter_templates(request),
            'show_error': request.GET.get('show_error'),
        }
        return render(request, 'documents/select_a_template.html', context)


def fake_items():
    fake = Faker()
    for item in range(0, 10):
        yield {
            "item": item,
            "description": fake.sentence(),
            "control_list": fake.pystr(min_chars=3, max_chars=7),
            "value": fake.pydecimal(left_digits=7, right_digits=2, min_value=0),
            "quantity": fake.pyint(min_value=0, max_value=999),
        }
    

class CreateDocument(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        case_id = str(kwargs['pk'])
        case = get_case(request, case_id)
        template = request.GET.get('template')

        if not template:
            return redirect(reverse_lazy('cases:documents:pick_a_template', kwargs={'pk': case_id}) + '?show_error=True')

        template_data = get_letter_template(request, template)

        django_engine = engines['django']
        template = django_engine.from_string(open(os.path.join(settings.LETTER_TEMPLATES_DIRECTORY, f'{template}.html'), 'r').read())
        letter_context = {
            'applicant': case.get('query').get('organisation'),
            'query': case.get('query'),
            'content': request.POST.get('content', ''),
        }

        letter_context["craigs_items"] = fake_items()
        
        preview = template.render(letter_context)

        flattened_letter_context = flatten_data(letter_context)

        for key, value in flattened_letter_context.items():
            if not value:
                flattened_letter_context[key] = ''

        context = {
            'title': 'Flags',
            'preview': preview,
            'content': letter_context.pop('content'),
            'letter_context': letter_context,
            'flattened_letter_context': flattened_letter_context,
            'template_data': template_data,
        }

        if request.POST.get('action') == 'print':
            # weasyprint
            pdf = PdfGenerator(preview, base_url=request.build_absolute_uri())
            pdf.render_pdf('/tmp/mypdf.pdf')

            # pdfkit
            # pdfkit.from_string('Hello!', 'out.pdf')

            fs = FileSystemStorage('/tmp')
            with fs.open('mypdf.pdf') as pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
                return response
        else:
            return render(request, 'documents/document_generator.html', context)


class Preview(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        case_id = str(kwargs['pk'])
        case = get_case(request, case_id)
        template = request.GET.get('template')

        django_engine = engines['django']
        template = django_engine.from_string(open(os.path.join(settings.LETTER_TEMPLATES_DIRECTORY, f'{template}.html'), 'r').read())
        letter_context = {
            'applicant': case.get('query').get('organisation'),
            'query': case.get('query'),
            'content': request.POST.get('content', ''),
        }
        preview = template.render(letter_context)

        html = HTML(string=preview)
        html.write_pdf(target='/tmp/mypdf.pdf')
        fs = FileSystemStorage('/tmp')
        with fs.open('mypdf.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
            return response


class Help(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'documents/help.html')
