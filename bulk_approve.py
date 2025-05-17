import os
import json
from telethon.sync import TelegramClient
from telethon.tl.types import User
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
group = os.getenv("CERBER_GROUP", "@cerber_gate")
APPROVED_FILE = "approved_users.json"

def load_approved_users():
    if not os.path.exists(APPROVED_FILE):
        return set()
    with open(APPROVED_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))

def save_approved_users(user_ids):
    with open(APPROVED_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(list(user_ids)), f)

client = TelegramClient("userbot", api_id, api_hash)

with client:
    participants = client.get_participants(group)
    approved = load_approved_users()
    added = 0

    for user in participants:
        if isinstance(user, User) and not user.bot:
            if user.id not in approved:
                approved.add(user.id)
                added += 1

    save_approved_users(approved)
    print(f"[BULK ADD] Добавлено новых пользователей: {added}")
