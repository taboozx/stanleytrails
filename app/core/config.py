import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
AUTH_TOKEN = os.getenv("API_AUTH_TOKEN")

CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@stanleytrails")
WATCH_CHANNEL = os.getenv("WATCH_CHANNEL", "stanleytrails")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
STANLEYTRAILS_GROUP = os.getenv("WATCH_CHANNEL", "stanleytrails")


CERBER_GROUP = os.getenv("CERBER_GROUP", "@cerber_gate")

SIGNATURE_HTML = '😾 <a href="https://t.me/stanleytrails">Азиатская бытовуха</a>'
SIGNATURE_TEXT = '😾 Азиатская бытовуха'

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
