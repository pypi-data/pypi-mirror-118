from typing import Container, Generic, Iterable, Iterator, Reversible, TypeVar
from collections import deque

T = TypeVar("T")


class Queue(Generic[T], Container[T], Reversible[T]):
	"""A collection of items which can be accessed in a FIFO order.

	Args:
		Generic (T): The type of the items stored in the queue.
	"""

	def __init__(self, items: Iterable[T] = ()) -> None:
		"""Construct a queue.

		Args:
			items (Iterable[T], optional): An iterable of the items to initialize the queue with. If omitted, queue will be empty.
		"""
		self.__queue = deque[T](items)

	def push(self, value: T):
		"""Push an item to the back of the queue.

		Args:
			value (T): The item to push to the back of the queue.
		"""
		self.__queue.append(value)

	def pop(self) -> T:
		"""Pop an item from the front of the queue.

		Returns:
			T: The frontmost item that was removed from the queue.

		Raises:
			IndexError: If the queue was empty.
		"""
		return self.__queue.popleft()

	def __len__(self) -> int:
		return len(self.__queue)

	def __bool__(self) -> bool:
		return bool(self.__queue)

	def __contains__(self, item: object) -> bool:
		return item in self.__queue

	def __reversed__(self) -> Iterator[T]:
		return reversed(self.__queue)

	def __iter__(self) -> Iterator[T]:
		return iter(self.__queue)