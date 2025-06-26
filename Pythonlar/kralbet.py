import requests
import re

BASE_URL = "https://royalvipcanlimac.com/channels.php"
LINK_PREFIX = "https://1029kralbettv.com"
M3U_FILE = "kralbet.m3u"

# Sayfa içeriğini al
r = requests.get(BASE_URL)
html = r.text

# href ve başlıkları yakala
href_matches = re.findall(r'href="(channel\?id=[^"]+)"', html)
title_matches = re.findall(r'<div class="home">(.*?)</div>', html)
img_matches = re.findall(r'<img src="([^"]+)"', html)

with open(M3U_FILE, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n\n")

    for idx, href in enumerate(href_matches):
        kanal_id = href.split("id=")[-1]
        tvg_name = title_matches[idx].strip() if idx < len(title_matches) else f"Kanal_{idx+1}"
        logo = f"{LINK_PREFIX}/{img_matches[idx].lstrip('/')}" if idx < len(img_matches) else ""
        stream_url = f"{LINK_PREFIX}/{href}"

        f.write(
            f'#EXTINF:-1 tvg-name="{tvg_name}" tvg-language="Türkçe" tvg-country="Türkiye" '
            f'tvg-id="{kanal_id}" tvg-logo="{logo}" group-title="Genel Kanallar",{tvg_name}\n'
        )
        f.write(f"{stream_url}\n\n")
