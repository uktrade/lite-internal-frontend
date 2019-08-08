from core.builtins.custom_tags import get_string
from libraries.forms.components import Form, BackLink, Question, InputType, Select


def create_ecju_query_form(choose_picklist_url):
    return Form(title=get_string('cases.ecju_queries.add_query.title'),
                description='',
                questions=[
                    Question(title='',
                             description=get_string('cases.ecju_queries.add_query.description'),
                             input_type=InputType.TEXTAREA,
                             name='question',
                             extras={
                                 'max_length': 5000,
                             }),
                    Question(title='',
                             description='',
                             input_type=InputType.HIDDEN,
                             name='form_add_ecju_query'),
                ],
                back_link=BackLink('Back to ' + get_string('cases.ecju_queries.add_query.picklist_title'),
                                   choose_picklist_url)
                )


def choose_ecju_query_type_form(case_url, picklists):
    return Form(title=get_string('cases.ecju_queries.add_query.picklist_title'),
                description='',
                questions=[
                    Select(title='',
                           description='You can:<ul>'
                                       '<li>write a new question</li>'
                                       '<li>choose a question from a list</li></ul>',
                           name='picklist',
                           options=picklists),
                    Question(title='',
                             description='',
                             input_type=InputType.HIDDEN,
                             name='form_ecju_query_type_select')
                ],
                back_link=BackLink('Back to ' + get_string('cases.ecju_queries.title'), case_url)
                )
