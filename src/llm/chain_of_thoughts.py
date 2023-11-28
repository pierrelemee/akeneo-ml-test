from abc import ABC, abstractmethod
from typing import Tuple

from src.models import ProductField


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
    def build_query(self, field: ProductField, description: str) -> Tuple[str, str]:
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

    def build_query(self, field: ProductField, description: str) -> Tuple[str, str]:
        return (
            "Tu es un assistant qui m'aide à extraire des valeurs depuis un produit.",
            f"""
Product description: ${description}
Attribut : {field.name}
Options : ${', '.join(field.options if field.options is not None else [])}
""",
        )


class ContextualChainOfThoughts(AbstractChainOfThoughts):
    """
    Builds a query giving some context to the LLM: you're an expert in household appliances who already gave
    relevant answers.

    This can be achieved by fetching the first ProductFieldValues related to the given ProductField.
    """

    def build_query(self, field: ProductField, description: str) -> Tuple[str, str]:
        return (
            f'Tu es un expert en électroménager. Quand on t\'as demandé la valeur de la propriété "{field.label}" sur un produit dont la description est "{field.values[0].context}" tu as répondu {field.values[0].value}.',
            f'Quelle est la valeur de la propriété "{field.label}" pour le produit dont la description est la suivante "{description}" ?',
        )
