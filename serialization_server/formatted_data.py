def parse_dict(msg: str) -> dict[str]:
    print('GOT MSG:', msg)
    lines = msg.split('\n')
    while '' in lines:
        lines.remove('')
    params = {}
    for line in lines:
        print(line)
        param, value = line.split(':')
        param = param.strip()
        value = value.strip()
        params[param] = value
    return params
