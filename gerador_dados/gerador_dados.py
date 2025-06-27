from faker import Faker
from faker_tolkiendiano import TolkienProvider
import random

def gerar_lista_dados(quantidade=5):
    fake = Faker('pt_BR')
    fake.add_provider(TolkienProvider)

    lista = []
    for _ in range(quantidade):
        endereco = fake.street_name()
        numero = random.randint(1, 9999)
        bairro = fake.bairro()
        cidade = fake.city()
        estado = fake.estado_nome()
        cep = fake.postcode()

        pessoa = {
            "nome": fake.name(),
            "cpf": fake.cpf(),
            "data_nascimento": fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%d/%m/%Y"),
            "email": fake.email(),
            "telefone": fake.phone_number(),
            "endereco": f"{endereco}, {numero}",
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep,
            "país": "Brasil",

            "personagem": fake.personagem_tolkiendiano(),
            "raça": fake.raça_tolkiendiana(),
            "lugar": fake.lugar_tolkiendiano(),
            "idioma": fake.lingua_tolkiendiana(),
            "item_mágico": fake.item_magico_tolkiendiano()
        }
        lista.append(pessoa)

    return lista
