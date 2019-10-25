def convert_dict_to_query_params(dictionary, start=''):
    items = []
    for key, value in dictionary.items():
        if isinstance(value, list):
            for val in value:
                items.append(key + '=' + str(val))
        else:
            items.append(key + '=' + str(value))
    return start+'&'.join(items)
