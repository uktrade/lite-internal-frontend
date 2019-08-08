from libraries.forms.components import Form, Option, RadioButtons, HelpSection


def advice_recommendation_form():
    return Form('Decision',
                'Description goes here',
                [
                    RadioButtons('type', [
                        Option('approve', 'Approve', 'Description goes here'),
                        Option('proviso', 'Proviso', 'Description goes here'),
                        Option('refuse', 'Refuse', 'Description goes here'),
                        Option('nlr', 'No licence required', 'Description goes here'),
                        Option('na', 'Not applicable', show_or=True),
                    ]),
                ],
                default_button_name='Continue',
                helpers=[
                    HelpSection('Help', 'Help goes here')
                ])
