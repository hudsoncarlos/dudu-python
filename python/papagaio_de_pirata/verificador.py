from datetime import datetime, timedelta
from python.papagaio_de_pirata.banco_dados_json import carregar_contas
from notificador import notificar
from email_alerta import enviar_email_alerta

DIAS_ALERTA = 3  # Dias antes do vencimento para avisar

def verificar_contas():
    hoje = datetime.today().date()
    contas = carregar_contas()

    mensagens = []

    for conta in contas:
        venc = datetime.strptime(conta["vencimento"], "%Y-%m-%d").date()
        dias_restantes = (venc - hoje).days

        if dias_restantes <= DIAS_ALERTA:
            msg = f"💸 {conta['nome']} vence em {dias_restantes} dia(s).\nLink: {conta['url']}"
            notificar("Conta a pagar!", msg.split('\n')[0])
            mensagens.append(msg)

    if mensagens:
        enviar_email_alerta(mensagens)

if __name__ == "__main__":
    verificar_contas()
