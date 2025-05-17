from telethon import TelegramClient

# ЗАМЕНИ ЭТИ ДАННЫЕ НА СВОИ
api_id = 23935181  # <-- твой API ID
api_hash = '55ff4f99b4c25688f486d84e9921a229'

client = TelegramClient('emoji_session', api_id, api_hash)

async def main():
    # Получаем последние 10 сообщений из Личных сообщений (Saved Messages)
    async for message in client.iter_messages('me', limit=10):
        print("=== MESSAGE ===")
        print(message.text)
        if message.entities:
            for entity in message.entities:
                print(entity)

with client:
    client.loop.run_until_complete(main())
