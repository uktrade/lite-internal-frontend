import boto3
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from s3chunkuploader.file_handler import S3FileUploadHandler

from cases.forms.attach_documents import attach_documents_form
from cases.forms.denial_reasons import denial_reasons_form
from cases.forms.move_case import move_case_form
from cases.forms.record_decision import record_decision_form
from cases.services import get_case, post_case_notes, put_applications, get_activity, put_case, post_case_documents
from conf.settings import env, AWS_STORAGE_BUCKET_NAME
from core.services import get_queue, get_queues
from libraries.forms.generators import error_page, form_page
from libraries.forms.submitters import submit_single_form
from queues.services import get_queue_case_assignments


class Cases(TemplateView):
    def get(self, request, **kwargs):
        """
        Show a list of cases
        """
        queue_id = request.GET.get('queue')

        # If a queue id is not provided, use the default queue
        if not queue_id:
            queue_id = '00000000-0000-0000-0000-000000000001'

        queues, status_code = get_queues(request)
        queue, status_code = get_queue(request, queue_id)
        case_assignments, status_code = get_queue_case_assignments(request, queue_id)

        context = {
            'queues': queues,
            'queue_id': queue_id,
            'data': queue,
            'title': queue.get('queue').get('name'),
            'case_assignments': case_assignments['case_assignments'],
        }
        return render(request, 'cases/index.html', context)

    def post(self, request, **kwargs):
        """
        Assign users depending on what cases were selected
        """
        queue_id = request.GET.get('queue')

        if not queue_id:
            queue_id = '00000000-0000-0000-0000-000000000001'

        return redirect(reverse('queues:case_assignments', kwargs={'pk': queue_id}) + '?cases=' + ','.join(request.POST.getlist('cases')))


class ViewCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)
        activity, status_code = get_activity(request, case_id)

        context = {
            'data': case,
            'title': case.get('case').get('application').get('name'),
            'activity': activity.get('activity'),
        }
        return render(request, 'cases/case/index.html', context)

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        response, status_code = post_case_notes(request, case_id, request.POST)

        if status_code != 201:
            error = response.get('errors').get('text')[0]
            error = error.replace('This field', 'Case note')
            error = error.replace('this field', 'the case note')  # TODO: Move to API
            return error_page(request, error)

        return redirect('/cases/' + case_id + '#case_notes')


class ManageCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)
        context = {
            'data': case,
            'title': 'Manage ' + case.get('case').get('application').get('name'),
        }
        return render(request, 'cases/manage.html', context)

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)
        application_id = case.get('case').get('application').get('id')

        # PUT form data
        data, status_code = put_applications(request, application_id, request.POST)

        if 'errors' in data:
            return redirect('/cases/' + case_id + '/manage')

        return redirect('/cases/' + case_id)


class DecideCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)

        if case['case']['application']['status'] == 'approved':
            data = {
                'status': case['case']['application']['status']
            }
        elif case['case']['application']['status'] == 'under_final_review':
            data = {
                'status': 'declined'
            }
        else:
            data = {}

        return form_page(request, record_decision_form(), data=data)

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)

        case_id = case.get('case').get('id')
        application_id = case.get('case').get('application').get('id')

        if not request.POST.get('status'):
            return form_page(request, record_decision_form(), errors={
                'status': ['Select an option']
            })

        if request.POST.get('status') == 'declined':
            return redirect(reverse('cases:deny', kwargs={'pk': case_id}))

        # PUT form data
        put_applications(request, application_id, request.POST)

        return redirect('/cases/' + case_id)


class DenyCase(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, denial_reasons_form())

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)

        application_id = case['case']['application']['id']

        data = {
            'reasons': request.POST.getlist('reasons'),
            'reason_details': request.POST['reason_details'],
            'status': 'under_final_review',
        }

        response, data = submit_single_form(request,
                                            denial_reasons_form(),
                                            put_applications,
                                            pk=application_id,
                                            override_data=data)

        if response:
            return response

        # If there is no response (no forms left to go through), go to the case page
        return redirect(reverse('cases:case', kwargs={'pk': case_id}))


class MoveCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)

        return form_page(request, move_case_form(request), data=case['case'])

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])

        data = {
            'queues': request.POST.getlist('queues'),
        }

        response, data = submit_single_form(request,
                                            move_case_form(request),
                                            put_case,
                                            pk=case_id,
                                            override_data=data)

        if response:
            return response

        # If there is no response (no forms left to go through), go to the case page
        return redirect(reverse('cases:case', kwargs={'pk': case_id}))


class AttachDocuments(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        get_case(request, case_id)

        form = attach_documents_form()

        s3 = boto3.resource('s3')
        my_bucket = s3.Bucket(AWS_STORAGE_BUCKET_NAME)
        for my_bucket_object in my_bucket.objects.all():
            form.title += my_bucket_object.key

        return form_page(request, form)

    def post(self, request, **kwargs):
        # self.request.upload_handlers.insert(0, S3FileUploadHandler(request))

        case_id = str(kwargs['pk'])

        data = {
            'name': 'test.pdf'
        }

        case_document, status_code = post_case_documents(request, case_id, data)

        print(case_document)

        return HttpResponse('yeet')
