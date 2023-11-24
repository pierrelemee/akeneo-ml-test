from abc import ABC, abstractmethod
from typing import Tuple

from src.models.product import Field


class AbstractChainOfThoughts(ABC):
    """
    A ChainOfThought builds the LLM query (system prompt and user message) given the context of a product field lookup,
    and extracts data from the output.

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

    def process_output(self, output: str):
        """
        Processes the output and return relevant data.

        :param output:
        :return: a list, object, string, number or even None
        """
        return output


class BasicChainOfThoughts(AbstractChainOfThoughts):
    """
    Builds a very basic query, with a static system prompt and a bullet points-styled user message.

    Based on the given example.
    """

    def build_query(self, field: Field, description: str) -> Tuple[str, str]:
        return (
            "Tu es un assistant qui m'aide à extraire des valeurs depuis un produit.",
            f"""
Product description: ${description}
Attribut : {field.name}
Options : ${', '.join(field.options if field.options is not None else [])}
""",
        )
