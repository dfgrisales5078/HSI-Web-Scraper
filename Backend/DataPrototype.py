from abc import ABC, abstractmethod

class DataPrototype(ABC):
    def __int__(self):
        self.data = None

    @abstractmethod
    def format_data(self):
        pass

    @abstractmethod
    def send_data_to_file(self):
        pass