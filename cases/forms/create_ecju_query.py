from core.builtins.custom_tags import get_string
from libraries.forms.components import Form, BackLink, Question, InputType, Select, TextArea


def choose_ecju_query_type_form(case_url, picklists):
    return Form(title=get_string('cases.ecju_queries.add_query.dropdown_title'),
                description='',
                questions=[
                    Select(title='',
                           description=get_string('cases.ecju_queries.add_query.dropdown_description'),
                           name='picklist',
                           options=picklists,
                           include_default_select=False),
                    Question(title='',
                             description='',
                             input_type=InputType.HIDDEN,
                             name='form_ecju_query_type_select')
                ],
                back_link=BackLink('Back to ' + get_string('cases.ecju_queries.title'), case_url),
                default_button_name='Continue'
                )


def create_ecju_query_form(choose_picklist_url):
    return Form(title=get_string('cases.ecju_queries.add_query.title'),
                description='',
                questions=[
                    TextArea(title='',
                             description=get_string('cases.ecju_queries.add_query.description'),
                             name='question',
                             extras={
                                 'max_length': 5000,
                             }),
                    Question(title='',
                             description='',
                             input_type=InputType.HIDDEN,
                             name='form_ecju_query_write_or_edit_question'),
                ],
                back_link=BackLink('Back to ' + get_string('cases.ecju_queries.add_query.dropdown_title'),
                                   choose_picklist_url),
                default_button_name='Send'
                )
