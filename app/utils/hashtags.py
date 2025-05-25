import os
import json
import re

HASHTAG_FILE = "hashtag_storage/hashtags.json"

def extract_hashtags_from_text(text: str):
    return re.findall(r"#([^\s#]+)", text)

def load_hashtags():
    if not os.path.exists(HASHTAG_FILE):
        return []
    with open(HASHTAG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_hashtags(new_tags):
    tags = set(load_hashtags())
    tags.update(new_tags)
    with open(HASHTAG_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(tags), f, ensure_ascii=False, indent=2)

def update_hashtags_from_post(text: str):
    hashtags = extract_hashtags_from_text(text)
    if hashtags:
        save_hashtags(hashtags)
