import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@stanleytrails")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
WATCH_CHANNEL = os.getenv("WATCH_CHANNEL", "stanleytrails")
AUTH_TOKEN = os.getenv("API_AUTH_TOKEN", "supersecrettoken")
SIGNATURE_HTML = '😾 <a href="https://t.me/stanleytrails">Азиатская бытовуха</a>'
SIGNATURE_TEXT = '😾 Азиатская бытовуха'
