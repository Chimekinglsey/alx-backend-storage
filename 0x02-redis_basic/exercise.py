#!/usr/bin/env python3
"""
1. Reading from Redis and recovering original type
"""
import redis
from typing import Union, Callable, Optional, Any
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Invokes the given method after incrementing its call counter.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    '''Tracks the call details of a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Returns the method's output after storing its inputs and output.
        '''
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker


def replay(fn: Callable) -> None:
    '''Displays the call history of a Cache class' method.
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


class Cache:
    """simulate a redis"""
    def __init__(self, host='localhost', port=6379, db=0) -> None:
        self._redis = redis.Redis(host=host, port=port, db=db)
        self._redis.flushdb()

    @call_history
    @count_calls
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
