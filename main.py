import requests
import json
import time
from datetime import datetime
from tqdm import tqdm
import re
import getpass

BASE_URL = "https://discord.com/api/v9"

def safe_name(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '_', name)
print("for help see readme: https://github.com/ROSTGG/discord-chat-import")
TOKEN = getpass.getpass("Discord token (hide): ").strip()
CHANNEL_ID = input("Channel ID: ").strip()
FORMAT = input("format (json / txt) [json]: ").strip().lower() or "json"
SLEEP = float(input("wait between request (sec) [0.4]: ") or 0.4)

HEADERS = {
    "Authorization": TOKEN,
    "User-Agent": "Mozilla/5.0"
}

channel = requests.get(
    f"{BASE_URL}/channels/{CHANNEL_ID}",
    headers=HEADERS
)

if channel.status_code != 200:
    print("error: channel access")
    exit(1)

channel = channel.json()
channel_name = safe_name(channel.get("name", "chat"))

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
OUTPUT_FILE = f"{channel_name}_{timestamp}.{FORMAT}"

MESSAGES_URL = f"{BASE_URL}/channels/{CHANNEL_ID}/messages"

raw_messages = []
before = None

pbar = tqdm(desc=f"export: {channel_name}", unit="msg")

while True:
    params = {"limit": 100}
    if before:
        params["before"] = before

    r = requests.get(MESSAGES_URL, headers=HEADERS, params=params)
    if r.status_code != 200:
        print("\nerror loading message stop:", r.status_code)
        break

    batch = r.json()
    if not batch:
        break

    raw_messages.extend(batch)
    before = batch[-1]["id"]
    pbar.update(len(batch))
    time.sleep(SLEEP)

pbar.close()

raw_messages.reverse()

id_to_text = {
    m["id"]: m["content"]
    for m in raw_messages
}

messages = []

for m in raw_messages:
    reply_id = m.get("message_reference", {}).get("message_id")

    messages.append({
        "timestamp": m["timestamp"],
        "author": m["author"]["username"],
        "content": m["content"],
        "reply_to": id_to_text.get(reply_id),
        "mentions": [u["username"] for u in m.get("mentions", [])],
        "reactions": [
            f"{r['emoji'].get('name')}×{r['count']}"
            for r in m.get("reactions", [])
        ],
        "attachments": [a["url"] for a in m.get("attachments", [])]
    })

if FORMAT == "json":
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

elif FORMAT == "txt":
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for m in messages:
            line = f"[{m['timestamp']}] {m['author']}: {m['content']}"
            if m["reply_to"]:
                line += f"\n  ↳ ответ на: {m['reply_to']}"
            if m["reactions"]:
                line += f" [reactions: {', '.join(m['reactions'])}]"
            if m["attachments"]:
                line += f" [files: {', '.join(m['attachments'])}]"
            f.write(line + "\n")

print("ready:", OUTPUT_FILE)
