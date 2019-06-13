from libraries.forms.components import Question, Form, InputType

form = Form(title='Add Queue', description='', caption='', questions=[
    Question(title='Name',
             description='',
             input_type=InputType.INPUT,
             name='name'),
])

edit_form = Form(title='Edit Queue', description='', caption='', questions=[
    Question(title='Name',
             description='',
             input_type=InputType.INPUT,
             name='name'),
])
