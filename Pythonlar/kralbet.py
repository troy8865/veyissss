import requests
from bs4 import BeautifulSoup
import re
import os

def m3u_olustur():
    try:
        print("M3U dosyası oluşturuluyor...")
        
        # Kaynak URL'ler
        kaynak_url = "https://royalvipcanlimac.com/channels.php"
        proxy_url = f"https://vettelchannelowner-kralbet.hf.space/proxy/m3u?url={kaynak_url}"
        
        # Sayfayı çek
        print("Kanal listesi alınıyor...")
        response = requests.get(proxy_url, timeout=15)
        response.raise_for_status()
        
        # HTML'i parse et
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # M3U başlığı
        m3u_icerik = "#EXTM3U\n"
        
        # Kanal sayacı
        kanal_sayisi = 0
        
        # Tüm kanalları işle
        for kanal in soup.find_all('div', class_='channel'):
            # Kanal adını al
            isim_div = kanal.find('div', class_='home')
            if not isim_div:
                continue
                
            kanal_adi = isim_div.get_text(strip=True)
            
            # Linki al
            link = kanal.find('a', href=True)
            if not link:
                continue
                
            link = link['href'].strip()
            if not link.startswith('/'):
                link = '/' + link
                
            # Tam URL'yi oluştur
            tam_url = f"https://1029kralbettv.com{link}"
            
            # M3U formatına ekle
            m3u_icerik += f'#EXTINF:-1 tvg-name="{kanal_adi}",{kanal_adi}\n'
            m3u_icerik += f"{tam_url}\n"
            kanal_sayisi += 1
        
        # Dosyaya yaz
        with open('kralbet.m3u', 'w', encoding='utf-8') as dosya:
            dosya.write(m3u_icerik)
            
        print(f"Başarılı! {kanal_sayisi} kanal eklendi.")
        return True
        
    except Exception as hata:
        print(f"Hata: {str(hata)}")
        return False

if __name__ == "__main__":
    m3u_olustur()
