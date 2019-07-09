from core.builtins.custom_tags import get_string
from libraries.forms.components import Form, MultiFileUpload, BackLink, Question, InputType


def attach_documents_form(case_url):
    return Form(get_string('cases.manage.documents.attach_documents.title'),
                get_string('cases.manage.documents.attach_documents.description'),
                [
                    MultiFileUpload('documents'),
                    Question(title='Description of good',
                             description='This can make it easier to find your good later',
                             input_type=InputType.TEXTAREA,
                             name='description',
                             extras={
                                 'max_length': 280,
                             })
                ],
                back_link=BackLink('Back to Case Documents', case_url))
