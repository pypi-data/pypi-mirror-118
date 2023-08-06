from abc import ABC, abstractmethod
import logging


class BaseCommand(ABC):
    """base class for all commands in mir"""

    # lifecycle
    def __init__(self, args):
        self.args = args

    # public: abstract
    @abstractmethod
    def run(self):
        logging.critical("BaseCommand run: this action should override in sub classes")
