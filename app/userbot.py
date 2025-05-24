import os, shutil, asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from telethon import TelegramClient, events
from telethon.tl.types import Message

# # 🔐 Load env
# load_dotenv()

# # 🧾 Config
# api_id = int(os.getenv("API_ID"))
# api_hash = os.getenv("API_HASH")
# channel_username = os.getenv("CHANNEL_USERNAME", "@stanleytrails")
# frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
# WATCH_CHANNEL = os.getenv("WATCH_CHANNEL", "stanleytrails")
# AUTH_TOKEN = os.getenv("API_AUTH_TOKEN", "supersecrettoken")

from app.config import (
    API_ID, API_HASH,
    CHANNEL_USERNAME, FRONTEND_ORIGIN,
    WATCH_CHANNEL, AUTH_TOKEN,
    SIGNATURE_HTML, SIGNATURE_TEXT
)
SIGNATURE_HTML = '😾 <a href="https://t.me/stanleytrails">Азиатская бытовуха</a>'
SIGNATURE_TEXT = '😾 Азиатская бытовуха'

# 🚀 Init
client = TelegramClient("userbot", API_ID, API_HASH)
app = FastAPI()

# 🌐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 Security
security = HTTPBearer()
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

# 🟢 Startup
@app.on_event("startup")
async def startup():
    await client.start()
    asyncio.create_task(auto_signature_watcher())

# 🕰 Background: подписывает всё без подписи
async def auto_signature_watcher():
    async for msg in client.iter_messages(WATCH_CHANNEL, limit=30):
        text = msg.message or msg.raw_text or ""
        if not text:
            continue

        # Проверяем — если больше одной подписи, надо чистить
        count_text = text.count(SIGNATURE_TEXT)
        count_html = text.count(SIGNATURE_HTML)
        total_signs = count_text + count_html

        if total_signs == 1 and text.strip().endswith(SIGNATURE_TEXT):
            continue  # Всё хорошо, одна подпись в конце — пропускаем

        try:
            edited = format_caption(text)
            await msg.edit(edited, parse_mode="HTML")
            print(f"[CLEANED + SIGNED] ID {msg.id}")
        except Exception as e:
            print(f"[CLEAN ERROR] {msg.id} → {e}")



# 🔔 Realtime подписка
@client.on(events.NewMessage(chats=WATCH_CHANNEL))
async def realtime_signature_handler(event):
    msg = event.message
    content = msg.message or msg.raw_text or ""
    if not content or SIGNATURE_TEXT in content:
        return
    try:
        new_text = format_caption(content)
        await msg.edit(new_text, parse_mode="HTML")
        print(f"[REALTIME SIGNED] ID {msg.id}")
    except Exception as e:
        print(f"[REALTIME ERROR] {msg.id} → {e}")

# 🧠 Format logic
def format_caption(text: str) -> str:
    # Удаляем все варианты подписи
    while SIGNATURE_HTML in text:
        text = text.replace(SIGNATURE_HTML, "")
    while SIGNATURE_TEXT in text:
        text = text.replace(SIGNATURE_TEXT, "")

    text = text.strip()

    # Удаляем пустые строки и пробелы в конце
    while text.endswith("\n") or text.endswith(" "):
        text = text.rstrip()

    # Разделяем заголовок и тело
    parts = text.split('\n', 1)
    title = parts[0]
    body = parts[1] if len(parts) > 1 else ""

    # Оборачиваем заголовок в <b> если короткий
    if not title.startswith("<b>") and len(title.split()) <= 4:
        title = f"<b>{title}</b>"

    # Добавляем в конец
    result = f"{title}\n\n{body.strip()}\n\n{SIGNATURE_HTML}"
    return result.strip()



# 📤 Upload API
@app.post("/publish/")
async def publish(
    type: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = Form(...),
    credentials: HTTPAuthorizationCredentials = Depends(verify_token),
):
    os.makedirs("./temp", exist_ok=True)
    path = f"./temp/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    caption = f"<b>{title}</b>"
    if description.strip():
        caption += f"\n\n{description.strip()}"

    try:
        await client.send_file(CHANNEL_USERNAME, path, caption=caption, parse_mode="HTML")
    except Exception as e:
        return {"status": "error", "detail": str(e)}

    return {"status": "ok", "file": file.filename}
