from abc import ABC, abstractmethod


class Queable(ABC):
    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def result(self):
        pass

    @abstractmethod
    def to_json(self):
        pass

    @abstractmethod
    def load_json(self, json_model):
        pass

    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def quality(self):
        pass
