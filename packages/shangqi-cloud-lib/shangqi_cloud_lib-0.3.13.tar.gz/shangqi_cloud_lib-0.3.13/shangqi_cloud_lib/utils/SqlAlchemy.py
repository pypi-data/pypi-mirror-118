def alchemy_default_to_dict(params, data):
    data_list = []
    key_list = []
    for arg in params:
        key_list.append(str(arg).split(".")[-1])
    if isinstance(data, list):
        for d in data:
            dict_data = dict(zip(key_list, d))
            data_list.append(dict_data)
        return data_list
    else:
        if data:
            return dict(zip(key_list, data))
        else:
            return {}
