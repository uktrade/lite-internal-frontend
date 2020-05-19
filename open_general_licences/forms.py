from lite_forms.components import Form, TreeView, FormGroup, TextArea, RadioButtons, Option


def test_form(control_list_entries):
    return Form(
        title="Select control list entries", questions=[TreeView(data=control_list_entries)]
    )


def new_open_general_licence_forms(control_list_entries):
    return FormGroup([
        Form(title="Select the type of open general licence you want to add",
             questions=[
                RadioButtons(name="type",
                             options=[
                                 Option("open_general_export_licence", "Open general export licence (OGEL)"),
                                 Option("open_general_trade_control_licence", "Open general trade control licence (OGTCL)"),
                                 Option("open_general_transhipment_licence", "Open general transhipment licence (OGTL)")
                             ])
             ]),
        Form(title="Name the OGL",
             questions=[
                TextArea(name="name")
             ]),
        Form(title="Select countries",
             questions=[
                TextArea(name="name")
             ]),
        test_form(control_list_entries),
        Form(title="Website",
             questions=[
                TextArea(name="name")
             ]),
        Form(title="Describe the OGL",
             questions=[
                TextArea(name="name")
             ]),
        Form(title="Does the OGL require registration",
             questions=[
                TextArea(name="name")
             ]),
    ])

