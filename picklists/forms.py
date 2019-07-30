from django.urls import reverse_lazy

from core.builtins.custom_tags import get_string
from libraries.forms.components import Question, Form, InputType, Option, Select, BackLink

_name = Question(title='Name',
                 description='',
                 input_type=InputType.INPUT,
                 name='name')

_picklist_type = Select(name='picklist_type',
                options=[Option('Provisos', 'Provisos'),
                         Option('ECJU queries', 'ECJU queries'),
                         Option('Annual Report Summary', 'Annual Report Summary'),
                         Option('Standard Advice', 'Standard advice')],
                title='Type')

_back_link = BackLink('Back to Pick Lists', reverse_lazy('picklist_items:picklist_items'))


def add_picklist_item_form():
    return Form(title=get_string('picklist.create'),
                description='',
                questions=[
                    _name,
                    _picklist_type,
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
