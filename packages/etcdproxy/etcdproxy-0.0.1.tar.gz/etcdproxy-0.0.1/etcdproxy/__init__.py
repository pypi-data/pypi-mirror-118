
from typing import Optional, Any
from pyproxypattern import Proxy
from .url_parser import etcdurl_parser


class EtcdProxy(Proxy):
    """etcd的代理类."""
    __slots__ = ('instance', "_callbacks", "_instance_check", "aio")

    def __init__(self, *, url: Optional[str] = None) -> None:
        """初始化一个etcd代理.

        Args:
            url (Optional[str], optional): etcd的url路径,注意schema为`etcd`或`etcd+async`. Defaults to None.
        """

        if url:
            instance = self.new_instance(url)
            super().__init__(instance)
        else:
            super().__init__()

    def new_instance(self, url: str) -> Any:
        aio, configs = etcdurl_parser(url)
        if aio:
            self.aio = True
            import aetcd3
            return aetcd3.client(**configs)
        else:
            self.aio = False
            import etcd3
            return etcd3.client(**configs)

    def initialize_from_url(self, url: str) -> None:
        """从url初始化."""
        instance = self.new_instance(url)
        self.initialize(instance)
