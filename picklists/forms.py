from django.urls import reverse_lazy

from core.builtins.custom_tags import get_string
from libraries.forms.components import Question, Form, InputType, Option, Select, BackLink

_name = Question(title='Name',
                 description='',
                 input_type=InputType.INPUT,
                 name='name')

_picklist_type = Select(name='type',
                options=[Option('proviso', 'Provisos'),
                         Option('ecju_query', 'ECJU queries'),
                         Option('letter_paragraph', 'Letter Paragraph'),
                         Option('annual_report_summary', 'Annual Report Summary'),
                         Option('standard_advice', 'Standard advice'),
                         Option('footnotes', 'Footnotes')],
                title='Type')

_text = Question(title='Add text for picklist item',
                 description='',
                 input_type=InputType.TEXTAREA,
                 name='text',
                 extras={
                     'max_length': 5000,
                 })

_back_link = BackLink('Back to Pick Lists', reverse_lazy('picklist_items:picklist_items'))


def add_picklist_item_form():
    return Form(title=get_string('picklist.create'),
                description='',
                questions=[
                    _name,
                    _picklist_type,
                    _text,
                ],
                back_link=_back_link)


# def edit_picklist_item_form():
#     return Form(title='Edit Pick List Item',
#                 description='',
#                 questions=[
#                     _name,
#                     _type,
#                 ],
#                 back_link=_back_link)
