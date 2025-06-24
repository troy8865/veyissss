import requests
from bs4 import BeautifulSoup

BASE_URL = "https://1029kralbettv.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": BASE_URL
}

# Ana sayfadan channel?id= linklerini topla
response = requests.get(BASE_URL, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

channel_links = set()  # DEĞİŞKEN BURADA TANIMLANIYOR

for a in soup.find_all("a", href=True):
    href = a["href"]
    if href.startswith("/channel?id="):
        full_link = BASE_URL + href
        channel_links.add(full_link)

print(f"{len(channel_links)} adet channel linki bulundu.")

print("Kralbet.m3u dosyasına yazılıyor...")

with open("kralbet.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n\n")
    for idx, link in enumerate(sorted(channel_links), 1):
        f.write(f"#EXTINF:-1 tvg-name=\"Kralbet Kanal {idx}\" group-title=\"KRALBET\",Kralbet Kanal {idx}\n")
        f.write(f"#EXTVLCOPT:http-user-agent={headers['User-Agent']}\n")
        f.write(f"#EXTVLCOPT:http-referrer={headers['Referer']}\n")
        f.write(link + "\n\n")

print(f"{len(channel_links)} kanal kralbet.m3u dosyasına yazıldı.")
