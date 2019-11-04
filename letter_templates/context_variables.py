context_variables = {
    'applicant': {
        'name': 'John Smith'
    },
    'consignee': {
        'name': 'Jane Smith'
    }
}
flattened_context_variables = {}


def flatten_dict(dictionary, path):
    if path != '':
        path += '.'
    for key, value in dictionary.items():
        if isinstance(value, dict):
            flatten_dict(value, path+key)
        else:
            flattened_context_variables[path + key] = value


flatten_dict(context_variables, '')


def get_sample_context_variables():
    return get_key_value_pair(flattened_context_variables)


def get_key_value_pair(data):
    return [{'key': key, 'value':  value} for (key, value) in data.items()]
