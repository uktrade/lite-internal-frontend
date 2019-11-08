import json

JSON_PATH = 'lite-content/lite-internal-frontend/context_variables.json'
flattened_context_variables = []


def _get_valid_class_types(variables):
    valid_variables = {}
    for key, data in variables.items():
        if data['valid'] == "True":
            valid_variables[key] = data
    return valid_variables


def _get_build_order(json):
    keys = []
    for key, value in json.items():
        if 'extends' in value:
            keys.append(key)
    return keys


def _add_base_class_variables(json):
    for class_name in _get_build_order(json):
        for base_name in json[class_name]['extends']:
            json[class_name].update({base_name: json[base_name]})
    return json


def load_context_variables():
    with open(JSON_PATH, 'r') as f:
        variables = json.load(f)

    # Populate classes with any base class variables
    variables = _add_base_class_variables(variables)

    # Extract all object types we want to give to the user (using 'valid' key)
    variables = _get_valid_class_types(variables)

    return variables


def flatten_dict(dictionary, path):
    if path != '':
        path += '.'
    for key, value in dictionary.items():
        if isinstance(value, dict):
            flatten_dict(value, path+key)
        elif key == 'variables':
            for variable in value:
                flattened_context_variables.append(path + variable)


context_variables = load_context_variables()
flatten_dict(context_variables, '')


def get_sample_context_variables():
    return get_key_value_pair(flattened_context_variables)


def get_key_value_pair(data):
    return [{'key': item, 'representation': '{' + item + '}}'} for item in data]
