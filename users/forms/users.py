from core.builtins.custom_tags import get_string
from libraries.forms.components import Question, Form, InputType, ArrayQuestion, Select
from users.services import get_roles


def add_user_form(request, teams):
    return Form(title=get_string('users.invite'), description='', questions=[
        Question(title='What\'s the user\'s email?',
                 description='',
                 input_type=InputType.INPUT,
                 name='email'),
        ArrayQuestion(title='What team will the user belong to?',
                      description='',
                      input_type=InputType.SELECT,
                      name='team',
                      data=teams),
        Select(name='role',
               options=get_roles(request, True),
               title='What role should this user have?'),
    ])


def edit_user_form(request, teams):
    return Form(title='Edit User', description='', caption='', questions=[
        Question(title='Email',
                 description='',
                 input_type=InputType.INPUT,
                 name='email'),
        ArrayQuestion(title='Team',
                      description='',
                      input_type=InputType.SELECT,
                      name='team',
                      data=teams),
        Select(name='role',
               options=get_roles(request, True),
               title='What role should this user have?'),
    ])
