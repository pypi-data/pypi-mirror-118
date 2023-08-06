# PyNeo
#
# @Author: Lin, Jason
# @Email : Jason.M.Lin@outlook.co
# @Time  : 2021/8/31 2:27 下午
#
# =============================================================================
"""connection"""
from typing import Optional, Tuple
from neo4j import GraphDatabase, Session


class Graph(object):
    _uri: str
    _auth: Optional[Tuple[str, str]]
    _config: dict
    _session: Session = None

    def __init__(self, uri: str, *, auth: Optional[Tuple[str, str]] = None, **config):
        """
        Args:
            uri: bolt://localhost:7687
            auth: (username, password)
            **config: database="TheOtherDb"可以控制默认的数据库
        """
        self._uri = uri
        self._auth = auth
        self._config = config
        self.driver = GraphDatabase.driver(uri, auth=auth, **config)

    @property
    def uri(self):
        return self._uri

    @property
    def auth(self):
        return self._auth

    @property
    def config(self):
        return self._config

    def run(self, cql: str):
        self._session.run(cql)

    def __enter__(self):
        self._session = self.driver.session(**self._config)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()
        self.driver.close()



