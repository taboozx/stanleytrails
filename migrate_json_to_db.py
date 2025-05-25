import json
from app.db.db import SessionLocal
from app.db.models import Hashtag, ApprovedUser

db = SessionLocal()

# Миграция тегов
try:
    with open("hashtag_storage/hashtags.json", "r", encoding="utf-8") as f:
        raw = json.load(f)
        for tag, count in raw.items():
            db.add(Hashtag(tag=tag, count=count))
    print("✅ Hashtags migrated")
except FileNotFoundError:
    print("⚠️ hashtags.json not found")

# Миграция одобренных пользователей
try:
    with open("approved_users.json", "r", encoding="utf-8") as f:
        raw = json.load(f)
        for user in raw:
            db.add(ApprovedUser(tg_id=str(user)))
    print("✅ Approved users migrated")
except FileNotFoundError:
    print("⚠️ approved_users.json not found")

db.commit()
db.close()
print("✅ Migration complete")
