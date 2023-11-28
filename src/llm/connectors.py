import os
from abc import ABC, abstractmethod
import replicate


class AbstractLLMConnector(ABC):
    """
    A LLMConnector gives the ability to reach an actual LLM . It can be by any mean: system command, raw python, HTTP
    query, SSH, etc...
    """

    def supprts(self, type: "LLMType") -> bool:
        return True

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


class ReplicateLLaMAConnector(AbstractLLMConnector):
    """
    Performs a query to an actual LLaMA2 using the `replicate` library.

    Ensure the API token is defined in the REPLICATE_API_TOKEN environment variable first.
    """

    _ref: str

    def __init__(self):
        super().__init__()

        self._ref = os.getenv(
            "REPLICATE_REF",
            "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        )

    def query(self, query: str) -> str:
        output = replicate.run(
            self._ref,
            input={"prompt": query},
        )

        return "".join(list(output))


class DumbCameLLMConnector(AbstractLLMConnector):
    """
    Dumb connector in plain Python always returning the same static value "Answer CameLL".

    Use for testing purpose only
    """

    def query(self, query: str) -> str:
        return "Answer CameLL"
