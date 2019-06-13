from queues.services import get_queue, get_queues, \
    post_queues, update_queue
from queues import forms

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class QueuesList(TemplateView):

    def get(self, request, **kwargs):
        data, status_code = get_queues(request)
        context = {
            'data': data,
            'title': 'Queues',
        }
        return render(request, 'queues/index.html', context)


class AddQueue(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'title': 'Add Queue',
            'page': forms.form,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data, status_code = post_queues(request, request.POST)

        if status_code == 400:
            context = {
                'title': 'Add Queue',
                'page': forms.form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('queues:queues'))


class EditQueue(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_queue(request, str(kwargs['pk']))
        context = {
            'data': data.get('queue'),
            'title': 'Edit Queue',
            'page': forms.edit_form,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data, status_code = update_queue(request, str(kwargs['pk']), request.POST)
        if status_code == 400:
            context = {
                'title': 'Add Queue',
                'page': forms.form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('queues:queues'))
