from abc import ABC, abstractmethod

class Runnable(ABC):

    @abstractmethod
    def run(self):
        raise NotImplementedError
    
    @abstractmethod
    def run(self, content, queue):
        raise NotImplementedError