from abc import ABC, abstractmethod


class Queable:
    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def result(self):
        pass


class Processor:
    def __init__(self):
        self.queue = []
        self.result = []

    def add(self, queue_object):
        self.queue.append(queue_object)

    def process(self):
        for obj in self.queue:
            self.result.append(obj.process())

    def results(self):
        return self.result
