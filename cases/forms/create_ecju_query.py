from core.builtins.custom_tags import get_string
from libraries.forms.components import Form, BackLink, Question, InputType, HiddenField, Select, Button, Group


def create_ecju_queries_form(case, case_url, picklists):
    return Form(title=get_string('cases.ecju_queries.title'),
                description='',
                questions=[
                    Question(title=get_string('cases.ecju_queries.add_query.title'),
                             description=get_string('cases.ecju_queries.add_query.description'),
                             input_type=InputType.TEXTAREA,
                             name='question',
                             extras={
                                 'max_length': 5000,
                             }),
                    HiddenField(name='case', value=case),
                    Select(title='Ask a quick question', description='Select a pre-filled question',
                           name='picklist',
                           options=picklists,
                           optional=True)

                ],
                back_link=BackLink('Back to ' + get_string('cases.ecju_queries.title'), case_url)
                )
