import os
import sys
import inspect
from typing import Literal
from functools import wraps

from loguru import logger as loguru

from .singleton import Singleton


class logger(Singleton):
    """Logger tool responsible of writing all actions to logs.

    Simply said - it is a extra layer over `loguru.logger` for keeping one logger through all program.

    Usage:
    ```
        from path.to.logger import logger
        logger(*your_args, **your_kwargs)
        logger.debug("hello!")
    ```
    """

    native_logger = loguru  # loguru.logger itself

    # Initialize class function variables.
    debug = native_logger.debug
    info = native_logger.info
    warning = native_logger.warning
    error = native_logger.error
    critical = native_logger.critical

    # Head catch decorator for final level of program with calling exit.
    head_catch = native_logger.catch(onerror=lambda _: sys.exit(1))

    # Original catch decorator for feeling free at args setting.
    origin_catch = native_logger.catch

    def __init__(self, *args, **kwargs) -> None:
        logger.create_logger(*args, **kwargs)

    @classmethod
    def catch(cls, func):
        """Log occured exceptions in function if it hasn't been done before and reraise it to higher level in any case."""
        @wraps(func)
        def inner(*args, **kwargs):
            # If error is logged, add extra message with it's module and function names.
            # Of course, better to put this data directly to code loguru context constructors, 
            # but it requires more deeper researching of loguru project itself, so it could be done later to improve this functionality.
            # But for now, enjoy parsing `extra` field of loguru's output :-).
            try:
                output = func(*args, **kwargs)
            except Exception as error:
                if len(error.args) == 2: # i.e some catcher already signed this error
                    # Just reraise error without logging.
                    raise error
                else:
                    inspect_module = inspect.getmodule(func)
                    if inspect_module:
                        node_info = inspect_module.__name__ + "." + func.__name__
                        with cls.native_logger.contextualize(node=node_info):
                            # Log and reraise error with new sign node argument.
                            logger.error(f"{error.__class__.__name__}: {error}")
                            raise error.__class__(node_info, error.args[0])
            else:
                return output
        return inner

    @classmethod
    def create_logger(cls, *args, **kwargs) -> int:
        return cls.native_logger.add(*args, **kwargs)

    @classmethod
    def remove_logger(cls, id: int) -> None:
        cls.native_logger.remove(id)

    @classmethod
    def get_native_logger(cls):
        return cls.native_logger

    @classmethod
    def init_logger(
        cls,
        *, 
        path: str, 
        format: str, 
        rotation: str, 
        level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        serialize: bool,
        has_to_delete_old: bool = False
    ) -> None:
        """Init logger model instance depending on given arguments. 

        Just a helpful method to recognize which arguments should be added with type hinting, and which is remain static.
        
        Remove previous old log if `has_to_delete_old=True`."""
        if has_to_delete_old and os.path.isfile(path):
            os.remove(path)
        cls(
            path, 
            format=format, 
            level=level,
            compression="zip", 
            rotation=rotation, 
            serialize=serialize
        ) 