from pytest import fixture

from shared.tools.utils import get_lite_client


@fixture(scope='module')
def add_a_document_template(context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config)
    document_template = lite_client.seed_document_template.add_template(lite_client.seed_picklist)
    context.document_template_name = document_template['name']
    context.document_template_layout = document_template['layout']['name']
    context.document_template_restricted_to = [document_template['restricted_to'][0]['value']]
    context.document_template_paragraph_text = [document_template['paragraph']['text']]


def get_paragraph_text(context, seed_data_config, paragraph_id):
    lite_client = get_lite_client(context, seed_data_config)
    return lite_client.seed_document_template.get_paragraph(paragraph_id)['text']
