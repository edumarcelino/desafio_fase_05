import smtplib
import requests
import time
from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes
import os

from desafio05_00_config import (
    EMAIL_SENDER, EMAIL_RECEIVER,
    TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, CANAL_ENVIO,
    EMAIL_USE_MAILHOG,
    EMAIL_PASSWORD
)

def enviar_email(mensagem, assunto="FIAP VisionGuard", delay=1, imagem_path=None):
    msg = EmailMessage()
    msg.set_content(mensagem)
    msg["Subject"] = assunto
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    # Anexar imagem, se fornecida
    if imagem_path and os.path.exists(imagem_path):
        with open(imagem_path, "rb") as img:
            maintype, subtype = mimetypes.guess_type(imagem_path)[0].split("/")
            msg.add_attachment(img.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(imagem_path))

    try:
        if EMAIL_USE_MAILHOG:
            with smtplib.SMTP("localhost", 1025) as smtp:
                smtp.send_message(msg)
            print(f"✅ Email enviado via MailHog: {mensagem}")
        else:
            import ssl
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                smtp.send_message(msg)
            print(f"✅ Email enviado via Gmail: {mensagem}")
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
    time.sleep(delay)

def enviar_telegram(mensagem, delay=1, imagem_path=None):
    if imagem_path and os.path.exists(imagem_path):
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        with open(imagem_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': mensagem}
            response = requests.post(url, files=files, data=data)
    else:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}
        response = requests.post(url, data=data)

    try:
        if response.status_code == 200:
            print(f"✅ Telegram enviado: {mensagem}")
        else:
            print(f"❌ Telegram falhou: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"⚠️ Erro Telegram: {e}")
    time.sleep(delay)

def enviar_alerta(mensagem, via=CANAL_ENVIO, imagem_path=None):
    if via == "telegram":
        enviar_telegram(mensagem, imagem_path=imagem_path)
    elif via == "email":
        enviar_email(mensagem, imagem_path=imagem_path)
    else:
        print(f"⚠️ Canal desconhecido: {via}")
