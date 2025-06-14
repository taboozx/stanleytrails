import os, shutil, asyncio
from fastapi import FastAPI, UploadFile, Form, HTTPException, Depends, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from telethon import events, functions, types
from datetime import datetime, timedelta
from datetime import datetime, timedelta, timezone

from telethon import events, functions
from datetime import datetime, timedelta, timezone

from telethon.tl.types import Message
from telethon import events
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetRepliesRequest
from telethon.errors import MsgIdInvalidError
from datetime import datetime

from app.api import hashtags_api
from app.telegram_client import client
from app.utils.extract_hashtags import extract_hashtags_from_channel
from typing import List
from collections import defaultdict
import logging


from app.config import (
    CHANNEL_USERNAME, FRONTEND_ORIGIN,
    WATCH_CHANNEL, AUTH_TOKEN,
    SIGNATURE_HTML, SIGNATURE_TEXT
)
from app.schemas.contest import ContestRunRequest

SIGNATURE_HTML = '😾 <a href="https://t.me/stanleytrails">Азиатская бытовуха</a>'
SIGNATURE_TEXT = '😾 Азиатская бытовуха'


# 🌐 FastAPI app
app = FastAPI()
app.include_router(hashtags_api.router)

# 🌐 CORS setup
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

# 🟢 Startup event: launch Telegram client and background task
@app.on_event("startup")
async def startup():
    await client.start()
    asyncio.create_task(periodic_hashtag_scan())
    asyncio.create_task(auto_signature_watcher())

# 🕰 Background watcher: check and fix message signatures
async def auto_signature_watcher():
    channel_peer = await client.get_input_entity(WATCH_CHANNEL)
    await client(GetFullChannelRequest(channel_peer))

    async for msg in client.iter_messages(channel_peer, limit=30):
        text = msg.message or msg.raw_text or ""
        if not text:
            continue

        count_text = text.count(SIGNATURE_TEXT)
        count_html = text.count(SIGNATURE_HTML)
        total_signs = count_text + count_html

        if total_signs == 1 and text.strip().endswith(SIGNATURE_TEXT):
            continue

        try:
            edited = format_caption(text)
            await msg.edit(edited, parse_mode="HTML")
            print(f"[CLEANED + SIGNED] ID {msg.id}")
        except Exception as e:
            print(f"[CLEAN ERROR] {msg.id} → {e}")

        try:
            await client(
                GetRepliesRequest(
                    peer=channel_peer,
                    msg_id=msg.id,
                    offset_id=0,
                    offset_date=None,
                    add_offset=0,
                    limit=1,
                    max_id=0,
                    min_id=0,
                    hash=0,
                )
            )
        except MsgIdInvalidError as e:
            logging.error(f"[REPLY ERROR] {msg.id} → {e}")
            continue

# 🔔 Realtime signature handler
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

# 🧠 Caption formatter

def format_caption(text: str) -> str:
    while SIGNATURE_HTML in text:
        text = text.replace(SIGNATURE_HTML, "")
    while SIGNATURE_TEXT in text:
        text = text.replace(SIGNATURE_TEXT, "")

    text = text.strip()
    while text.endswith("\n") or text.endswith(" "):
        text = text.rstrip()

    parts = text.split('\n', 1)
    title = parts[0]
    body = parts[1] if len(parts) > 1 else ""

    if not title.startswith("<b>") and len(title.split()) <= 4:
        title = f"<b>{title}</b>"

    result = f"{title}\n\n{body.strip()}\n\n{SIGNATURE_HTML}"
    return result.strip()

# 📤 Upload API
@app.post("/publish/")
async def publish(
    type: str = Form(None),
    title: str = Form(None),
    description: str = Form(...),
    media: List[UploadFile] = File(None),
    credentials: HTTPAuthorizationCredentials = Depends(verify_token),
):
    logger = logging.getLogger("uvicorn")

    logger.info("📥 Incoming POST /publish/")
    logger.info(f"📝 Title: {title}")
    logger.info(f"🧾 Description: {description}")
    logger.info(f"🖼 Files: {[file.filename for file in media] if media else 'No files'}")

    since = datetime.utcnow() - timedelta(days=data.days)
    if title and title.strip():
        caption += f"<b>{title.strip()}</b>"
    if description.strip():
        if caption:
    reacted: set[tuple[int, int]] = set()
        # \u2795 Count reactions
        offset = None
        while True:
            res = await client(
                functions.messages.GetMessageReactionsListRequest(
                    peer=WATCH_CHANNEL,
                    id=msg.id,
                    limit=100,
                    reaction=None,
                    offset=offset,
                )
            )

            for rec in res.reactions:
                uid = getattr(rec.peer_id, "user_id", None)
                if uid is None:
                    continue
                key = (uid, msg.id)
                if key in reacted:
                    continue
                reacted.add(key)
                scores[uid] += 1

            if not res.next_offset:
                break
            offset = res.next_offset

        # \u2795 Count comments
                    offset_date=None,

        try:
            await client.send_message(
                CHANNEL_USERNAME,
                caption,
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")
            return {"status": "error", "detail": str(e)}
    else:
        # Отправка медиа по очереди
        os.makedirs("./temp", exist_ok=True)
        for idx, file in enumerate(media):
            path = f"./temp/{file.filename}"
            with open(path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            try:
                await client.send_file(
                    CHANNEL_USERNAME,
                    path,
                    caption=caption if idx == 0 else None,  # подпись только к первому
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"❌ Failed to send file {file.filename}: {e}")
                return {"status": "error", "detail": str(e)}

    return {"status": "ok", "text": caption}


async def periodic_hashtag_scan():
    while True:
        print("🕵️‍♂️ Запуск фонового сканирования хэштегов")
        try:
            await asyncio.sleep(5)
            await extract_hashtags_from_channel()
            print(f"✅ Хэштеги обновлены ({datetime.now().isoformat()})")
        except Exception as e:
            print(f"❌ Ошибка при сканировании: {e}")
        await asyncio.sleep(86400)  # 24 часа


@app.post("/contest/run")
async def contest_run(
    data: ContestRunRequest, credentials: HTTPAuthorizationCredentials = Depends(verify_token)
):
    since = datetime.now(timezone.utc) - timedelta(days=data.days)
    scores: dict[int, int] = defaultdict(int)
    reacted: set[tuple[int, int]] = set()


    full = await client(functions.channels.GetFullChannelRequest(channel=WATCH_CHANNEL))
    _ = full.full_chat.linked_chat_id  # ensure discussion chat exists

    async for msg in client.iter_messages(WATCH_CHANNEL):
        if msg.date < since:
            break
        # \u2795 Count reactions
        offset = None
        while True:
            try:
                res = await client(
                    functions.messages.GetMessageReactionsListRequest(
                        peer=WATCH_CHANNEL,
                        id=msg.id,
                        limit=100,
                        reaction=None,
                        offset=offset,
                    )
                )
            except Exception as e:
                logging.error(f"❌ Reactions error on msg {msg.id}: {e}")
                break

            for rec in res.reactions:
                uid = getattr(rec.peer_id, "user_id", None)
                if uid is None:
                    continue
                key = (uid, msg.id)
                if key in reacted:
                    continue
                reacted.add(key)
                scores[uid] += 1

            if not res.next_offset:
                break
            offset = res.next_offset

        # \u2795 Count comments
        offset_id = 0
        while True:
            try:
                r = await client(
                    functions.messages.GetRepliesRequest(
                        peer=WATCH_CHANNEL,
                        msg_id=msg.id,
                        offset_id=offset_id,
                        offset_date=None,
                        add_offset=0,
                        limit=100,
                        max_id=0,
                        min_id=0,
                        hash=0,
                    )
                )
            except TypeError as e:
                logging.error(f"❌ GetReplies error on msg {msg.id}: {e}")
                break

        offset_id = 0
        while True:
            r = await client(
                functions.messages.GetRepliesRequest(
                    peer=WATCH_CHANNEL,
                    msg_id=msg.id,
                    offset_id=offset_id,
                    offset_date=None,  # required; no offset_peer in Telethon
                    add_offset=0,
                    limit=100,
                    max_id=0,
                    min_id=0,
                    hash=0,
                )
            )

            if not r.messages:
                break

            for c in r.messages:
                uid = getattr(c.from_id, "user_id", None)
                if not uid or c.date < since:
                    continue
                key = (uid, msg.id)
                if key in counted:
                    continue
                counted.add(key)
                scores[uid] += 2

            offset_id = r.messages[-1].id

    sorted_users = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    winners = []
    for uid, score in sorted_users[: data.winners_count]:
        try:
            user = await client.get_entity(uid)
            username = user.username or (user.first_name or "")
            if user.last_name:
                username = f"{username} {user.last_name}".strip()
            username = username.strip() or str(uid)
        except Exception:
            username = str(uid)

        text = data.message.replace("@username", f"@{username}")
        try:
            await client.send_message(uid, text)
        except Exception as e:
            print(f"❌ Failed to notify {uid}: {e}")

        winners.append({"username": username, "score": score})

    return {"status": "ok", "winners": winners}
