from fastapi import APIRouter
from collections import Counter
from app.utils.hashtags import extract_hashtags_from_text
from app.config import WATCH_CHANNEL
from app.telegram_client import client

router = APIRouter()

@router.get("/hashtags")
async def get_hashtags():
    counter = Counter()
    async for msg in client.iter_messages(WATCH_CHANNEL, limit=50):
        text = msg.message or msg.raw_text or ""
        found = extract_hashtags_from_text(text)
        counter.update(tag for tag in found)

    return [
        {"tag": tag, "count": count} for tag, count in counter.most_common()
    ]
