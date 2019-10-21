from django.urls import reverse_lazy
from lite_forms.components import TextInput, TextArea, BackLink, Form, Button, MarkdownArea, HiddenField
from lite_forms.helpers import conditional
from lite_forms.styles import ButtonStyle

from core.builtins.custom_tags import get_string

_name = TextInput(title='Name',
                  name='name')

_text = TextArea(title='Text',
                 name='text',
                 extras={
                     'max_length': 5000,
                 })

_context_variables = [
    {'key': 'application.name', 'value': 'Application 1234'},
    {'key': 'organisation.name', 'value': 'My Organisation LTD.'},
    {'key': 'application.recipient', 'value': 'John Smith'}
]

_paragraph = MarkdownArea(title='Paragraph Text',
                          name='text',
                          variables=_context_variables,
                          extras={
                              'max_length': 5000,
                          })


def add_picklist_item_form(request):
    picklist_type = request.GET.get('type')

    return Form(title=get_string(f'picklist.create.{picklist_type}'),
                questions=[
                    _name,
                    HiddenField('type', picklist_type),
                    conditional(picklist_type == 'letter_paragraph', _paragraph, _text)
                ],
                back_link=BackLink('Back to picklists', reverse_lazy('picklists:picklists') + f'?type={picklist_type}'),
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

    return Form(title='Edit ' + picklist_item['name'],
                questions=[
                    _name,
                    conditional(picklist_item['type']['key'] == 'letter_paragraph', _paragraph, _text),
                ],
                back_link=BackLink('Back to ' + picklist_item['name'],
                                   reverse_lazy('picklists:picklist_item',
                                                kwargs={'pk': picklist_item['id']})),
                buttons=[
                    Button('Save', 'submit', ButtonStyle.DEFAULT),
                    conditional(picklist_item['status']['key'] == 'deactivated', activate_button, deactivate_button),
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
