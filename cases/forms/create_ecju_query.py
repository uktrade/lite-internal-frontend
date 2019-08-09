from core.builtins.custom_tags import get_string
from libraries.forms.components import Form, BackLink, Select, TextArea, RadioButtons, Option, HiddenField


def choose_ecju_query_type_form(case_url, picklists):
    return Form(title=get_string('cases.ecju_queries.add_query.dropdown_title'),
                description='',
                questions=[
                    Select(title='',
                           description=get_string('cases.ecju_queries.add_query.dropdown_description'),
                           name='picklist',
                           options=picklists,
                           include_default_select=False),
                    HiddenField(name='form_name', value='ecju_query_type_select'),
                ],
                back_link=BackLink('Back to ' + get_string('cases.ecju_queries.title'), case_url),
                default_button_name='Continue'
                )


def create_ecju_query_write_or_edit_form(choose_picklist_url):
    return Form(title=get_string('cases.ecju_queries.add_query.title'),
                description='',
                questions=[
                    TextArea(title='',
                             description=get_string('cases.ecju_queries.add_query.description'),
                             name='question',
                             extras={
                                 'max_length': 5000,
                             }),
                    HiddenField(name='form_name', value='ecju_query_write_or_edit_question'),
                ],
                back_link=BackLink('Back to ' + get_string('cases.ecju_queries.add_query.dropdown_title'),
                                   choose_picklist_url),
                default_button_name='Continue'
                )


def create_ecju_create_confirmation_form():
    return Form(title='Do you want to send your question?',
                description='',
                questions=[
                     RadioButtons(title='',
                                  name='ecju_query_confirmation',
                                  description='',
                                  options=[
                                      Option(key='yes',
                                             value='Yes, send the question'),
                                      Option(key='no',
                                             value='No, edit the question')
                                  ],
                                  classes=['govuk-radios--inline']),
                     HiddenField(name='form_name', value='ecju_query_create_confirmation'),
                ],
                back_link=BackLink('Back to ' + get_string('cases.ecju_queries.add_query.title'), '#'),
                default_button_name='Continue'
                )
