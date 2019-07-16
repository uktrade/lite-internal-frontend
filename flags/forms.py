from libraries.forms.components import Question, Form, InputType, Option, Select

_name = Question(title='Name',
                 description='',
                 input_type=InputType.INPUT,
                 name='name')

_level = Select(name='level',
                options=[Option('Case', 'Case'),
                         Option('Organisation', 'Organisation'),
                         Option('Destination', 'Destination'),
                         Option('Good', 'Good')],
                title='Level')


def add_flag_form():
    return Form(title='Add Flag', description='', questions=[
        _name,
        _level,
    ])


def edit_flag_form():
    return Form(title='Edit Flag', description='', questions=[
        _name,
        _level,
    ])
