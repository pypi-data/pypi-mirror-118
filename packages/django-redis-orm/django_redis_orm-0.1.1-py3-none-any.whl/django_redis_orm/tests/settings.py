"""
    Caching test
        1. Set REDIS_ROOTS in project settings
        2. Provide models with this redis roots
        3. Run: python manage.py run_redis_caching
"""

from django_redis_orm.core import *


def get_connection_pool():
    host = 'localhost'
    port = 6379
    db = 0
    connection_pool = redis.ConnectionPool(
        decode_responses=True,
        host=host,
        port=port,
        db=db,
    )
    return connection_pool


REDIS_ROOTS = {
    'test_caching_root': RedisRoot(
        prefix='test_caching',
        connection_pool=get_connection_pool(),
        ignore_deserialization_errors=True,
        economy=True
    )
}
