import json
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import webbrowser
import os

# Configurações
DIAS_AVISO = 3
ARQ_CONTAS = os.path.join(os.path.dirname(__file__), "contas.json")
ARQ_CONFIG_EMAIL = os.path.join(os.path.dirname(__file__), "config_email.json")

def carregar_json(caminho):
    with open(caminho, "r") as f:
        return json.load(f)

def enviar_email(alertas, config):
    if not alertas:
        return

    corpo = "\n".join(alertas)

    msg = MIMEMultipart()
    msg["From"] = config["email_origem"]
    msg["To"] = config["email_destino"]
    msg["Subject"] = "🔔 Alerta de vencimento de contas"

    msg.attach(MIMEText(corpo, "plain"))

    try:
        server = smtplib.SMTP(config["smtp"], config["porta"])
        server.starttls()
        server.login(config["email_origem"], config["senha"])
        server.sendmail(config["email_origem"], config["email_destino"], msg.as_string())
        server.quit()
        print("📧 E-mail enviado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")

def verificar_vencimentos(contas, dias_aviso):
    hoje = datetime.today().date()
    alertas = []

    for conta in contas:
        nome = conta["nome"]
        url = conta["url"]
        vencimento = datetime.strptime(conta["vencimento"], "%Y-%m-%d").date()
        dias_restantes = (vencimento - hoje).days

        if 0 <= dias_restantes <= dias_aviso:
            msg = f"🔔 Conta '{nome}' vence em {dias_restantes} dias!\nLink: {url}"
            print(msg)
            alertas.append(msg)

            abrir = input("Deseja abrir o site agora? (s/n): ").strip().lower()
            if abrir == "s":
                webbrowser.open(url)

    return alertas

def main():
    try:
        contas = carregar_json(ARQ_CONTAS)
        config_email = carregar_json(ARQ_CONFIG_EMAIL)
        alertas = verificar_vencimentos(contas, DIAS_AVISO)
        enviar_email(alertas, config_email)
    except FileNotFoundError as e:
        print(f"❌ Arquivo não encontrado: {e}")
    except Exception as e:
        print(f"⚠️ Erro: {e}")

if __name__ == "__main__":
    main()
