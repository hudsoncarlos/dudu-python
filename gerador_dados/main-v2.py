from gerador_dados import gerar_lista_dados
from exportador import salvar_em_csv, salvar_em_json
import pprint

def main():
    print("🧙‍♂️ Gerador de dados pessoais + Tolkien")
    qtd = input("Quantos registros deseja gerar? (padrão: 5) ")
    qtd = int(qtd) if qtd.strip().isdigit() else 5

    dados = gerar_lista_dados(qtd)

    # Exibir no terminal com indentação bonita
    print("\n📋 Dados Gerados:\n")
    for pessoa in dados:
        pprint.pprint(pessoa)
        print("-" * 50)

    # Pergunta se deseja salvar
    salvar = input("\nDeseja salvar os dados em arquivo? (s/n): ").lower()
    if salvar == "s":
        salvar_em_csv(dados, "saida/tolkien.csv")
        salvar_em_json(dados, "saida/tolkien.json")
        print("\n💾 Arquivos salvos em 'saida/tolkien.csv' e 'saida/tolkien.json'")
    else:
        print("\n❌ Dados não foram salvos.")

if __name__ == "__main__":
    main()
