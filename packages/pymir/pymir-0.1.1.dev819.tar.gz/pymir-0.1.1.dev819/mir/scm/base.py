#    Modified from GitPython CMD wrapper:
#    https://github.com/gitpython-developers/GitPython/blob/master/git/cmd.py


class BaseScm():
    """
    Base class providing an interface to retrieve attribute values upon
    first access.
    """

    __slots__ = tuple()

    def __getattr__(self, attr):
        self._set_cache_(attr)
        # will raise in case the cache was not created
        return object.__getattribute__(self, attr)

    def _set_cache_(self, attr):
        """
        This method should be overridden in the derived class.
        """
        pass
