# MCP araçları dosyası
# Bu dosya MCP araçlarının tanımlarını içerecek

import os


def prepare_full_context():
    # .gitignore dosyasını okuyarak desen listesini oluştur
    ignore_patterns = []
    with open('.gitignore', 'r') as file:
        for line in file.readlines():
            line = line.strip()
            if line and not line.startswith('#'):
                ignore_patterns.append(line)

    # Proje dizinini dolaş ve dosyaları filtrele
    full_context = ''
    for root, _, files in os.walk('.'):       
        for file in sorted(files):
            file_path = os.path.join(root, file)
            if not any(os.path.fnmatch.fnmatch(file_path, pattern) for pattern in ignore_patterns):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                full_context += f"--- Dosya: {file_path} ---\n{content}\n"

    return full_context

__all__ = ['prepare_full_context']
