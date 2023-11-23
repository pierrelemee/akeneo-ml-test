from abc import ABC, abstractmethod
from typing import Tuple

from src.fields import Field


class AbstractLLMConnector(ABC):
    """
    A LLMConnector gives the ability to reach an actual LLM . It can be by any mean: system command, raw python, HTTP
    query, SSH, etc...
    """

    @abstractmethod
    def query(self, query: str) -> str:
        """

        :param query: str the LLM query to be executed
        :return:
        """
        pass


class AbstractChainOfThoughts(ABC):
    """
    A ChainOfThought builds the LLM query (system prompt and user message) given the context of a product field lookup.

    The context is made of:
    * a Field instance (name, type, label, options, multiple)
    * a product description
    * TBD: an example of field value (see the `examples.json` file
    """

    @abstractmethod
    def build_query(self, field: Field, description: str) -> Tuple[str, str]:
        """

        :param field:
        :param description:
        :return:
        """
        pass


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
        self._connector = connector
        self._chain_of_thoughts = chain_of_thoughts

    def lookup_field_description(self, field: Field, description: str) -> str:
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


class DumbLLaMAConnector(AbstractLLMConnector):
    def query(self, query: str) -> str:
        return "Answer LLaMA"


class DumbCameLLMConnector(AbstractLLMConnector):
    def query(self, query: str) -> str:
        return "Answer CameLL"


class BasicChainOfThoughts(AbstractChainOfThoughts):
    def build_query(self, field: Field, description: str) -> Tuple[str, str]:
        return (
            "Tu es un assistant qui m'aide à extraire des valeurs depuis un produit.",
            f"""
Product description: ${description}
Attribut : {field.name}
Options : ${', '.join(field.options if field.options is not None else [])}
""",
        )


class LLaMA(AbstractLLM):
    def __init__(self):
        super().__init__(DumbLLaMAConnector(), BasicChainOfThoughts())

    def build_query(self, system_prompt: str, user_message: str) -> str:
        # TODO: ensure built query doesn't exceed 4096 characters
        return f"""
[INST] <<SYS>>
${system_prompt}
<</SYS>>

{user_message} [/INST]
"""


class CameLLM(AbstractLLM):
    def __init__(self):
        super().__init__(DumbCameLLMConnector(), BasicChainOfThoughts())

    def build_query(self, system_prompt: str, user_message: str) -> str:
        # TODO: ensure built query doesn't exceed 2048 characters
        return f"""
[INST] <<SYS>>
${system_prompt}
<</SYS>>

{user_message} [/INST]
"""
