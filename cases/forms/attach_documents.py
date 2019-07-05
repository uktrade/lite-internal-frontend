from core.builtins.custom_tags import get_string
from libraries.forms.components import Form, MultiFileUpload, BackLink


def attach_documents_form(case_url):
    return Form(get_string('cases.manage.attach_documents.title'),
                get_string('cases.manage.attach_documents.description'),
                [
                    MultiFileUpload('documents')
                ],
                back_link=BackLink('Back to Case Documents', case_url))
