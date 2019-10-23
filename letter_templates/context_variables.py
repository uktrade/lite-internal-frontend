sample_values = {
    'applicant.name': 'John Smith',
    'consignee.name': 'Jane Smith'
}


def get_sample_context_variables():
    return get_key_value_pair(sample_values)


def get_key_value_pair(data):
    return [{'key': key, 'value':  value} for (key, value) in data.items()]
