from collections import OrderedDict


class AttrDict(OrderedDict):
    __exclude_keys__ = set()

    def __getattr__(self, key):
        if key in self.__exclude_keys__:
            return super(AttrDict, self).__getattribute__(key)
        try:
            return self[key]
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        if key in self.__exclude_keys__:
            super(AttrDict, self).__setattr__(key, value)
            return
        self[key] = value
