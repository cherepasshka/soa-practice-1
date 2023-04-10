import json


def parse_param(value: str, param: str):
    if param == 'int':
        return int(value)
    elif param == 'float':
        return float(value)
    elif param == 'list_str':
        return list(value[1:-1].split())
    elif param == 'list_int':
        return list(map(int, value[1:-1].split()))
    elif param == 'list_float':
        return list(map(float, value[1:-1].split()))
    elif param == 'dict':
        if "'" in value:
            value = value.replace("'", '"')
        return json.loads(value)
    return value


def parse_dict(msg: str) -> dict[str]:
    lines = msg.split('\n')
    while '' in lines:
        lines.remove('')
    params = {}
    for line in lines:
        index = line.index(':')
        param, value = line[:index], line[index + 1:]
        param = param.strip()
        value = value.strip()
        params[param] = parse_param(value, param)
    return params
