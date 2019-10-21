from django.shortcuts import render
from django.views.generic import TemplateView

from cases.services import get_case, get_case_documents
from core.builtins.custom_tags import get_string


class GenerateDocuments(TemplateView):
    def get(self, request, **kwargs):
        """
        List all documents belonging to a case
        """
        case_id = str(kwargs['pk'])
        case = get_case(request, case_id)
        # case_documents, _ = get_case_documents(request, case_id)

        context = {
            'title': get_string('cases.generate_documents.title'),
            'case': case,
            # 'case_documents': case_documents['documents'],
        }
        return render(request, 'cases/case/documents.html', context)
