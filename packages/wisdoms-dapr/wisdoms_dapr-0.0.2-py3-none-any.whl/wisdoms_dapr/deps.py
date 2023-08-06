import typing

from elasticsearch_dsl import connections
from redis import Redis

from wisdoms_dapr.elasticsearch import ElasticsearchConnectionConfig


def get_es(conf: typing.Union[dict, ElasticsearchConnectionConfig]) -> typing.Callable:
    """Get Elasticsearch Connection

    conf:
        hosts: http url[s]
        auth:
            username: str
            password: str
        timeout: int
        **kwargs: es kwargs

    raise: connection exceptions
    """

    if isinstance(conf, ElasticsearchConnectionConfig):
        conf = conf.dict()

    def _get_es() -> connections.Elasticsearch:
        try:
            return connections.get_connection()
        except KeyError:
            auth = None
            if isinstance(conf.get('auth'), dict) and conf['auth'].get('username') and conf['auth'].get('password'):
                auth = conf.pop('auth')
                auth = (auth['username'], auth['password'])

            return connections.create_connection(http_auth=auth, **conf)

    return _get_es


def get_redis(conf: dict) -> typing.Callable:
    """
    Get Redis Connection

    conf: package redis.Redis init kwargs
    raise: redis connection exception
    """
    db = None

    def _get_redis() -> Redis:
        nonlocal db
        if db is None:
            db = Redis(**conf)

        return db

    return _get_redis
