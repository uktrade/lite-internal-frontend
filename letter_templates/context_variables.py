import json

JSON_PATH = 'lite-content/lite-internal-frontend/context_variables.json'
flattened_context_variables = {}


def _get_valid_class_types(variables):
    valid_variables = {}
    for key, data in variables.items():
        if data['valid'] == "True":
            valid_variables[key] = data
    return valid_variables


def _add_base_class_variables(raw_json, build_order):
    for class_name in build_order:
        for base_name in raw_json[class_name]['base']:
            raw_json[class_name].update({base_name: raw_json[base_name]})
    return raw_json


def load_context_variables():
    with open(JSON_PATH, 'r') as f:
        raw_json = json.load(f)

    # Populate classes with any base class variables
    raw_json = _add_base_class_variables(raw_json, raw_json['build_order']['order'])

    # Extract all object types we want to give to the user (using 'valid' key)
    valid_variables = _get_valid_class_types(raw_json)

    return valid_variables


def flatten_dict(dictionary, path):
    if path != '':
        path += '.'
    for key, value in dictionary.items():
        if isinstance(value, dict):
            flatten_dict(value, path+key)
        elif key == 'variables':
            for variable in value:
                flattened_context_variables[path + variable] = variable


context_variables = load_context_variables()
flatten_dict(context_variables, '')


def get_sample_context_variables():
    return get_key_value_pair(flattened_context_variables)


def get_key_value_pair(data):
    return [{'key': key, 'value': value, 'representation': '{'+key+'}}'} for (key, value) in data.items()]
