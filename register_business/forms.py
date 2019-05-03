from libraries.forms.components import Section, Form, Question, InputType, Button, HeadingStyle, Heading, \
    HelpSection

register_business_forms = Section('', '', [

    Form(title='Register a Business',
         description='Part 1 of 3',
         questions=[
             Question(title='What\'s the business name?',
                      description='',
                      input_type=InputType.INPUT,
                      name='organisation.name'),
             Question(title='European Union registration and identification number (EORI)',
                      description='',
                      input_type=InputType.INPUT,
                      name='organisation.eori_number'),
             Question(title='Standard Industrial Classification Number (SIC)',
                      description='Classifies industries by a four-digit code.',
                      input_type=InputType.INPUT,
                      name='organisation.sic_number'),
             Question(title='UK VAT number',
                      description='9 digits long, with the first two letters indicating the'
                                  ' country code of the registered business.',
                      input_type=InputType.INPUT,
                      name='organisation.vat_number'),
             Question(title='Company registration number (CRN)',
                      description='8 numbers, or 2 letters followed by 6 numbers.',
                      input_type=InputType.INPUT,
                      name='organisation.registration_number'),
         ],
         buttons=[
             Button('Save and continue', '')
         ],
         prefix='organisation'
         ),

    Form(title='Create a default site for this organisation',
         description='Part 2 of 3',
         questions=[
             Question(title='Name of site',
                      description='',
                      input_type=InputType.INPUT,
                      name='site.name'),
             Heading('Address', HeadingStyle.M),
             Question(title='Address Line 1',
                      description='',
                      input_type=InputType.INPUT,
                      name='site.address_line_1'),
             Question(title='Address Line 2',
                      description='',
                      input_type=InputType.INPUT,
                      name='site.address_line_2',
                      optional=True),
             Question(title='Zip code',
                      description='',
                      input_type=InputType.INPUT,
                      name='site.zip_code'),
             Question(title='City',
                      description='',
                      input_type=InputType.INPUT,
                      name='site.city'),
             Question(title='State',
                      description='',
                      input_type=InputType.INPUT,
                      name='site.state'),
             Question(title='Country',
                      description='',
                      input_type=InputType.INPUT,
                      name='site.country'),
         ], buttons=[
            Button('Save and continue', '')
        ],
         prefix='site'
         ),
    Form('Create an admin for this organisation', 'Part 3 of 3', [
        Question(title='Email Address',
                 description='',
                 input_type=InputType.INPUT,
                 name='user.email'),
        Question(title='First name',
                 description='',
                 input_type=InputType.INPUT,
                 name='user.first_name'),
        Question(title='Last name',
                 description='',
                 input_type=InputType.INPUT,
                 name='user.last_name'),
        Question(title='Password',
                 description='',
                 input_type=InputType.PASSWORD,
                 name='user.password'),
        Question(title='Reenter Password',
                 description='',
                 input_type=InputType.PASSWORD,
                 name='user.reenter_password'),
    ], buttons=[
        Button('Submit', '')
    ], helpers=[
        HelpSection('Help', 'This will be the default user for this organisation.')
    ],
         prefix='user'
         ),
])
