import json
from datetime import datetime, timedelta
import webbrowser
import os

# Configurações
DIAS_AVISO = 3  # Quantos dias antes do vencimento alertar

# Caminho do arquivo de contas
ARQUIVO_CONTAS = os.path.join(os.path.dirname(__file__), "contas.json")

def carregar_contas():
    with open(ARQUIVO_CONTAS, "r") as f:
        return json.load(f)

def verificar_vencimentos(contas, dias_aviso):
    hoje = datetime.today().date()
    for conta in contas:
        nome = conta["nome"]
        url = conta["url"]
        vencimento = datetime.strptime(conta["vencimento"], "%Y-%m-%d").date()

        dias_restantes = (vencimento - hoje).days

        if 0 <= dias_restantes <= dias_aviso:
            print(f"🔔 Conta '{nome}' vence em {dias_restantes} dias! Acesse: {url}")
            abrir = input("Deseja abrir o site agora? (s/n): ").strip().lower()
            if abrir == "s":
                webbrowser.open(url)

def main():
    try:
        contas = carregar_contas()
        verificar_vencimentos(contas, DIAS_AVISO)
    except FileNotFoundError:
        print("❌ Arquivo de contas não encontrado.")
    except Exception as e:
        print(f"⚠️ Erro: {e}")

if __name__ == "__main__":
    main()
