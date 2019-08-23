import logging
import uuid
import json
import time
from django.shortcuts import redirect
from django.urls import resolve
from s3chunkuploader.file_handler import UploadFailed
from core.builtins.custom_tags import get_string
from libraries.forms.generators import error_page


class ProtectAllViewsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if resolve(request.path).app_name != 'authbroker_client' and not request.user.is_authenticated:
            return redirect('authbroker_client:login')

        response = self.get_response(request)

        return response


class UploadFailedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if not isinstance(exception, UploadFailed):
            return None
        return error_page(request, get_string('cases.manage.documents.attach_documents.file_too_large'))


class LoggingMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        request.correlation = uuid.uuid4().hex
        data = {
            "message": "liteolog internal",
            "corrID": request.correlation,
            "method": request.method,
            "type": "http request",
            "url": request.path,
        }
        logging.info(data)
        response = self.get_response(request)
        data['type'] = "http response"
        data['elapsed'] = time.time() - start
        logging.info(data)
        return response
