import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://royalvipcanlimac.com/channels.php"
CHANNEL_BASE = "https://1029kralbettv.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": CHANNEL_BASE
}

# 1. Kaynak sayfayı çek
resp = requests.get(SOURCE_URL, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")

# 2. channel?id=... linklerini bul
channel_links = set()

for a in soup.find_all("a", href=True):
    href = a["href"]
    if href.startswith("/channel?id="):
        full_link = CHANNEL_BASE + href
        channel_links.add(full_link)

print(f"{len(channel_links)} kanal bulundu.")

# 3. kralbet.m3u dosyasına yaz
with open("kralbet.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n\n")
    for idx, link in enumerate(sorted(channel_links), 1):
        f.write(f"#EXTINF:-1 tvg-name=\"Kralbet Kanal {idx}\" group-title=\"KRALBET\",Kralbet Kanal {idx}\n")
        f.write(f"#EXTVLCOPT:http-user-agent={headers['User-Agent']}\n")
        f.write(f"#EXTVLCOPT:http-referrer={headers['Referer']}\n")
        f.write(link + "\n\n")
