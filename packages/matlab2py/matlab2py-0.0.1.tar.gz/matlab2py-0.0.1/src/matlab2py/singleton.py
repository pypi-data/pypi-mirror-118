"""
Implements the parent class for a singleton.
"""


class Singleton(object):
    """
    This is lifted verbatim from the python docs:
    https://www.python.org/download/releases/2.2/descrintro/#__new__

    Subclasses must implement a method `init` rather than `__init__` because
    `__init__` is called on every attempted instantiation of the class.
    """

    def __new__(cls, *args, **kwargs):
        """
        Override new such that if an instance already exists, we just return it.
        If it exists it's stored in the `__it__` member.
        Note that this can't use `hasattr` as explained in a comment on this
        SO answer: https://stackoverflow.com/a/11517201/13722253
        """
        it = cls.__dict__.get("__it__")

        if it is not None:
            return it

        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwargs)

        return it

    def init(self, *args, **kwds):
        """The replacement for `__init__`."""
        pass
