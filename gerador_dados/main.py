from gerador_dados import gerar_lista_dados
from exportador import salvar_em_csv, salvar_em_json

dados = gerar_lista_dados(quantidade=10)

salvar_em_csv(dados, "saida/tolkien.csv")
salvar_em_json(dados, "saida/tolkien.json")

print("✅ Arquivos gerados em 'saida/'")
