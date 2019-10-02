from django.urls import reverse_lazy
from lite_forms.components import Form, FormGroup, TextInput, BackLink


def add_letter_template():
    return FormGroup([
        Form(title='Enter a name for your letter template',
             description='This will make it easier to find your template in the future',
             questions=[
                 TextInput(name='name')
             ],
             back_link=BackLink('Back to letter templates', reverse_lazy('letter_templates:letter_templates')),
             default_button_name='Continue')
    ], show_progress_indicators=True)
