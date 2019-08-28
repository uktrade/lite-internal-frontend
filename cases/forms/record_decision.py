from lite_forms.components import Form, RadioButtons, Option

from core.builtins.custom_tags import get_string


def record_decision_form():
    return Form(get_string('cases.record_decision.title'),
                [
                    RadioButtons('status',
                                 [
                                     Option('approved', get_string('cases.record_decision.grant')),
                                     Option('declined', get_string('cases.record_decision.deny'))
                                 ])
                ],
                default_button_name='Submit')
