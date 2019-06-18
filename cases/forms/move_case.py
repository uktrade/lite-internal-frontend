from core.services import get_queues
from libraries.forms.components import Form, ArrayQuestion, InputType


def move_case_form(request):
    return Form('Where do you want to move this case?',
                'Select all queues that apply.',
                [
                    ArrayQuestion('', '', InputType.CHECKBOXES, 'queues', get_queues(request, True))
                ],
                default_button_name='Submit')
