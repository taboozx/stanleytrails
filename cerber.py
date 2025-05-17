import os
import json
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events, Button
from telethon.tl.types import User

load_dotenv()

# 🔐 Telegram credentials
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
cerber_group = os.getenv("CERBER_GROUP", "@cerber_gate")
approved_file = "approved_users.json"
session_name = "cerber"  # creates cerber.session separately

# 🗂 Init client
client = TelegramClient(session_name, api_id, api_hash)

# ✅ Работа с approved_users.json
def load_approved_users():
    if not os.path.exists(approved_file):
        return set()
    with open(approved_file, "r", encoding="utf-8") as f:
        try:
            return set(json.load(f))
        except json.JSONDecodeError:
            return set()

def save_approved_users(user_ids):
    with open(approved_file, "w", encoding="utf-8") as f:
        json.dump(sorted(list(user_ids)), f, indent=2)

# 👁 Реакция на вступление
@client.on(events.ChatAction(chats=cerber_group))
async def handle_new_member(event):
    if event.user_joined or event.user_added:
        user = await event.get_user()
        approved = load_approved_users()

        if user.bot or not isinstance(user, User):
            return

        if user.id in approved:
            print(f"[CERBER] {user.id} уже подтверждён — не трогаем.")
            return

        try:
            await client.send_message(
                user.id,
                (
                    "👋 Добро пожаловать в группу!\n\n"
                    "Подтвердите, что вы не имеете претензий к контенту, "
                    "даже если он может задевать культурные, моральные или религиозные убеждения.\n\n"
                    "Нажмите кнопку ниже, чтобы остаться."
                ),
                buttons=[Button.inline("✅ Согласен", b"cerber_ok")]
            )
            print(f"[CERBER] Сообщение отправлено {user.id}")

            # ⏳ Старт таймера на 5 минут
            asyncio.create

# 🎯 Обработка подтверждения
@client.on(events.CallbackQuery(data=b"cerber_ok"))
async def approve_user(event):
    user_id = event.sender_id
    approved = load_approved_users()

    if user_id not in approved:
        approved.add(user_id)
        save_approved_users(approved)
        print(f"[CERBER ✅] Подтверждён: {user_id}")

    await event.respond("✅ Спасибо! Вы подтверждены.")
    await client.send_message(user_id, "👉 Вход разрешён. Добро пожаловать!")

# 🚀 Запуск
async def main():
    await client.start()
    print("[CERBER] Стартовал. Охраняю группу...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
