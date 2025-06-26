import requests
import re

BASE_URL = "https://royalvipcanlimac.com/channels.php"
PROXY_PREFIX = "https://vettelchannelowner-kralbet.hf.space/proxy/m3u?url="
LINK_PREFIX = "https://1029kralbettv.com"
M3U_FILE = "kralbet.m3u"

response = requests.get(PROXY_PREFIX + BASE_URL)
html = response.text

matches = re.findall(r'href="(channel\?id=[^"]+)"', html)
image_matches = re.findall(r'<img src="([^"]+)"', html)

with open(M3U_FILE, "w", encoding="utf-8") as file:
    file.write("#EXTM3U\n")
    for match in matches:
        full_url = f"{PROXY_PREFIX}{LINK_PREFIX}/{match}"
        file.write(f"#EXTINF:-1,{match}\n{full_url}\n")

    for img in image_matches:
        full_img_url = f"{LINK_PREFIX}/{img}"
        file.write(f"#EXTINF:-1,Logo\n{full_img_url}\n")
