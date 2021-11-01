from typing import Any, Callable

TFunc = Callable[..., Any]


def exception_handler(func: TFunc) -> TFunc:
    def inner(*args: str, **kwargs: dict) -> Any:
        try:
            retval = func(*args, **kwargs)
            return retval
        except Exception as e:
            print(e)
    return inner

