import typing

from elasticsearch_dsl.connections import create_connection, get_connection, Elasticsearch
from pydantic import BaseModel, Field

from wisdoms_dapr import exceptions


class ElasticsearchConnectionConfig(BaseModel):
    class AuthConfig(BaseModel):
        username: str
        password: str

    hosts: typing.Union[str, list[str]]
    auth: typing.Optional[AuthConfig]
    timeout: float = Field(12, ge=3)


def create_elasticsearch_connection(
        config: typing.Union[dict, ElasticsearchConnectionConfig],
        *,
        alias: str = None
) -> Elasticsearch:
    """Create Elasticsearch Connection"""

    try:
        conf = ElasticsearchConnectionConfig(**config)
    except Exception as e:
        print(e)
        raise exceptions.InvalidConfigError

    try:
        c = get_connection(alias=alias)
        if c:
            return c
    except KeyError:
        pass

    return create_connection(**conf.dict())
