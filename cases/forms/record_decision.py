from libraries.forms.components import Form, InputType, ArrayQuestion, Option


def record_decision_form():
    return Form('Do you want to grant or deny this application?',
                '',
                [
                    ArrayQuestion('',
                                  '',
                                  InputType.RADIOBUTTONS,
                                  'status',
                                  [
                                      Option('approved', 'Grant application'),
                                      Option('declined', 'Deny application')
                                  ])
                ],
                default_button_name='Submit')
