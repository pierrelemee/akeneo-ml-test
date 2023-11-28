from abc import ABC, abstractmethod
from enum import Enum

from src.llm.chain_of_thoughts import AbstractChainOfThoughts
from src.llm.connectors import AbstractLLMConnector
from src.models import ProductField


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

    def lookup_field_description(self, field: ProductField, description: str) -> str:
        """
        Looks up for product field description by:
        * building the LLM query through the CoT
        * fetching the output of the query through the connector
        * processing the result through the CoT

        :param field:
        :param description:
        :return:
        """
        if not self._connector.is_valid():
            return None

        system_prompt, user_message = self._chain_of_thoughts.build_query(
            field, description
        )
        return self._chain_of_thoughts.process_output(
            self._connector.query(self.build_query(system_prompt, user_message))
        )

    @abstractmethod
    def build_query(self, system_prompt: str, user_message: str) -> str:
        """
        Builds a LLM query

        :param system_prompt: the system prompt
        :param user_message:  the user message

        :return: the output as string
        """


class LLaMA(AbstractLLM):
    TEMPLATE = "[INST] <<SYS>>{0}<</SYS>> {1} [/INST]"
    MAX_LENGTH = 4096

    def get_type(self) -> LLMType:
        return LLMType.LLAMA

    def build_query(self, system_prompt: str, user_message: str) -> str:
        return self.TEMPLATE.format(
            # Truncate system prompt to only ensure built query is shorter than the max length
            system_prompt[
                : self.MAX_LENGTH
                - (len(self.TEMPLATE.format("", "")) + len(user_message))
            ],
            user_message,
        )


class CameLLM(AbstractLLM):
    TEMPLATE = """
[INST] <<SYS>>
{0}
<</SYS>>

{1} [/INST]
"""
    MAX_LENGTH = 2048

    def get_type(self) -> LLMType:
        return LLMType.CAMELLM

    def build_query(self, system_prompt: str, user_message: str) -> str:
        return self.TEMPLATE.format(
            # Truncate system prompt to only ensure built query is shorter than the max length
            system_prompt[
                : self.MAX_LENGTH
                - (len(self.TEMPLATE.format("", "")) + len(user_message))
            ],
            user_message,
        )
