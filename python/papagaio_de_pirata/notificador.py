from plyer import notification

def notificar(titulo, mensagem):
    try:
        notification.notify(
            title=titulo,
            message=mensagem,
            timeout=10  # segundos
        ) # type: ignore
        print(f"🔔 Notificação enviada: {titulo}")
    except Exception as e:
        print(f"❌ Falha ao notificar: {e}")
