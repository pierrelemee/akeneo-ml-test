import pytest

from src.llm.chain_of_thoughts import ContextualChainOfThoughts
from src.models import ProductFieldValue, ProductField


class TestAbstractChainOfThoughts:
    """
    Test AbstractChainOfThoughts operations.
    """

    @pytest.fixture
    def input_field(self):
        ProductField.truncate_table(restart_identity=False, cascade=True)
        field, _ = ProductField.get_or_create(
            name="EF001438", multiple=False, label="longueur (cm)", type="number"
        )
        ProductFieldValue.create(
            name_id="EF001438",
            context="Stelrad Rad hygiène galvanisé T10,  non-habillé et sans ailettes, avec étriers, émissions à75/65/20DEGC= 1563W, connections: 4 x 1/2' F, hauteur: 500 mm, longueur: 3000 mm, couleur: Stelrad 9016, no d'article: 0108051030",
            value=3000,
        )

        return field

    def test_contextual_prompt(self, input_field: ProductField):
        chain_of_thoughts = ContextualChainOfThoughts()

        system_prompt, user_message = chain_of_thoughts.build_query(
            input_field, "Baignoire d'angle Geberit Bastia avec pieds: 142x142cm"
        )

        assert (
            system_prompt
            == 'Tu es un expert en électroménager. Quand on t\'as demandé la valeur de la propriété "longueur (cm)" sur un produit dont la description est "Stelrad Rad hygiène galvanisé T10,  non-habillé et sans ailettes, avec étriers, émissions à75/65/20DEGC= 1563W, connections: 4 x 1/2\' F, hauteur: 500 mm, longueur: 3000 mm, couleur: Stelrad 9016, no d\'article: 0108051030" tu as répondu 3000.'
        )
        assert (
            user_message
            == 'Quelle est la valeur de la propriété "longueur (cm)" pour le produit dont la description est la suivante "Baignoire d\'angle Geberit Bastia avec pieds: 142x142cm" ?'
        )
