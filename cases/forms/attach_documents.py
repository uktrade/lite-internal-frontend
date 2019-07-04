from core.builtins.custom_tags import get_string
from libraries.forms.components import Form, MultiFileUpload


def attach_documents_form():
    return Form(get_string('cases.manage.attach_documents.title'),
                get_string('cases.manage.attach_documents.description'),
                [
                    MultiFileUpload('documents')
                ])
