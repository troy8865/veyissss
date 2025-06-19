import requests
import json
import gzip
from io import BytesIO

def mevcut_kanallari_oku(dosya_adi="kablo.m3u"):
    """Mevcut M3U dosyasındaki kanalları okur ve bir sete kaydeder"""
    try:
        with open(dosya_adi, "r", encoding="utf-8") as f:
            m3u_icerik = f.readlines()
        
        eski_kanallar = set()
        for satir in m3u_icerik:
            if satir.startswith("http"):  # Sadece URL satırlarını al
                eski_kanallar.add(satir.strip())
        
        return eski_kanallar
    except FileNotFoundError:
        return set()

def get_canli_tv_m3u():
    """M3U dosyasını güncellerken mevcut kanalları korur"""

    url = "https://core-api.kablowebtv.com/api/channels"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://tvheryerde.com",
        "Origin": "https://tvheryerde.com",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer TOKEN"  # Güvenlik için gerçek token eklenmemeli
    }

    try:
        print("📡 API'den veri alınıyor...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        try:
            with gzip.GzipFile(fileobj=BytesIO(response.content)) as gz:
                content = gz.read().decode('utf-8')
        except:
            content = response.content.decode('utf-8')

        data = json.loads(content)

        if not data.get("IsSucceeded") or not data.get("Data", {}).get("AllChannels"):
            print("❌ Geçerli veri alınamadı!")
            return False
        
        kanallar = data["Data"]["AllChannels"]
        print(f"✅ {len(kanallar)} yeni kanal bulundu")

        # Mevcut kanalları oku ve listeye ekle
        eski_kanallar = mevcut_kanallari_oku()

        with open("kablo.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            kanal_sayisi = 0
            kanal_index = 1  

            for kanal in kanallar:
                name = kanal.get("Name")
                stream_data = kanal.get("StreamData", {})
                hls_url = stream_data.get("HlsStreamUrl") if stream_data else None
                logo = kanal.get("PrimaryLogoImageUrl", "")
                categories = kanal.get("Categories", [])

                if not name or not hls_url:
                    continue

                group = categories[0].get("Name", "Genel") if categories else "Genel"

                if group == "Bilgilendirme":
                    continue

                tvg_id = str(kanal_index)

                # Eğer kanal zaten mevcut listede varsa ekleme
                if hls_url in eski_kanallar:
                    continue

                f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-logo="{logo}" group-title="{group}",{name}\n')
                f.write(f'{hls_url}\n')

                kanal_sayisi += 1
                kanal_index += 1  

            # Önceden eklenen kanalları tekrar ekleyelim
            for eski_kanal in eski_kanallar:
                f.write(f"{eski_kanal}\n")

        print(f"📺 Güncellenmiş kablo.m3u dosyası oluşturuldu! ({kanal_sayisi + len(eski_kanallar)} kanal)")
        return True

    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

if __name__ == "__main__":
    get_canli_tv_m3u()
