from django.urls import reverse_lazy

from libraries.forms.components import Form, Option, RadioButtons, BackLink


def advice_recommendation_form(case_id):
    return Form('What do you advise?',
                'You can advise to:',
                [
                    RadioButtons('type', [
                        Option('approve', 'Grant the licence'),
                        Option('proviso', 'Add a proviso'),
                        Option('refuse', 'Refuse the licence'),
                        Option('no_licence_required', 'Tell the applicant they do not need a licence'),
                        Option('not_applicable', 'Ask the applicant a question', show_or=True),
                    ]),
                ],
                default_button_name='Continue',
                back_link=BackLink('Back to advice'),
                post_url=reverse_lazy('cases:give_advice', kwargs={'pk': case_id}))
