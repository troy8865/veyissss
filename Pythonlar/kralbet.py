import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

PROXY_PREFIX = "https://vettelchannelowner-kralbet.hf.space/proxy/m3u?url="
BASE_URL = "https://1029kralbettv.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": BASE_URL
}

response = requests.get(PROXY_PREFIX + "https://royalvipcanlimac.com/channels.php", headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

channels = []

# Örnek: her kanal linki <a href="..."> ve yanında <div class="home">kanal adı</div> ve <img src="..."> varsa
for a in soup.find_all("a", href=True):
    href = a['href']

    # Sadece /channel?id= ya da istediğin pattern varsa filtrele (isteğe göre)
    if not href:
        continue

    # Kanal adı bulmaya çalış
    parent = a.parent
    kanal_adi = None
    kanal_logo = None

    div_home = parent.find("div", class_="home") if parent else None
    if div_home:
        kanal_adi = div_home.text.strip()

    img = parent.find("img") if parent else None
    if img and img.get("src"):
        logo_src = img["src"]
        kanal_logo = urljoin(BASE_URL, logo_src)

    # Linki tam URL haline getir (eğer göreli ise)
    kanal_link = href
    if not href.startswith("http"):
        kanal_link = urljoin(BASE_URL, href)

    # Burada başına PROXY_PREFIX ekle
    kanal_link = PROXY_PREFIX + kanal_link

    if kanal_adi:
        channels.append({
            "name": kanal_adi,
            "link": kanal_link,
            "logo": kanal_logo
        })

print(f"{len(channels)} kanal bulundu.")



print("Kralbet.m3u dosyasına yazılıyor...")

with open("kralbet.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n\n")
    for idx, link in enumerate(sorted(channel_links), 1):
        f.write(f"#EXTINF:-1 tvg-name=\"Kralbet Kanal {idx}\" group-title=\"KRALBET\",Kralbet Kanal {idx}\n")
        f.write(f"#EXTVLCOPT:http-user-agent={headers['User-Agent']}\n")
        f.write(f"#EXTVLCOPT:http-referrer={headers['Referer']}\n")
        f.write(link + "\n\n")

print(f"{len(channel_links)} kanal kralbet.m3u dosyasına yazıldı.")

