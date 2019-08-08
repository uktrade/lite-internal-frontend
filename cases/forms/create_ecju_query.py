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
                ],
                back_link=BackLink('Back to ' + get_string('cases.ecju_queries.add_query.picklist_title'),
                                   choose_picklist_url)
                )


def choose_ecju_query_type_form(case_url, picklists):
    return Form(title=get_string('cases.ecju_queries.add_query.picklist_title'),
                description='',
                questions=[
                    Select(title='',
                           description='Select a pre-filled question',
                           name='picklist',
                           options=picklists,
                           optional=True)

                ],
                back_link=BackLink('Back to ' + get_string('cases.ecju_queries.title'), case_url)
                )
