from libraries.forms.components import Question, Form, InputType, Option, Select


def add_flag_form():
    return Form(title='Add Flag', description='', questions=[
        Question(title='Name',
                 description='',
                 input_type=InputType.INPUT,
                 name='name'),
        Select(name='level',
               options=[Option('Case', 'Case'),
                        Option('Organisation', 'Organisation'),
                        Option('Destination', 'Destination'),
                        Option('Good', 'Good')],
               title='Level', )
    ])


def edit_flag_form():
    return Form(title='Edit Flag', description='', caption='', questions=[
        Question(title='Name',
                 description='',
                 input_type=InputType.INPUT,
                 name='name'),
        Select(name='level',
               options=[Option('Case', 'Case'),
                        Option('Organisation', 'Organisation'),
                        Option('Destination', 'Destination'),
                        Option('Good', 'Good')],
               title='Level', )
    ])
