from typing import Callable, Generic, TypeVar, Optional, Any


# Generic Types
T = TypeVar("T")  # Value type
E = TypeVar("E")  # Error type
U = TypeVar("U")  # Mapped type
F = TypeVar("F")  # Mapped error type


# Rust-style Result
class Result(Generic[T, E]):
    """Rust-style Result implementation in Python."""

    def __init__(self, value: Optional[T] = None, error: Optional[E] = None):
        if (value is None) == (error is None):
            raise ValueError("Result must contain either a value or an error")
        self._value = value
        self._error = error

    @property
    def is_ok(self) -> bool:
        return self._error is None

    @property
    def is_err(self) -> bool:
        return self._error is not None

    def ok(self) -> Optional[T]:
        return self._value if self.is_ok else None

    def err(self) -> Optional[E]:
        return self._error if self.is_err else None

    def unwrap(self) -> T:
        if self.is_ok:
            return self._value
        raise ValueError(f"Called unwrap on an Err value: {self._error}")

    def unwrap_err(self) -> E:
        if self.is_err:
            return self._error
        raise ValueError(f"Called unwrap_err on an Ok value: {self._value}")

    def map(self, op: Callable[[T], U]) -> 'Result[U, E]':
        if self.is_ok:
            return Result(value=op(self._value))
        return Result(error=self._error)

    def map_err(self, op: Callable[[E], F]) -> 'Result[T, F]':
        if self.is_err:
            return Result(error=op(self._error))
        return Result(value=self._value)

    def and_then(self, op: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        if self.is_ok:
            return op(self._value)
        return Result(error=self._error)

    def or_else(self, op: Callable[[E], 'Result[T, F]']) -> 'Result[T, F]':
        if self.is_err:
            return op(self._error)
        return Result(value=self._value)


# Rust-style Option
class Option(Generic[T]):
    """Rust-style Option implementation in Python."""

    def __init__(self, value: Optional[T] = None):
        self._value = value

    @property
    def is_some(self) -> bool:
        return self._value is not None

    @property
    def is_none(self) -> bool:
        return self._value is None

    def unwrap(self) -> T:
        if self.is_some:
            return self._value
        raise ValueError("Called unwrap on a None value")

    def unwrap_or(self, default: T) -> T:
        return self._value if self.is_some else default

    def map(self, op: Callable[[T], U]) -> 'Option[U]':
        if self.is_some:
            return Option(op(self._value))
        return Option()

    def and_then(self, op: Callable[[T], 'Option[U]']) -> 'Option[U]':
        if self.is_some:
            return op(self._value)
        return Option()

    def or_else(self, op: Callable[[], 'Option[T]']) -> 'Option[T]':
        if self.is_none:
            return op()
        return self


# Decorator for Result
def result_wrapper(func: Callable[..., T]) -> Callable[..., Result[T, Exception]]:
    """
    A decorator to wrap function output in a Result object.
    """
    def wrapped(*args, **kwargs) -> Result[T, Exception]:
        try:
            result = func(*args, **kwargs)
            return Result(value=result)
        except Exception as e:
            return Result(error=e)
    return wrapped


# Decorator for Option
def option_wrapper(func: Callable[..., Optional[T]]) -> Callable[..., Option[T]]:
    """
    A decorator to wrap function output in an Option object.
    """
    def wrapped(*args, **kwargs) -> Option[T]:
        result = func(*args, **kwargs)
        return Option(result)
    return wrapped
