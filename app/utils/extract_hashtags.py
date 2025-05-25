import re
from app.telegram_client import client
from app.db.db import SessionLocal
from app.db.models import Hashtag
from app.config import WATCH_CHANNEL

async def extract_hashtags_from_channel():
    db = SessionLocal()
    tag_counter = {}

    async for msg in client.iter_messages(WATCH_CHANNEL, limit=100):
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

    db.commit()
    db.close()
    print(f"✅ Extracted {len(tag_counter)} hashtags from channel.")
