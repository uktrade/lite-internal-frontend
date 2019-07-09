from django.urls import reverse_lazy

from core.builtins.custom_tags import get_string
from libraries.forms.components import Question, Form, InputType, Checkboxes, Option, \
    BackLink


def add_role():
    return Form(title=get_string('roles.add.title'),
                description=get_string('roles.add.description'),
                questions=[
            Question(title='What do you want to call the role?',
                     description='',
                     input_type=InputType.INPUT,
                     name='name'),
            Checkboxes(name='permissions',
                       options=[
                           Option('', 'Banana'),
                           Option('', 'Banana'),
                           Option('', 'Banana'),
                           Option('', 'Banana'),
                           Option('', 'Banana'),
                       ],
                       title='What permissions should this role have?',
                       description='Select as many or as few as you want'),
        ],
                back_link=BackLink('Back to Roles', reverse_lazy('users:roles')))
