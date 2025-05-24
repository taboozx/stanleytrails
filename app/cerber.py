import os
import json
import asyncio
from fastapi import FastAPI
from telethon import TelegramClient, events, Button
from telethon.tl.types import User
from app.config import API_ID, API_HASH, STANLEYTRAILS_GROUP

app = FastAPI()

client = TelegramClient("cerber", API_ID, API_HASH)
approved_users_file = "approved_users.json"

# Загрузка / сохранение одобренных пользователей
def load_approved():
    if not os.path.exists(approved_users_file):
        return set()
    with open(approved_users_file, "r") as f:
        return set(json.load(f))

def save_approved(data):
    with open(approved_users_file, "w") as f:
        json.dump(sorted(list(data)), f, indent=2)

# Ловим вступление в группу
@client.on(events.ChatAction(chats=STANLEYTRAILS_GROUP))
async def handle_join(event):
    if not (event.user_joined or event.user_added):
        return

    user = await event.get_user()
    if user.bot or not isinstance(user, User):
        return

    approved = load_approved()
    if user.id in approved:
        return

    msg = await client.send_message(
        STANLEYTRAILS_GROUP,
        f"@{user.username or user.first_name}, пожалуйста подтвердите согласие с правилами:",
        buttons=[Button.inline("✅ Согласен", f"ok:{user.id}".encode())]
    )

    try:
        await client.pin_message(STANLEYTRAILS_GROUP, msg.id, notify=False)
    except:
        pass

    async def check_later():
        await asyncio.sleep(60)
        if user.id not in load_approved():
            try:
                await client.delete_messages(STANLEYTRAILS_GROUP, msg.id)
                await client.kick_participant(STANLEYTRAILS_GROUP, user.id)
                print(f"[CERBER 🔨] {user.id} не подтвердил — удалён")
            except Exception as e:
                print(f"[CERBER ❌] Ошибка удаления {user.id}: {e}")
        else:
            await client.delete_messages(STANLEYTRAILS_GROUP, msg.id)

    asyncio.create_task(check_later())

# Обработка нажатия на кнопку
@client.on(events.CallbackQuery)
async def confirm(event):
    data = event.data.decode()
    if not data.startswith("ok:"):
        return

    expected_id = int(data.split(":")[1])
    if event.sender_id != expected_id:
        await event.answer("⛔ Не трогай чужую кнопку", alert=True)
        return

    approved = load_approved()
    if event.sender_id not in approved:
        approved.add(event.sender_id)
        save_approved(approved)
        print(f"[CERBER ✅] Подтверждён: {event.sender_id}")

    await event.answer("✅ Спасибо, вы подтверждены")
    try:
        await client.delete_messages(STANLEYTRAILS_GROUP, event.message_id)
    except:
        pass

# FastAPI и Telethon вместе
@app.on_event("startup")
async def startup():
    await client.start()
    print("[CERBER] Стартовал в @stanleytrails")
    asyncio.create_task(client.run_until_disconnected())
