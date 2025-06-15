import requests
import time

URL = "https://vavoo.to/channels"
PROXY_BASE = "https://vettelchannelowner-vettel-channel.hf.space/proxy/m3u?url=https://vavoo.to/play/{}/index.m3u8"
LOGO_URL = "https://raw.githubusercontent.com/vettelistrue/Vettel-Channel-M3U/refs/heads/main/Pythonlar/VETTEL.png"
OUTPUT_FILE = "vavoo.m3u"
UPDATE_INTERVAL = 10 * 60 * 60  # 10 saat (saniye cinsinden)

def fetch_turkey_channels():
    response = requests.get(URL)
    if response.status_code != 200:
        print("Hata: Kanal listesi alınamadı.")
        return []

    channels = response.json()
    turkey_channels = [ch for ch in channels if ch.get("country") == "Turkey"]
    return turkey_channels

def generate_m3u(channels):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            name = ch.get("name", "Unknown").strip()
            proxy_url = PROXY_BASE.format(ch.get("id"))

            f.write(
                f'#EXTINF:-1 tvg-name="{name}" tvg-language="Türkçe" '
                f'tvg-country="Türkiye" tvg-logo="{LOGO_URL}" '
                f'group-title="Tüm Kanallar",{name}\n{proxy_url}\n'
            )

    print(f"{len(channels)} kanal bulundu → '{OUTPUT_FILE}' dosyasına yazıldı.")

def auto_update():
    while True:
        print("🔄 Güncelleme başlatılıyor...")
        turkey_channels = fetch_turkey_channels()
        generate_m3u(turkey_channels)
        print(f"✅ Güncelleme tamamlandı! Bir sonraki güncelleme 10 saat sonra.")
        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    auto_update()
