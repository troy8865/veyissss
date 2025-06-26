import requests
import re
from bs4 import BeautifulSoup

BASE_URL = "https://royalvipcanlimac.com/channels.php"
PROXY_PREFIX = "https://vettelchannelowner-kralbet.hf.space/proxy/m3u?url="
LINK_PREFIX = "https://1029kralbettv.com"
M3U_FILE = "kralbet.m3u"

# HTML'yi al
response = requests.get(PROXY_PREFIX + BASE_URL)
html = response.text

# BeautifulSoup ile parse et
soup = BeautifulSoup(html, "html.parser")
channels = soup.find_all("a", href=re.compile(r"channel\?id="))
titles = soup.find_all("div", class_="home")

with open(M3U_FILE, "w", encoding="utf-8") as file:
    file.write("#EXTM3U\n")

    for idx, channel in enumerate(channels):
        href = channel["href"]
        channel_id = href.split("id=")[-1]
        stream_url = f"{PROXY_PREFIX}{LINK_PREFIX}/{href}"

        # tvg-name'i <div class="home"> içinden al
        tvg_name = titles[idx].text.strip() if idx < len(titles) else f"Channel {idx+1}"
        file.write(f'#EXTINF:-1 tvg-name="{tvg_name}",{tvg_name}\n{stream_url}\n')

    # img src'leri al ve yaz (isteğe bağlı)
    images = soup.find_all("img", src=True)
    for img in images:
        img_url = f"{LINK_PREFIX}/{img['src'].lstrip('/')}"
        file.write(f"#EXTINF:-1,Logo\n{img_url}\n")
