from libraries.forms.components import Form, MultiFileUpload


def attach_documents_form():
    return Form('Attach Documents',
                'Attach all relevant documents.',
                [
                    MultiFileUpload('documents')
                ])
