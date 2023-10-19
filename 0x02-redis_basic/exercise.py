#!/usr/bin/env python3
"""
1. Reading from Redis and recovering original type
"""
import redis
from typing import Union, Callable, Optional, Any
import uuid

class Cache:
    """simulate a redis"""
    def __init__(self, host='localhost', port=6379, db=0) -> None:
        self._redis = redis.Redis(host=host, port=port, db=db)
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random uuid, store it in Redis, return the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable[[Union[str, bytes, int, float]],
                                  Any]] = None
            ) -> Union[str, bytes, int, float, None]:
        """
            Retrieve data from the cache using the provided key.
        """
        if key in self._redis:
            data = self._redis.get(key)
            if fn is not None:
                return fn(data)
            return data
        return None

    def get_str(self, key: str) -> str:
        """
        Retrieve data from the cache and convert it to a UTF-8 encoded string.

        Args:
            key (str): The key to look up in the cache.

        Returns:
            str: The retrieved data converted to a UTF-8 encoded string.
        """
        return self.get(key, fn=lambda data: data.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieve data from the cache and convert it to an integer.
        """
        return self.get(key, fn=int)

# cache = Cache()

# TEST_CASES = {
#     b"foo": None,
#     123: int,
#     "bar": lambda d: d.decode("utf-8")
# }

# for value, fn in TEST_CASES.items():
#     key = cache.store(value)
#     assert cache.get(key, fn=fn) == value
