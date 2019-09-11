from django.urls import reverse_lazy
from lite_forms.components import Form, TextInput, BackLink, HiddenField


def approve_licence_form(case_id):
    return Form(
        title='Approve',
        description='',
        questions=[
            TextInput(name='day', description='For example, 27 3 2007', title='When will the licence start?'),
            TextInput(name='month'),
            TextInput(name='year'),
            TextInput(name='duration', title='How long will it last?'),
        ],
        back_link=BackLink(url=reverse_lazy('cases:final_advice_view', kwargs={'pk': case_id}), text='back to final advice'),
    )


def refuse_licence_form(case_id):
    return Form(
        title='Refuse',
        description='',
        back_link=BackLink(url=reverse_lazy('cases:final_advice_view', kwargs={'pk': case_id}), text='back to final advice'),
    )
