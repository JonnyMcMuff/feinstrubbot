from abc import *


class Command:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self):
        pass

