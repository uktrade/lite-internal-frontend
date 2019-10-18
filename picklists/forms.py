from django.urls import reverse_lazy
from lite_forms.components import TextInput, Select, Option, TextArea, BackLink, Form, Button, MarkdownArea
from lite_forms.styles import ButtonStyle

from core.builtins.custom_tags import get_string

_name = TextInput(title='Name',
                  name='name')

_picklist_type = Select(name='type',
                        options=[Option('proviso', 'Proviso'),
                                 Option('ecju_query', 'ECJU Query'),
                                 Option('letter_paragraph', 'Letter Paragraph'),
                                 Option('report_summary', 'Report Summary'),
                                 Option('standard_advice', 'Standard Advice'),
                                 Option('footnotes', 'Footnote')],
                        title='Type')

_text = TextArea(title='Add text for picklist item',
                 name='text',
                 extras={
                     'max_length': 5000,
                 })

_context_variables = [
    {'key': 'application.name', 'value': 'Application 1234'},
    {'key': 'organisation.name', 'value': 'My Organisation LTD.'},
    {'key': 'application.recipient', 'value': 'John Smith'}
]

_paragraph = MarkdownArea(title='Add text for paragraph',
                          name='text',
                          variables=_context_variables,
                          extras={
                              'max_length': 5000,
                          })

_back_link = BackLink('Back to picklists', '#')


def add_picklist_item_form(request):
    picklist_type = request.GET.get('type')
    paragraph = False
    if picklist_type.lower() == 'letter_paragraph':
        paragraph = True

    questions = [_name, _picklist_type]
    if paragraph:
        questions.append(_paragraph)
    else:
        questions.append(_text)

    return Form(title=get_string('picklist.create'),
                questions=questions,
                back_link=_back_link,
                default_button_name='Save')


def edit_picklist_item_form(picklist_item):
    deactivate_button = Button(value='Deactivate',
                               action='',
                               style=ButtonStyle.WARNING,
                               link=reverse_lazy('picklists:deactivate',
                                                 kwargs={'pk': picklist_item['id']}),
                               float_right=True)
    activate_button = Button(value='Reactivate',
                             action='',
                             style=ButtonStyle.SECONDARY,
                             link=reverse_lazy('picklists:reactivate',
                                               kwargs={'pk': picklist_item['id']}),
                             float_right=True)

    if picklist_item['status']['key'] == 'deactivated':
        button = activate_button
    else:
        button = deactivate_button

    return Form(title=get_string('picklist.edit'),
                questions=[
                    _name,
                    _picklist_type,
                    _text,
                ],
                back_link=BackLink('Back to ' + picklist_item['name'],
                                   reverse_lazy('picklists:picklist_item',
                                                kwargs={'pk': picklist_item['id']})),
                buttons=[
                    Button('Save', 'submit', ButtonStyle.DEFAULT),
                    button,
                ])


def deactivate_picklist_item(picklist_item):
    return Form(title='Are you sure you want to deactivate ' + picklist_item['name'] + '?',
                description='You can always reactivate it later if need be.',
                questions=[],
                back_link=BackLink('Back',
                                   reverse_lazy('picklists:edit',
                                                kwargs={'pk': picklist_item['id']})),
                buttons=[
                    Button('Deactivate', 'submit', ButtonStyle.WARNING),
                    Button('Cancel',
                           'cancel',
                           ButtonStyle.SECONDARY,
                           reverse_lazy('picklists:edit',
                                        kwargs={'pk': picklist_item['id']}))
                ])


def reactivate_picklist_item(picklist_item):
    return Form(title='Are you sure you want to reactivate ' + picklist_item['name'] + '?',
                description='You can always deactivate it later if need be.',
                questions=[],
                back_link=BackLink('Back',
                                   reverse_lazy('picklists:edit',
                                                kwargs={'pk': picklist_item['id']})),
                buttons=[
                    Button('Reactivate', 'submit', ButtonStyle.DEFAULT),
                    Button('Cancel',
                           'cancel',
                           ButtonStyle.SECONDARY,
                           reverse_lazy('picklists:edit',
                                        kwargs={'pk': picklist_item['id']}))
                ])
