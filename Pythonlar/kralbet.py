import requests
from bs4 import BeautifulSoup

def m3u_olustur():
    try:
        # Kaynak URL'yi al
        kaynak_url = "https://royalvipcanlimac.com/channels.php"
        proxy_url = f"https://vettelchannelowner-kralbet.hf.space/proxy/m3u?url={kaynak_url}"
        
        # Sayfayı çek
        print("Sayfa çekiliyor...")
        response = requests.get(proxy_url, timeout=10)
        response.raise_for_status()
        
        # HTML'i parse et
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # M3U başlığını hazırla
        m3u_icerik = "#EXTM3U\n"
        
        print("Kanal bilgileri işleniyor...")
        # Tüm kanalları bul
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
            link = link['href']
            
            # Tam URL'yi oluştur
            tam_url = f"https://1029kralbettv.com{link}"
            
            # M3U'ya ekle
            m3u_icerik += f'#EXTINF:-1 tvg-name="{kanal_adi}",{kanal_adi}\n'
            m3u_icerik += f"{tam_url}\n"
            
        # Dosyaya yaz
        with open('kralbet.m3u', 'w', encoding='utf-8') as dosya:
            dosya.write(m3u_icerik)
            
        print("M3U dosyası başarıyla oluşturuldu!")
        return True
        
    except Exception as hata:
        print(f"Hata oluştu: {str(hata)}")
        return False

if __name__ == "__main__":
    m3u_olustur()
