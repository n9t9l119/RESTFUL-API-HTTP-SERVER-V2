from abc import ABC, abstractmethod


class AbstractDataTemplate(ABC):
    @abstractmethod
    def check_template_matches(self, data):
        raise NotImplementedError(
            f'Method {self.__class__.check_template_matches.__name__} not implemented in class {self.__class__.__name__}')