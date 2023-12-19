import unittest

from django.test import TestCase

import random

from .models import Queue
from django.db import IntegrityError


# 1)	Реализуйте класс UniqueQueue, очереди которая хранит только уникальные элементы в списке.
# При добавлении нового элемента(который уже есть ) в очередь ничего не должно происходить.
# Уникальный же элемент добавляйте обычным образом.
class UniqueQueue:
    LIFO = "LIFO"

    def __init__(self, strategy="LIFO"):
        if strategy != self.LIFO:
            raise ValueError
        self.strategy = strategy
        self.storage = []

    def is_empty(self):
        return len(self.storage) == 0

    def add(self, value):
        if value not in self.storage:
            self.storage.append(value)

    def pop(self):
        if not self.is_empty():
            return self.storage.pop(0)
        else:
            raise ValueError("Storage is empty")

    # 2) В классе UniqueQueue реализуйте методы для получения длинны очереди
    def size(self):
        return len(self.storage)

    def first(self):
        if not self.is_empty():
            return self.storage[0]
        else:
            raise ValueError("Storage is empty")

    # 2) и последнего элемента, добавленного в очередь
    def last(self):
        if not self.is_empty():
            return self.storage[-1]
        else:
            raise ValueError("Storage is empty")


# 3)	Реализуйте тесты для стратегии LIFO, а также для проверки методов описанных во 2 пункте.
# У вас должно быть не менее 10 различных тестовых сценариев.
class TestUniqueQueue(unittest.TestCase):
    def setUp(self):
        self.unique_queue = UniqueQueue()
        self.mock_data = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]

    def test_queue_exist(self):
        self.assertIsInstance(self.unique_queue, UniqueQueue)

    def test_set_wrong_strategy(self):
        with self.assertRaises(ValueError):
            wrong_strategy = "FIFO"
            UniqueQueue(wrong_strategy)

    def test_add_value(self):
        self.unique_queue.add(self.mock_data[0])
        value = self.unique_queue.pop()
        self.assertEqual(value, self.mock_data[0])

    def test_add_multivalues(self):
        random_numbers = self.mock_data
        unique_list = []
        for number in random_numbers:
            self.unique_queue.add(number)
            last_value = self.unique_queue.last()
            if last_value not in unique_list:
                unique_list.append(last_value)

        for number in unique_list:
            value = self.unique_queue.pop()
            self.assertEqual(value, number)

    def test_pop_value(self):
        self.unique_queue.add(self.mock_data[0])
        self.unique_queue.add(self.mock_data[1])
        self.assertEqual(self.unique_queue.pop(), self.mock_data[0])

    def test_add_dublicate(self):
        self.unique_queue.add(self.mock_data[0])
        self.unique_queue.add(self.mock_data[5])
        self.assertEqual(self.unique_queue.size(), 1)

    def test_size(self):
        random_numbers = [random.randint(1, 10) for _ in range(10)]
        # random_numbers = self.mock_data
        unique_len = len(set(random_numbers))

        for number in random_numbers:
            self.unique_queue.add(number)

        self.assertEqual(self.unique_queue.size(), unique_len)

    def test_first(self):
        self.unique_queue.add(self.mock_data[0])
        self.unique_queue.add(self.mock_data[1])
        self.assertEqual(self.unique_queue.first(), self.mock_data[0])

    def test_last(self):
        self.unique_queue.add(self.mock_data[0])
        self.unique_queue.add(self.mock_data[1])
        self.assertEqual(self.unique_queue.last(), self.mock_data[1])

    def test_empty(self):
        self.unique_queue.add(self.mock_data[0])
        self.unique_queue.pop()
        with self.assertRaises(ValueError):
            self.unique_queue.pop()


# 4) Подключите тестовую базу данных Django и Создайте модель Queue.
# Сделайте рефакторинг вашей UniqueQueue с использованием созданной модели.
from .models import Queue


class UniqueQueue2:
    def add(self, item):
        if self.is_unique(item):
            Queue.objects.create(item=item)
            return True
        else:
            raise ValueError("Dublicate")

    def is_unique(self, item):
        return not Queue.objects.filter(item=item).exists()


class UniqueQueueTests(TestCase):
    def test_add_value(self):
        unique_queue = UniqueQueue2()
        result = unique_queue.add("value1")
        self.assertTrue(result)

    def test_add_dublicate(self):
        Queue.objects.create(item="value2")
        unique_queue = UniqueQueue2()
        result = unique_queue.add("value2")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
