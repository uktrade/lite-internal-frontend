def clean_advice(json):
    import ast

    def _clean_dict_item(item):
        return ast.literal_eval(item)

    json = json.copy()

    json['goods'] = _clean_dict_item(json['goods'])
    json['goods_types'] = _clean_dict_item(json['goods_types'])
    json['countries'] = _clean_dict_item(json['countries'])
    json['end_user'] = _clean_dict_item(json['end_user'])
    json['ultimate_end_users'] = _clean_dict_item(json['ultimate_end_users'])
    json['denial_reasons'] = json.getlist('denial_reasons')

    if json['end_user']:
        json['end_user'] = json['end_user'][0]
    else:
        json['end_user'] = None

    return json
