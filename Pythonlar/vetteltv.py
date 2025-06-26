import difflib

def kanal_listesini_ayikla(dosya_yolu):
    with open(dosya_yolu, 'r', encoding='utf-8') as f:
        satirlar = f.readlines()

    kanallar = []
    for i in range(len(satirlar)):
        if satirlar[i].startswith('#EXTINF'):
            isim = satirlar[i].split(',')[-1].strip()
            link = satirlar[i + 1].strip()
            kanallar.append({'isim': isim, 'link': link, 'index': i})
    return kanallar, satirlar

def en_benzer_kanal(hedef_kanal, kanal_listesi):
    eslesmeler = [
        (kanal, difflib.SequenceMatcher(None, hedef_kanal.lower(), kanal['isim'].lower()).ratio())
        for kanal in kanal_listesi
    ]
    eslesmeler = sorted(eslesmeler, key=lambda x: x[1], reverse=True)
    return eslesmeler[0] if eslesmeler and eslesmeler[0][1] >= 0.9 else (None, 0)

def m3u_guncelle():
    vettel_kanallar, vettel_satirlar = kanal_listesini_ayikla('vetteltv.m3u')
    kablo_kanallar, _ = kanal_listesini_ayikla('kablo.m3u')

    for kanal in vettel_kanallar:
        eslesen_kanal, oran = en_benzer_kanal(kanal['isim'], kablo_kanallar)
        if eslesen_kanal:
            print(f"Güncelleniyor: {kanal['isim']} → {eslesen_kanal['isim']} ({int(oran*100)}%)")
            index = kanal['index']
            vettel_satirlar[index + 1] = eslesen_kanal['link'] + '\n'

    with open('vetteltv.m3u', 'w', encoding='utf-8') as f:
        f.writelines(vettel_satirlar)

if __name__ == '__main__':
    m3u_guncelle()
