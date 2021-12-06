import json

import environ
import redis

from ks_shared.decoration import singleton

env = environ.Env()


@singleton
class RedisStorage(object):
    redis = None
    _prefix = 'grz_campaign'

    def __init__(self, prefix=None):
        self.redis = redis.from_url(env("REDIS_URL"))
        if prefix:
            self._prefix = prefix

    @property
    def client(self):
        return self.redis

    def key_name(self, key):
        return '{0}:{1}'.format(self._prefix, key)

    def get(self, key, default=None):
        key = self.key_name(key)
        value = self.redis.get(key)
        if value is None:
            return default
        return json.loads(value.decode('utf-8'))

    def set(self, key, value, ttl=None):
        if value is None:
            return
        key = self.key_name(key)
        value = json.dumps(value)
        self.redis.set(key, value, ex=ttl)

    def incr(self, key, amount=1):
        if amount is None:
            return
        key = self.key_name(key)
        self.redis.incr(key, amount=amount)

    def delete(self, key):
        key = self.key_name(key)
        self.redis.delete(key)
