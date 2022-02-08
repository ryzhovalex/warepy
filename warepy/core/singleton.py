from abc import ABCMeta


class SingletonMeta(type):
    """Singleton metaclass for implementing singleton patterns. 
    Source: https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python

    Usage:
    ```
    class MySingleInstanceClass(metaclass=Singleton): ...
    ```
    """
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super().__call__(*args, **kwargs)
        return cls.instances[cls]


class Singleton(metaclass=SingletonMeta):
    """
    Singleton object with some essential methods for accessing singleton instances without arguments and without linter errors.

    Particularly, all meant to be singleton classes should be inherited from this object.
    """
    @classmethod
    def get_instance(cls) -> object:
        """Return instance binded to called singleton avoiding linter missing arguments error."""
        return cls()