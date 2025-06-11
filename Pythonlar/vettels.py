import re

def load_m3u(file_path):
    """M3U dosyasını oku ve içeriğini liste olarak döndür."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def parse_m3u(lines):
    """M3U içeriğini sözlük olarak ayrıştır."""
    channels = {}
    current_name = None

    for line in lines:
        if line.startswith('#EXTINF'):
            match = re.search(r',(.+)', line)
            if match:
                current_name = match.group(1).strip()
        elif line.startswith('http'):
            if current_name:
                channels[current_name] = line.strip()

    return channels

def update_channels(vettecl_file, vavoo_file, output_file):
    """Vettel kanal listesini Vavoo'ya göre güncelle."""
    vettecl_data = parse_m3u(load_m3u(vettel_file))
    vavoo_data = parse_m3u(load_m3u(vavoo_file))

    updated_lines = []
    for line in load_m3u(vettecl_file):
        if line.startswith('#EXTINF'):
            updated_lines.append(line)
            match = re.search(r',(.+)', line)
            if match:
                current_name = match.group(1).strip()
        elif line.startswith('http'):
            if current_name and current_name in vavoo_data:
                updated_lines.append(vavoo_data[current_name] + '\n')
            else:
                updated_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

if __name__ == "__main__":
    update_channels("vettelchannel.m3u", "vavoo.m3u", "updated_vetteclchannel.m3u")
    print("Güncelleme tamamlandı! ✅")
