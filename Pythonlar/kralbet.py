import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://1029kralbettv.com"
}

url = "https://1029kralbettv.com"

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Sayfadaki tüm m3u8 linklerini topla
m3u8_links = re.findall(r'(https?://[^\s"]+\.m3u8)', response.text)

with open("kralbet.m3u", "w", encoding="utf-8") as f:
    for idx, link in enumerate(m3u8_links, 1):
        f.write(f"#EXTINF:-1 tvg-name=\"Kralbet Kanal {idx}\" group-title=\"KRALBET\",Kralbet Kanal {idx}\n")
        f.write(f"#EXTVLCOPT:http-user-agent={headers['User-Agent']}\n")
        f.write(f"#EXTVLCOPT:http-referrer={headers['Referer']}\n")
        f.write(link + "\n")

print(f"{len(m3u8_links)} adet m3u8 linki kralbet.m3u dosyasına yazıldı.")
