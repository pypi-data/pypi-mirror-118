from urllib.parse import urlparse, parse_qsl
from typing import Tuple, Dict, Union, ItemsView


def etcdurl_parser(url: str) -> Tuple[bool, Dict[str, Union[str, int, ItemsView]]]:
    """解析etcd路径

    Args:
        url (str): etcd的地址,注意请以`etcd://`或者`etcd+async://`开头

    Raises:
        AttributeError: schema 必须为etcd

    Returns:
        Dict[str, Union[str, int, Dict[str, str]]]: 初始化etcd客户端的参数数据
    """
    keys = ("timeout", "ca_cert", "cert_key", "cert_cert")
    aio = False
    intkeys = ("timeout",)
    result: Dict[str, Union[str, int, ItemsView]] = {
        "host": '127.0.0.1',
        "port": 2379,
    }
    parse_result = urlparse(url)
    schema = parse_result.scheme.lower()
    if schema not in ("etcd", "etcd+async"):
        raise AttributeError("schema 必须为etcd")
    if schema == "etcd+async":
        aio = True
    if parse_result.username:
        result.update({"user": parse_result.username})
    if parse_result.password:
        result.update({"password": parse_result.password})
    if parse_result.port:
        result.update({"port": parse_result.port})
    if parse_result.hostname:
        result.update({"host": parse_result.hostname})
    if parse_result.query:
        sql_result = dict(parse_qsl(parse_result.query))
        _grpc_options: Dict[str, Union[str, int]] = {}
        for k, v in sql_result.items():
            if k in keys:
                if k in intkeys:
                    result.update({k: int(v)})
                else:
                    result.update({k: v})
            else:
                if v.isdigit():
                    _grpc_options.update({k: int(v)})
                else:
                    _grpc_options.update({k: v})
        if _grpc_options:
            grpc_options = _grpc_options.items()
            result.update({"grpc_options": grpc_options})
    return aio, result
