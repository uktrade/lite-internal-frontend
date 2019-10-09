from django.urls import reverse_lazy
from lite_forms.components import Form, FormGroup, TextInput, BackLink, Checkboxes, Option, RadioButtons


def add_letter_template():
    return FormGroup(
        forms=[
            Form(title='Enter a name for your letter template',
                 description='This will make it easier to find in the future.',
                 questions=[
                     TextInput(name='name')
                 ],
                 back_link=BackLink('Back to letter templates', reverse_lazy('letter_templates:letter_templates')),
                 default_button_name='Continue'),
            Form(title='What types of case can this template apply to?',
                 description='Select all case types that apply.',
                 questions=[
                     Checkboxes(
                         name='restricted_to',
                         options=[
                             Option('application', 'Applications'),
                             Option('clc_query', 'Control List Classification Queries'),
                             Option('end_user_advisory_query', 'End User Advisory Queries'),
                         ])
                 ],
                 default_button_name='Continue'),
            Form(title='Select a layout to use for this letter template',
                 questions=[
                     RadioButtons(
                         name='layout',
                         options=[
                             Option('licence', 'Licence'),
                         ])
                 ],
                 default_button_name='Continue')
        ])
