import re
from app.telegram_client import client
from app.db.db import SessionLocal
from app.db.models import Hashtag, MetaKV
from app.config import WATCH_CHANNEL

def get_meta(db, key: str) -> str | None:
    entry = db.query(MetaKV).filter_by(key=key).first()
    return entry.value if entry else None

def set_meta(db, key: str, value: str):
    entry = db.query(MetaKV).filter_by(key=key).first()
    if entry:
        entry.value = value
    else:
        db.add(MetaKV(key=key, value=value))

async def extract_hashtags_from_channel():
    db = SessionLocal()
    tag_counter = {}

    try:
        last_id = int(get_meta(db, "last_scanned_msg_id") or 0)
    except ValueError:
        last_id = 0

    max_seen_id = last_id
    new_messages = 0

    async for msg in client.iter_messages(WATCH_CHANNEL, limit=100):
        if msg.id <= last_id:
            continue  # старое сообщение — пропускаем

        new_messages += 1
        max_seen_id = max(max_seen_id, msg.id)
        text = msg.message or msg.raw_text or ""
        tags = re.findall(r"#\w+", text)
        for tag in tags:
            norm = tag.lower()
            tag_counter[norm] = tag_counter.get(norm, 0) + 1

    for tag, count in tag_counter.items():
        exists = db.query(Hashtag).filter_by(tag=tag).first()
        if exists:
            exists.count += count
        else:
            db.add(Hashtag(tag=tag, count=count))

    if new_messages:
        set_meta(db, "last_scanned_msg_id", str(max_seen_id))

    db.commit()
    db.close()
    print(f"✅ Extracted {len(tag_counter)} hashtags from {new_messages} new messages.")
