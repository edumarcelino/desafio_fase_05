import os
from dotenv import load_dotenv

load_dotenv("config.env")

CANAL_ENVIO = os.getenv("CANAL_ENVIO", "email")

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

EMAIL_USE_MAILHOG = True  # Defina como False para usar o Gmail
