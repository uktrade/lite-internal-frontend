from django.urls import reverse_lazy

from libraries.forms.components import Form, Option, RadioButtons, HelpSection, BackLink, HiddenField


def advice_recommendation_form(case_id):
    return Form('What do you advise?',
                'You can advise to:',
                [
                    RadioButtons('type', [
                        Option('approve', 'Grant the licence ', 'Description goes here'),
                        Option('proviso', 'Add a proviso', 'Description goes here'),
                        Option('refuse', 'Refuse the licence', 'Description goes here'),
                        Option('nlr', 'Tell the applicant they do not need a licence', 'Description goes here'),
                        Option('na', 'Ask the applicant a question', show_or=True),
                    ]),
                ],
                default_button_name='Continue',
                helpers=[
                    HelpSection('Help', 'Help goes here')
                ],
                back_link=BackLink('Back to advice'),
                post_url=reverse_lazy('cases:give_advice', kwargs={'pk': case_id}))
