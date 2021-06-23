import abc


class TypePlugin(abc.ABC):
    @abc.abstractmethod
    def get_source(self):
        pass
