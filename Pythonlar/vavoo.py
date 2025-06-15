import requests
import re

URL = "https://vavoo.to/channels"
PROXY_BASE = "https://vettelchannelowner-vettel-channel.hf.space/proxy/m3u?url=https://vavoo.to/play/{}/index.m3u8"
LOGO_URL = "https://raw.githubusercontent.com/vettelistrue/Vettel-Channel-M3U/refs/heads/main/Pythonlar/VETTEL.png"
OUTPUT_FILE = "vavoo.m3u"

TURKISH_CHAR_MAP = str.maketrans({
    'ç': 'c', 'Ç': 'C',
    'ğ': 'g', 'Ğ': 'G',
    'ı': 'i', 'İ': 'I',
    'ö': 'o', 'Ö': 'O',
    'ş': 's', 'Ş': 'S',
    'ü': 'u', 'Ü': 'U'
})

def normalize_tvg_id(name):
    name_ascii = name.translate(TURKISH_CHAR_MAP)
    return re.sub(r'\W+', '_', name_ascii.strip()).upper()

def fix_channel_name(name):
    return name.strip()

def fetch_turkey_channels():
    response = requests.get(URL)
    if response.status_code != 200:
        print("Hata: Kanal listesi alınamadı.")
        return []

    channels = response.json()
    turkey_channels = [ch for ch in channels if ch.get("country") == "Turkey"]

    for ch in turkey_channels:
        ch["name"] = fix_channel_name(ch.get("name", ""))
    
    return turkey_channels  # API'den gelen sıralamayı koruyoruz

def generate_m3u(channels):
    grouped_channels = {}

    # API'deki grup bilgisine göre kanalları kategorize et
    for ch in channels:
        name = ch.get("name", "Unknown").strip()
        group_title = ch.get("category", "Diğer")  # API'den gelen kategori bilgisi alınıyor

        if group_title not in grouped_channels:
            grouped_channels[group_title] = []

        grouped_channels[group_title].append(ch)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for group, channels in grouped_channels.items():
            kanal_count = len(channels)
            for ch in channels:
                name = ch.get("name", "Unknown").strip()
                tvg_id = normalize_tvg_id(name)
                proxy_url = PROXY_BASE.format(ch.get("id"))

                f.write(
                    f'#EXTINF:-1 tvg-name="{name}" tvg-language="Türkçe" '
                    f'tvg-country="Türkiye" tvg-id="{tvg_id}" tvg-logo="{LOGO_URL}" '
                    f'group-title="{group} ({kanal_count})",{name}\n{proxy_url}\n'
                )

    print(f"{len(channels)} kanal bulundu → '{OUTPUT_FILE}' dosyasına yazıldı.")

if __name__ == "__main__":
    turkey_channels = fetch_turkey_channels()
    generate_m3u(turkey_channels)
