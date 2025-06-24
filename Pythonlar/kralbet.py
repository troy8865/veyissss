import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://1029kralbettv.com"
}

url = "https://1029kralbettv.com"

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# M3U8 bağlantılarını bul
m3u8_links = []
for link in soup.find_all("a", href=True):
    href = link["href"]
    if ".m3u8" in href:
        name = link.get_text(strip=True) or "Kral Kanal"
        m3u8_links.append((name, href))

# .m3u dosyasına yaz
with open("kralbet.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for name, link in m3u8_links:
        f.write(f"#EXTINF:-1,{name}\n")
        f.write(f"#EXTVLCOPT:http-user-agent={headers['User-Agent']}\n")
        f.write(f"#EXTVLCOPT:http-referrer={headers['Referer']}\n")
        f.write(f"{link}\n")
