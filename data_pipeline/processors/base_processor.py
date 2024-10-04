from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    @abstractmethod
    def process(self, input_data):
        pass

    @abstractmethod
    def batch_process(self, input_data_list):
        pass