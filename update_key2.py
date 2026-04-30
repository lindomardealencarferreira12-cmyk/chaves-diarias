import os
import re

directory = r"C:\Users\Lindomar de Alencar\.gemini\antigravity\scratch\chaves-diarias"

def process_file(filename):
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Image filename
    content = content.replace("modern_abstract_key_1777507388626.png", "horizontal_smoke_key_1777510824466.png")

    # 2. Tooltip texts
    content = content.replace("Clique na chave e receba sua chave para hoje", "Clique na chave e pegue sua chave diária.")
    content = content.replace("Click the key and receive your key for today", "Click the key and get your daily key.")
    content = content.replace("Haga clic en la llave y reciba su llave de hoy", "Haga clic en la llave y tome su llave diaria.")

    # 3. Fix CSS rotations
    content = content.replace("transform: rotate(90deg);", "")
    content = content.replace("transform: rotate(90deg) scale(1.05);", "transform: scale(1.05);")
    content = content.replace("transform: translateY(0) rotate(90deg);", "transform: translateY(0);")
    content = content.replace("transform: translateY(-15px) rotate(90deg);", "transform: translateY(-15px);")

    # 4. Make image larger since it's horizontal now
    content = content.replace("width: 350px;\n            max-width: 80vw;", "width: 500px;\n            max-width: 90vw;")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print(f"Updated {filename}")

process_file("index.html")
process_file("index-en.html")
process_file("index-es.html")
