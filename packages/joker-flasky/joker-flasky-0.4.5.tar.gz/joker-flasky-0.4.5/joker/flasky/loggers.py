#!/usr/bin/env python3
# coding: utf-8

import logging
from logging import Handler, LogRecord

import orjson
from redis import Redis

from joker.flasky.errors import ErrorInfo


class RedisHandler(Handler):
    """
    A handler class which writes logging records to a redis queue.
    """

    redis_key = 'logging.q'

    def _get_redis(self) -> Redis:
        raise NotImplementedError

    def __init__(self, level=logging.NOTSET, limit=1000):
        super().__init__()
        self.redis = self._get_redis()
        self.limit = limit

    def emit(self, record: LogRecord):
        """Emit a record."""
        try:
            msg = self.format(record)
            with self.redis.pipeline(transaction=True) as pipe:
                pipe.lpush(self.redis_key, msg)
                pipe.ltrim(self.redis_key, 0, self.limit)
                pipe.execute()
        except Exception:
            self.handleError(record)


class ErrorInterface:
    def __init__(self, redis: Redis, prefix: str, limit=1000, ttl=3600):
        self.redis = redis
        self.prefix = prefix
        self.limit = limit
        self.ttl = ttl

    def dump(self, errinfo: ErrorInfo):
        ek = errinfo.error_key
        if self.redis.incr(f'{self.prefix}.err-count.{ek}') > 1:
            return
        dinfo = orjson.dumps(errinfo.debug_info)
        pipe = self.redis.pipeline()
        pipe.setex(f'{self.prefix}.err-debug.{ek}', self.ttl, dinfo)
        pipe.lpush(f'{self.prefix}.err-queue', ek)
        pipe.ltrim(f'{self.prefix}.err-queue', 0, self.limit)
        pipe.execute()

    def query(self, error_key: str) -> dict:
        dinfo = self.redis.get(f'{self.prefix}.err.{error_key}')
        if not dinfo:
            return {}
        return orjson.loads(dinfo)


__all__ = ['ErrorInterface', 'RedisHandler']
