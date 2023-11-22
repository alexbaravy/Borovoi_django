from time import sleep
from functools import lru_cache
from random import randint


@lru_cache()
def cache_function(data):
    # sleep(3)
    if not data:
        return 0
    current_number = data[0]
    rest_of_list = data[1:]
    if current_number > 0:
        return current_number + cache_function(rest_of_list)
    else:
        return cache_function(rest_of_list)


my_list = [randint(-1000, 1000) for _ in range(100)]

print("before cache:")
print(cache_function(tuple(my_list)))  # считаем результат и заносим в кэш
sleep(1)
print("after cache:")
print(cache_function(tuple(my_list)))  # сразу возвращаем результат, он уже в кэше
