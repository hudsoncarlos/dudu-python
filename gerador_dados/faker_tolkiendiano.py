from faker.providers import BaseProvider
import random

class TolkienProvider(BaseProvider):
    personagens = [
        "Frodo", "Gandalf", "Bilbo", "Aragorn", "Roverandom",
        "Sr. Boaventura de Bolsin", "Beren", "Lúthien", "Melian",
        "Feanor", "Glorfindel", "Eärendil", "Tom Bombadil"
    ]
    raças = ["Hobbit", "Elfo", "Anão", "Homem", "Maiar", "Valar", "Ent", "Dragão"]
    lugares = [
        "Valfenda", "Condado", "Mordor", "Gondor", "Rohan",
        "Angband", "Aman", "Floresta das Trevas", "Númenor"
    ]
    línguas = ["Quenya", "Sindarin", "Westron", "Valarin", "Entês"]
    itens = ["O Um Anel", "Silmaril", "Andúril", "Cajado de Gandalf", "Arkenstone"]

    def personagem_tolkiendiano(self):
        return random.choice(self.personagens)

    def raça_tolkiendiana(self):
        return random.choice(self.raças)

    def lugar_tolkiendiano(self):
        return random.choice(self.lugares)

    def lingua_tolkiendiana(self):
        return random.choice(self.línguas)

    def item_magico_tolkiendiano(self):
        return random.choice(self.itens)
