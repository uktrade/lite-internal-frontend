from form.models import Section, Form, Question, InputType, ArrayQuestion, Option

section1 = Section("Register a Business", "", [
    Form("Form Title", "Form Description", [
        Question(title='What\'s your business name?',
                 description='',
                 input_type=InputType.INPUT,
                 name='name'),
        Question(title='Test field',
                 description='',
                 input_type=InputType.INPUT,
                 name='name'),
        Question(title='more test fields',
                 description='',
                 input_type=InputType.INPUT,
                 name='name'),
        Question(title='test',
                 description='',
                 input_type=InputType.INPUT,
                 name='name'),
        Question(title='further test',
                 description='',
                 input_type=InputType.INPUT,
                 name='name'),
    ]),
])
