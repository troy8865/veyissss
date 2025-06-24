import requests
import re
from bs4 import BeautifulSoup

BASE_URL = "https://1029kralbettv.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": BASE_URL
}

# 1. Ana sayfayı çek
resp = requests.get(BASE_URL, headers=headers)
soup = BeautifulSoup(resp.text, 'html.parser')

# 2. channel?id=... linklerini bul
channel_links = []
for a in soup.find_all("a", href=True):
    href = a['href']
    if href.startswith("/channel?id="):
        full_url = BASE_URL + href
        if full_url not in channel_links:
            channel_links.append(full_url)

print(f"{len(channel_links)} kanal sayfası bulundu.")

# 3. Her sayfaya gir, .m3u8 linklerini ara
final_links = []

for url in channel_links:
    try:
        page = requests.get(url, headers=headers)
        found = re.findall(r'(https?://[^\s"\'<>]+\.m3u8)', page.text)
        final_links.extend(found)
    except Exception as e:
        print(f"Hata: {url} - {e}")

print(f"{len(final_links)} adet .m3u8 linki bulundu.")

# 4. kralbet.m3u dosyasına yaz
with open("kralbet.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n\n")
    for idx, link in enumerate(final_links, 1):
        f.write(f"#EXTINF:-1 tvg-name=\"Kralbet Kanal {idx}\" group-title=\"KRALBET\",Kralbet Kanal {idx}\n")
        f.write(f"#EXTVLCOPT:http-user-agent={headers['User-Agent']}\n")
        f.write(f"#EXTVLCOPT:http-referrer={headers['Referer']}\n")
        f.write(link + "\n\n")
