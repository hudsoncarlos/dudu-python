from banco_sqlite import inicializar_banco, adicionar_conta, listar_contas

inicializar_banco()
adicionar_conta("Cartão Nubank", "2025-06-01", "https://nubank.com.br")
contas = listar_contas()
for c in contas:
    print(c)
