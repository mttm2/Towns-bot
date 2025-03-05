import requests
import random
import re

# Файл с токеном и ID каналов
DATA_FILE = "data.txt"
MSG_FILE = "msg.txt"

# Расширенный список User-Agent заголовков для большей рандомизации
USER_AGENTS = [
    # Chrome (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    
    # Firefox (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
    
    # Edge (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.0.0",
    
    # Chrome (Mac)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    
    # Safari (Mac)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.0 Safari/537.36",

    # Chrome (Android)
    "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
    
    # Safari (iOS)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/537.36",
]

def load_data():
    """Загружает токен и ID каналов из файла data.txt"""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        data = {}
        for line in lines:
            key, value = line.strip().split("=", 1)
            data[key] = value.strip()

        token = data.get("TOKEN", "")
        channel_ids = [ch.strip() for ch in data.get("CHANNEL_IDS", "").split(",") if ch.strip()]

        if not token or not channel_ids:
            print("❌ Ошибка: Файл data.txt некорректно заполнен.")
            return None, None

        return token, channel_ids
    except Exception as e:
        print(f"❌ Ошибка чтения data.txt: {e}")
        return None, None

def clean_message(text):
    """Фильтрует сообщения, убирая эмодзи Discord и ссылки"""
    text = re.sub(r"<a?:\w+:\d+>", "", text)  # Убираем эмодзи Discord
    text = re.sub(r"https?://\S+", "", text)  # Убираем ссылки
    text = re.sub(r"<#\d+>", "", text)  # Убираем ссылки на каналы (<#123456789>)
    text = text.strip()  # Убираем пробелы в начале и конце
    return text if text else None  # Возвращаем None, если после очистки текст пуст

def get_messages(channel_id, token, limit=50):
    """Получает последние сообщения из канала Discord"""
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}"
    headers = {
        "Authorization": token,  # Авторизация через self-bot
        "User-Agent": random.choice(USER_AGENTS),  # Случайный User-Agent
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        raw_messages = [msg["content"].strip() for msg in response.json() if msg["content"].strip()]
        filtered_messages = [clean_message(msg) for msg in raw_messages if clean_message(msg)]  # Фильтруем
        return filtered_messages
    else:
        print(f"❌ Ошибка {response.status_code} при получении сообщений из канала {channel_id}.")
        return []

def save_messages(messages):
    """Сохраняет уникальные сообщения в msg.txt"""
    try:
        with open(MSG_FILE, "r", encoding="utf-8") as file:
            existing_messages = set(file.read().splitlines())  
    except FileNotFoundError:
        existing_messages = set()

    new_messages = set(messages) - existing_messages  

    if new_messages:
        with open(MSG_FILE, "a", encoding="utf-8") as file:
            for msg in new_messages:
                file.write(msg + "\n")
        print(f"✅ Добавлено {len(new_messages)} новых сообщений в msg.txt")
    else:
        print("⚠️ Нет новых сообщений")

if __name__ == "__main__":
    token, channel_ids = load_data()
    if token and channel_ids:
        all_messages = []
        for channel_id in channel_ids:
            print(f"📥 Получаю сообщения из канала {channel_id}...")
            all_messages.extend(get_messages(channel_id, token))

        save_messages(all_messages)
