from abc import ABC, abstractmethod
from enum import Enum

from src.models.chain_of_thoughts import AbstractChainOfThoughts
from src.models.connectors import AbstractLLMConnector
from src.models.product import Field


class LLMType(Enum):
    LLAMA = "llama2"
    CAMELLM = "camellm"


class AbstractLLM(ABC):
    """
    A LLM knows how to format the LLM query given system prompt and user message
    """

    _connector: AbstractLLMConnector
    _chain_of_thoughts: AbstractChainOfThoughts

    def __init__(
        self,
        connector: AbstractLLMConnector,
        chain_of_thoughts: AbstractChainOfThoughts,
    ):
        super().__init__()

        if not connector.supprts(self.get_type()):
            raise Exception(
                f"Unsupported connector ${type(connector)} for LLM type ${self.get_type().name}"
            )

        self._connector = connector
        self._chain_of_thoughts = chain_of_thoughts

    @abstractmethod
    def get_type(self) -> LLMType:
        pass

    def lookup_field_description(self, field: Field, description: str) -> str:
        if not self._connector.is_valid():
            return None

        system_prompt, user_message = self._chain_of_thoughts.build_query(
            field, description
        )
        return self._connector.query(self.build_query(system_prompt, user_message))

    @abstractmethod
    def build_query(self, system_prompt: str, user_message: str) -> str:
        """
        Builds a LLM query

        :param system_prompt: the system prompt
        :param user_message:  the user message

        :return: the output as string
        """
        pass


class LLaMA(AbstractLLM):
    def get_type(self) -> LLMType:
        return LLMType.LLAMA

    def build_query(self, system_prompt: str, user_message: str) -> str:
        # TODO: ensure built query doesn't exceed 4096 characters
        return f"""
[INST] <<SYS>>
${system_prompt}
<</SYS>>

{user_message} [/INST]
"""


class CameLLM(AbstractLLM):
    def get_type(self) -> LLMType:
        return LLMType.CAMELLM

    def build_query(self, system_prompt: str, user_message: str) -> str:
        # TODO: ensure built query doesn't exceed 2048 characters
        return f"""
[INST] <<SYS>>
${system_prompt}
<</SYS>>

{user_message} [/INST]
"""
