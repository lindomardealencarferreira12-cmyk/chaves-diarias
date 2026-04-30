import os
import re

directory = r"C:\Users\Lindomar de Alencar\.gemini\antigravity\scratch\chaves-diarias"

def process_file(filename):
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Typography resizes
    content = content.replace("font-size: clamp(4rem, 12vw, 10rem);", "font-size: clamp(3rem, 8vw, 6rem);")
    content = content.replace("font-size: clamp(3rem, 7vw, 6rem);", "font-size: clamp(2.5rem, 5vw, 4rem);")
    content = content.replace("font-size: clamp(6rem, 15vw, 15rem);", "font-size: clamp(4rem, 10vw, 8rem);")
    content = content.replace("font-size: 2.5rem;\n            margin-bottom: 1rem;", "font-size: 1.8rem;\n            margin-bottom: 1rem;")

    # 2. Remove Construction Badge CSS and HTML
    badge_css = r"/\*\s*CONSTRUCTION RIBBON\s*\*/[\s\S]*?pointer-events: none;\s*\}"
    content = re.sub(badge_css, "", content)
    
    content = re.sub(r'<div class="construction-badge">.*?</div>', "", content)

    # 3. Add CSS for Hero Key Wrapper and WhatsApp
    new_css = """
        /* HERO KEY */
        .hero-key-wrapper {
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            text-decoration: none;
            margin-bottom: 2rem;
            position: relative;
            z-index: 10;
        }
        .hero-img {
            width: 350px;
            max-width: 80vw;
            filter: drop-shadow(0 20px 40px rgba(0,0,0,0.8));
            animation: float-key 6s ease-in-out infinite;
            border-radius: 20px;
            mix-blend-mode: screen;
            transform: rotate(90deg);
            transition: filter 0.5s var(--ease), transform 0.5s var(--ease);
        }
        @keyframes float-key {
            0%, 100% { transform: translateY(0) rotate(90deg); }
            50% { transform: translateY(-15px) rotate(90deg); }
        }
        .hero-key-wrapper:hover .hero-img {
            filter: drop-shadow(0 20px 40px rgba(229, 192, 123, 0.6));
            transform: rotate(90deg) scale(1.05);
        }
        .key-tooltip {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border);
            color: #fff;
            padding: 10px 25px;
            border-radius: 100px;
            font-size: 1rem;
            margin-top: 20px;
            transition: all 0.3s var(--ease);
            font-family: var(--font-sans);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            font-weight: 600;
        }
        .hero-key-wrapper:hover .key-tooltip {
            background: var(--accent);
            color: #000;
            transform: translateY(-5px);
        }

        /* WHATSAPP FLOAT BUTTON */
        .whatsapp-wrapper {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 10px;
        }
        .whatsapp-text {
            background-color: #FFF;
            color: #000;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 800;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            position: relative;
            animation: bounce-msg 2s infinite;
            font-family: var(--font-sans);
        }
        .whatsapp-text::after {
            content: '';
            position: absolute;
            bottom: -6px;
            right: 20px;
            border-width: 6px 6px 0;
            border-style: solid;
            border-color: #FFF transparent transparent transparent;
        }
        @keyframes bounce-msg {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
        .whatsapp-float {
            width: 60px;
            height: 60px;
            background-color: #25d366;
            color: #FFF;
            border-radius: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4);
            transition: all 0.3s ease;
            text-decoration: none;
            animation: pulse-wa 2s infinite;
        }
        .whatsapp-float:hover {
            background-color: #128C7E;
            transform: scale(1.1);
        }
        @keyframes pulse-wa {
            0% { box-shadow: 0 0 0 0 rgba(37, 211, 102, 0.7); }
            70% { box-shadow: 0 0 0 15px rgba(37, 211, 102, 0); }
            100% { box-shadow: 0 0 0 0 rgba(37, 211, 102, 0); }
        }

        /* Responsive fixes for WhatsApp */
        @media (max-width: 768px) {
            .whatsapp-wrapper {
                bottom: 30px;
                right: 20px;
            }
            .whatsapp-float {
                width: 55px;
                height: 55px;
            }
        }
        
        /* FLAGS */
        .lang-link {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .lang-link img {
            border-radius: 2px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.5);
            margin-top: 1px;
        }
"""
    # Insert new CSS just before </style>
    if "/* HERO KEY */" not in content:
        content = content.replace("</style>", new_css + "\n</style>")

    # 4. Replace Hero Image with Hero Wrapper
    # First, find and remove the old image if it exists in the old format
    old_img_regex = r'<img src="modern_abstract_key_1777507388626\.png".*?class="hero-img.*?>'
    
    tooltip_text = "Clique na chave e receba sua chave para hoje"
    if "index-en.html" in filename:
        tooltip_text = "Click the key and receive your key for today"
    elif "index-es.html" in filename:
        tooltip_text = "Haga clic en la llave y reciba su llave de hoy"
        
    hero_replacement = f'''<a href="SEU_LINK_SUBSTACK_AQUI" class="hero-key-wrapper reveal delay-1">
                <img src="modern_abstract_key_1777507388626.png" alt="Chave" class="hero-img" onerror="this.src='key.png'">
                <div class="key-tooltip">{tooltip_text}</div>
            </a>'''
            
    content = re.sub(old_img_regex, hero_replacement, content)

    # 5. Add flags to lang links
    pt_link = '<a href="index.html" class="lang-link active">PT</a>'
    pt_link_un = '<a href="index.html" class="lang-link">PT</a>'
    
    en_link = '<a href="index-en.html" class="lang-link active">EN</a>'
    en_link_un = '<a href="index-en.html" class="lang-link">EN</a>'
    
    es_link = '<a href="index-es.html" class="lang-link active">ES</a>'
    es_link_un = '<a href="index-es.html" class="lang-link">ES</a>'
    
    pt_flag = '<a href="index.html" class="lang-link active"><img src="https://flagcdn.com/w20/br.png" alt="PT" width="16"> PT</a>'
    pt_flag_un = '<a href="index.html" class="lang-link"><img src="https://flagcdn.com/w20/br.png" alt="PT" width="16"> PT</a>'

    en_flag = '<a href="index-en.html" class="lang-link active"><img src="https://flagcdn.com/w20/us.png" alt="EN" width="16"> EN</a>'
    en_flag_un = '<a href="index-en.html" class="lang-link"><img src="https://flagcdn.com/w20/us.png" alt="EN" width="16"> EN</a>'

    es_flag = '<a href="index-es.html" class="lang-link active"><img src="https://flagcdn.com/w20/es.png" alt="ES" width="16"> ES</a>'
    es_flag_un = '<a href="index-es.html" class="lang-link"><img src="https://flagcdn.com/w20/es.png" alt="ES" width="16"> ES</a>'

    content = content.replace(pt_link, pt_flag).replace(pt_link_un, pt_flag_un)
    content = content.replace(en_link, en_flag).replace(en_link_un, en_flag_un)
    content = content.replace(es_link, es_flag).replace(es_link_un, es_flag_un)

    # 6. Add WhatsApp button before footer
    whatsapp_html = """
    <!-- WHATSAPP FLOAT BUTTON -->
    <div class="whatsapp-wrapper">
        <div class="whatsapp-text">Fale agora conosco</div>
        <a href="https://wa.me/5567999128212" class="whatsapp-float" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" style="width: 35px; height: 35px; fill: #FFF;"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7 .9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
        </a>
    </div>

    <footer>
"""
    if "whatsapp-wrapper" not in content:
        content = content.replace("<footer>", whatsapp_html)

    # 7. Make sure old float animation css is removed if we redeclare it? The re.sub doesn't remove the original float keyframes but they won't clash. Let's just remove the original `.hero-img` block
    old_hero_img_css = r"\.hero-img\s*\{[\s\S]*?mix-blend-mode: screen;\s*\}"
    content = re.sub(old_hero_img_css, "", content)
    
    # Also remove original float keyframes
    old_float_kf = r"@keyframes float\s*\{[\s\S]*?\}"
    content = re.sub(old_float_kf, "", content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print(f"Updated {filename}")

process_file("index.html")
process_file("index-en.html")
process_file("index-es.html")
