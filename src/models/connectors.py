from abc import ABC, abstractmethod


class AbstractLLMConnector(ABC):
    """
    A LLMConnector gives the ability to reach an actual LLM . It can be by any mean: system command, raw python, HTTP
    query, SSH, etc...
    """

    def is_valid(self) -> bool:
        """
        Checks whether the connection is valid. Rewrite this method to adapt the logic.

        :return: bool
        """
        return True

    @abstractmethod
    def query(self, query: str) -> str:
        """

        :param query: str the LLM query to be executed
        :return:
        """


class DumbLLaMAConnector(AbstractLLMConnector):
    """
    Dumb connector in plain Python always returning the same static value "Answer LLaMA".

    Use for testing purpose only
    """

    def query(self, query: str) -> str:
        return "Answer LLaMA"


class DumbCameLLMConnector(AbstractLLMConnector):
    """
    Dumb connector in plain Python always returning the same static value "Answer CameLL".

    Use for testing purpose only
    """

    def query(self, query: str) -> str:
        return "Answer CameLL"
