from typing import Collection, Generic, Iterable, Iterator, Reversible, TypeVar


T = TypeVar("T")


class Stack(Generic[T], Reversible[T], Collection[T]):
	"""A collection of items which can be accessed in a LIFO order.

	Args:
		Generic (T): The type of the items stored in the stack.
	"""

	def __init__(self, items: Iterable[T] = ()) -> None:
		"""Construct a stack.

		Args:
			items (Iterable[T], optional): An iterable of the items to initialize the stack with. If omitted, stack will be empty.
		"""
		self.__list = list(items)

	def push(self, value: T):
		"""Push an item onto the stack.

		Args:
			value (T): The item to push onto the stack.
		"""
		self.__list.append(value)

	def pop(self) -> T:
		"""Pop an item from the top of the stack.

		Returns:
			T: The topmost item that was removed from the stack.

		Raises:
			IndexError: If the stack was empty.
		"""
		return self.__list.pop()

	def __len__(self) -> int:
		return len(self.__list)

	def __bool__(self) -> bool:
		return bool(self.__list)

	def __contains__(self, item: object) -> bool:
		return item in self.__list

	def __reversed__(self) -> Iterator[T]:
		return reversed(self.__list)

	def __iter__(self) -> Iterator[T]:
		return iter(self.__list)