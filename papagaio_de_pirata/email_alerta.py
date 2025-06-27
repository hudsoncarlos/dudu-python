import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

ARQ_CONFIG_EMAIL = "config_email.json"

def carregar_config_email():
    if not os.path.exists(ARQ_CONFIG_EMAIL):
        raise FileNotFoundError("Arquivo config_email.json não encontrado.")
    with open(ARQ_CONFIG_EMAIL, "r", encoding="utf-8") as f:
        return json.load(f)

def enviar_email_alerta(mensagens: list[str]):
    if not mensagens:
        return

    config = carregar_config_email()
    corpo = "\n\n".join(mensagens)

    msg = MIMEMultipart()
    msg["From"] = config["email_origem"]
    msg["To"] = config["email_destino"]
    msg["Subject"] = "🔔 Contas vencendo em breve"

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
