import os

html_template = """<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:ital,wght@0,300..800;1,300..800&display=swap" rel="stylesheet">
    
    <script src="https://unpkg.com/@studio-freight/lenis@1.0.34/dist/lenis.min.js"></script>

    <style>
        :root {{
            --bg: #050505;
            --text: #F2F2F2;
            --text-muted: #888888;
            --accent: #E5C07B;
            --surface: rgba(25, 25, 25, 0.6);
            --border: rgba(255, 255, 255, 0.08);
            
            --font-display: 'Instrument Serif', serif;
            --font-sans: 'Plus Jakarta Sans', sans-serif;
            
            --ease: cubic-bezier(0.25, 1, 0.5, 1);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background-color: var(--bg); color: var(--text); font-family: var(--font-sans); overflow-x: hidden; -webkit-font-smoothing: antialiased; }}
        
        body::before {{
            content: ''; position: fixed; inset: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 9999; opacity: 0.04;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
        }}

        ::selection {{ background: var(--text); color: var(--bg); }}

        html.lenis {{ height: auto; }}
        .lenis.lenis-smooth {{ scroll-behavior: auto; }}
        .lenis.lenis-smooth [data-lenis-prevent] {{ overscroll-behavior: contain; }}
        .lenis.lenis-stopped {{ overflow: hidden; }}
        .lenis.lenis-scrolling iframe {{ pointer-events: none; }}

        h1, h2, h3 {{ font-family: var(--font-display); font-weight: 400; line-height: 1.1; }}
        p {{ line-height: 1.6; font-size: 1.125rem; color: var(--text-muted); }}
        
        .container {{ max-width: 1400px; margin: 0 auto; padding: 0 5vw; }}

        nav {{ position: fixed; top: 0; left: 0; right: 0; padding: 2rem 0; z-index: 100; mix-blend-mode: difference; transition: padding 0.3s var(--ease); }}
        nav.scrolled {{ padding: 1rem 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(10px); mix-blend-mode: normal; }}
        .nav-content {{ display: flex; justify-content: space-between; align-items: center; }}
        .nav-left, .nav-right {{ flex: 1; display: flex; }}
        .nav-right {{ justify-content: flex-end; gap: 1rem; align-items: center; }}
        
        .logo {{ flex: 0 0 auto; font-family: var(--font-display); font-size: 2.2rem; color: #fff; text-decoration: none; text-align: center; line-height: 1; white-space: nowrap; }}
        .logo span {{ font-family: var(--font-sans); font-size: 0.65rem; letter-spacing: 0.3em; text-transform: uppercase; display: block; margin-top: 0.5rem; color: var(--text-muted); }}

        .lang-link {{ display: flex; align-items: center; gap: 6px; color: #fff; text-decoration: none; font-size: 0.85rem; font-weight: 600; opacity: 0.5; transition: opacity 0.3s var(--ease); }}
        .lang-link img {{ border-radius: 2px; box-shadow: 0 1px 3px rgba(0,0,0,0.5); margin-top: 1px; }}
        .lang-link:hover, .lang-link.active {{ opacity: 1; }}

        .btn-nav {{ background: #fff; color: #000; padding: 0.8rem 1.5rem; border-radius: 100px; text-decoration: none; font-size: 0.85rem; font-weight: 700; transition: transform 0.3s var(--ease), box-shadow 0.3s var(--ease); }}
        .btn-nav:hover {{ transform: scale(1.05); box-shadow: 0 0 20px rgba(255,255,255,0.3); }}

        .hero {{ min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding-top: 15vh; position: relative; }}

        .hero-key-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: center; text-decoration: none; margin-bottom: 3rem; position: relative; z-index: 10; width: 100%; }}
        .hero-img {{ width: 500px; max-width: 90vw; filter: drop-shadow(0 20px 40px rgba(0,0,0,0.8)); animation: float-key 6s ease-in-out infinite; border-radius: 20px; mix-blend-mode: screen; transition: filter 0.5s var(--ease), transform 0.5s var(--ease); margin: 0 auto; }}
        @keyframes float-key {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-15px); }} }}
        .hero-key-wrapper:hover .hero-img {{ filter: drop-shadow(0 20px 40px rgba(229, 192, 123, 0.6)); transform: scale(1.05); }}
        
        .key-tooltip {{
            background: var(--accent);
            color: #000;
            padding: 12px 30px;
            border-radius: 100px;
            font-size: 1.1rem;
            margin-top: 20px;
            transition: all 0.3s var(--ease);
            font-family: var(--font-sans);
            box-shadow: 0 10px 30px rgba(229, 192, 123, 0.4);
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .hero-key-wrapper:hover .key-tooltip {{ background: #fff; transform: translateY(-5px); box-shadow: 0 15px 40px rgba(255, 255, 255, 0.3); }}

        .hero h1 {{ font-size: clamp(3rem, 8vw, 6rem); letter-spacing: -0.05em; line-height: 0.95; z-index: 2; position: relative; }}
        .hero h1 span {{ display: block; font-style: italic; color: var(--accent); opacity: 0.9; }}
        .hero p {{ max-width: 600px; margin: 2rem auto; font-size: 1.25rem; z-index: 2; position: relative; }}

        .badge {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(20px); border: 1px solid var(--border); padding: 0.5rem 1rem; border-radius: 100px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 3rem; display: inline-flex; align-items: center; gap: 10px; z-index: 2; position: relative; }}
        .badge-dot {{ width: 8px; height: 8px; background: #25d366; border-radius: 50%; box-shadow: 0 0 10px #25d366; animation: pulse-dot 2s infinite; }}
        @keyframes pulse-dot {{ 0% {{ box-shadow: 0 0 0 0 rgba(37, 211, 102, 0.7); }} 70% {{ box-shadow: 0 0 0 10px rgba(37, 211, 102, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(37, 211, 102, 0); }} }}

        .section {{ padding: 10rem 0; position: relative; }}
        .section-header {{ margin-bottom: 5rem; }}
        .section-header h2 {{ font-size: clamp(2.5rem, 5vw, 4rem); letter-spacing: -0.02em; }}

        .bento-grid {{ display: grid; grid-template-columns: repeat(12, 1fr); gap: 1.5rem; grid-auto-rows: minmax(350px, auto); }}
        .bento-item {{ background: var(--surface); border: 1px solid var(--border); border-radius: 32px; padding: 3.5rem; position: relative; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.6s var(--ease), background 0.6s var(--ease), border-color 0.6s var(--ease); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); }}
        .bento-item:hover {{ transform: translateY(-10px); background: rgba(40, 40, 40, 0.8); border-color: rgba(255,255,255,0.2); }}
        .bento-item.large {{ grid-column: span 8; }}
        .bento-item.small {{ grid-column: span 4; }}
        .bento-item.medium {{ grid-column: span 6; }}
        .bento-item h3 {{ font-size: 1.8rem; margin-bottom: 1rem; }}
        .bento-icon {{ font-size: 4rem; color: var(--accent); margin-bottom: 2rem; font-family: var(--font-display); font-style: italic; opacity: 0.8; }}

        .samples-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 3rem; }}
        .sample-card {{ padding-top: 2rem; border-top: 1px solid var(--border); transition: border-color 0.4s var(--ease); }}
        .sample-card:hover {{ border-top-color: var(--accent); }}
        .sample-card h4 {{ font-family: var(--font-display); font-size: 2rem; color: #fff; margin-bottom: 1rem; line-height: 1.2; }}

        .pricing {{ text-align: center; max-width: 800px; margin: 0 auto; }}
        .price-huge {{ font-family: var(--font-display); font-size: clamp(4rem, 10vw, 8rem); line-height: 0.9; margin: 2rem 0; color: var(--accent); text-shadow: 0 0 80px rgba(229, 192, 123, 0.2); }}
        .price-sub {{ font-size: 1.5rem; color: #fff; }}

        .btn-huge {{ display: inline-flex; align-items: center; justify-content: center; background: #fff; color: #000; font-size: 1.25rem; font-weight: 700; padding: 1.5rem 4rem; border-radius: 100px; text-decoration: none; margin-top: 4rem; transition: all 0.5s var(--ease); position: relative; overflow: hidden; box-shadow: 0 10px 30px rgba(255,255,255,0.1); }}
        .btn-huge::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: var(--accent); transform: scaleY(0); transform-origin: bottom; transition: transform 0.5s var(--ease); z-index: 1; border-radius: 100px; }}
        .btn-huge:hover::before {{ transform: scaleY(1); }}
        .btn-huge span {{ position: relative; z-index: 2; }}
        .btn-huge:hover {{ color: #000; box-shadow: 0 20px 50px rgba(229, 192, 123, 0.3); transform: translateY(-5px); }}

        .faq-item {{ border-bottom: 1px solid var(--border); padding: 2.5rem 0; cursor: pointer; transition: border-color 0.3s var(--ease); }}
        .faq-item:hover {{ border-color: rgba(255,255,255,0.2); }}
        .faq-question {{ display: flex; justify-content: space-between; align-items: center; font-size: clamp(1.5rem, 3vw, 2.5rem); font-family: var(--font-display); color: #fff; }}
        .faq-answer {{ max-height: 0; overflow: hidden; transition: max-height 0.5s var(--ease), margin 0.5s var(--ease); color: var(--text-muted); padding-right: 2rem; font-size: 1.2rem; }}
        .faq-item.active .faq-answer {{ max-height: 300px; margin-top: 1.5rem; }}
        .faq-icon {{ font-size: 2.5rem; font-weight: 300; transition: transform 0.5s var(--ease); color: var(--accent); }}
        .faq-item.active .faq-icon {{ transform: rotate(45deg); }}

        footer {{ padding: 5rem 0; text-align: center; border-top: 1px solid var(--border); font-size: 0.9rem; }}

        .reveal {{ opacity: 0; filter: blur(10px); transform: translateY(60px); transition: opacity 1.2s var(--ease), filter 1.2s var(--ease), transform 1.2s var(--ease); }}
        .reveal.active {{ opacity: 1; filter: blur(0); transform: translateY(0); }}
        .delay-1 {{ transition-delay: 0.1s; }}
        .delay-2 {{ transition-delay: 0.2s; }}
        .delay-3 {{ transition-delay: 0.3s; }}

        .whatsapp-wrapper {{ position: fixed; bottom: 30px; right: 30px; z-index: 1000; display: flex; flex-direction: column; align-items: flex-end; gap: 10px; }}
        .whatsapp-text {{ background-color: #FFF; color: #000; padding: 6px 14px; border-radius: 20px; font-size: 0.9rem; font-weight: 800; box-shadow: 0 5px 15px rgba(0,0,0,0.3); position: relative; animation: bounce-msg 2s infinite; font-family: var(--font-sans); }}
        .whatsapp-text::after {{ content: ''; position: absolute; bottom: -6px; right: 20px; border-width: 6px 6px 0; border-style: solid; border-color: #FFF transparent transparent transparent; }}
        @keyframes bounce-msg {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-5px); }} }}
        .whatsapp-float {{ width: 60px; height: 60px; background-color: #25d366; color: #FFF; border-radius: 50px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4); transition: all 0.3s ease; text-decoration: none; animation: pulse-wa 2s infinite; }}
        .whatsapp-float:hover {{ background-color: #128C7E; transform: scale(1.1); }}
        @keyframes pulse-wa {{ 0% {{ box-shadow: 0 0 0 0 rgba(37, 211, 102, 0.7); }} 70% {{ box-shadow: 0 0 0 15px rgba(37, 211, 102, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(37, 211, 102, 0); }} }}

        @media (max-width: 1024px) {{ .bento-item.large, .bento-item.small, .bento-item.medium {{ grid-column: span 12; }} .bento-grid {{ grid-auto-rows: auto; }} .bento-item {{ padding: 2.5rem; }} .section {{ padding: 6rem 0; }} }}
        @media (max-width: 768px) {{ .nav-content {{ flex-direction: column; gap: 1rem; }} .nav-right {{ justify-content: center; width: 100%; }} .btn-nav {{ display: none; }} .hero-img {{ width: 300px; }} .faq-question {{ font-size: 1.5rem; }} nav {{ padding: 1rem 0; }} .whatsapp-wrapper {{ bottom: 30px; right: 20px; }} .whatsapp-float {{ width: 55px; height: 55px; }} }}
    </style>
</head>
<body>
    <nav id="navbar">
        <div class="container nav-content">
            <div class="nav-left"></div>
            <a href="#" class="logo">{brand_name}<br><span>{brand_sub}</span></a>
            <div class="nav-right">
                <a href="index.html" class="lang-link {pt_active}"><img src="https://flagcdn.com/w20/br.png" alt="PT" width="16"> PT</a>
                <a href="index-en.html" class="lang-link {en_active}"><img src="https://flagcdn.com/w20/us.png" alt="EN" width="16"> EN</a>
                <a href="index-es.html" class="lang-link {es_active}"><img src="https://flagcdn.com/w20/es.png" alt="ES" width="16"> ES</a>
                <a href="SEU_LINK_SUBSTACK_AQUI" class="btn-nav">{btn_nav}</a>
            </div>
        </div>
    </nav>

    <section class="hero" id="inicio">
        <div class="container">
            <div class="badge reveal">
                <div class="badge-dot"></div>
                {badge_text}
            </div>
            
            <a href="SEU_LINK_SUBSTACK_AQUI" class="hero-key-wrapper reveal delay-1">
                <img src="horizontal_smoke_key_1777510824466.png" alt="Key" class="hero-img">
                <div class="key-tooltip">{tooltip_text}</div>
            </a>
            
            <h1 class="reveal delay-2">{h1_main} <span>{h1_span}</span></h1>
            <p class="reveal delay-3">{hero_p}</p>
        </div>
    </section>

    <!-- BENTO BOX PROMISE -->
    <section class="section">
        <div class="container">
            <div class="section-header reveal">
                <h2>{bento_title}</h2>
            </div>
            
            <div class="bento-grid">
                <div class="bento-item large reveal">
                    <div class="bento-icon">01</div>
                    <div>
                        <h3>{b1_title}</h3>
                        <p>{b1_p}</p>
                    </div>
                </div>
                <div class="bento-item small reveal delay-1">
                    <div class="bento-icon">02</div>
                    <div>
                        <h3>{b2_title}</h3>
                        <p>{b2_p}</p>
                    </div>
                </div>
                <div class="bento-item medium reveal delay-2">
                    <div class="bento-icon">03</div>
                    <div>
                        <h3>{b3_title}</h3>
                        <p>{b3_p}</p>
                    </div>
                </div>
                <div class="bento-item medium reveal delay-3">
                    <div class="bento-icon">04</div>
                    <div>
                        <h3>{b4_title}</h3>
                        <p>{b4_p}</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- SAMPLES -->
    <section class="section" style="background: #090909; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);">
        <div class="container">
            <div class="section-header reveal">
                <h2>{samples_title}</h2>
                <p style="font-size: 1.5rem; margin-top: 1rem;">{samples_p}</p>
            </div>
            <div class="samples-grid">
                <div class="sample-card reveal">
                    <h4>{s1_title}</h4>
                    <p>{s1_p}</p>
                </div>
                <div class="sample-card reveal delay-1">
                    <h4>{s2_title}</h4>
                    <p>{s2_p}</p>
                </div>
                <div class="sample-card reveal delay-2">
                    <h4>{s3_title}</h4>
                    <p>{s3_p}</p>
                </div>
            </div>
        </div>
    </section>

    <!-- PRICING -->
    <section class="section">
        <div class="container pricing reveal">
            <h2>{pricing_title}</h2>
            <div class="price-huge">{price_huge}</div>
            <div class="price-sub">{price_sub}</div>
            
            <a href="SEU_LINK_SUBSTACK_AQUI" class="btn-huge">
                <span>{btn_pricing}</span>
            </a>
            
            <p style="margin-top: 2rem; font-size: 1rem;">{pricing_p}</p>
        </div>
    </section>

    <!-- FAQ -->
    <section class="section" style="border-top: 1px solid var(--border);">
        <div class="container" style="max-width: 900px;">
            <h2 style="margin-bottom: 4rem;" class="reveal">{faq_title}</h2>
            
            <div class="faq-list reveal delay-1">
                <div class="faq-item" onclick="this.classList.toggle('active')">
                    <div class="faq-question">
                        <span>{f1_q}</span>
                        <span class="faq-icon">+</span>
                    </div>
                    <div class="faq-answer">
                        <p>{f1_a}</p>
                    </div>
                </div>
                <div class="faq-item" onclick="this.classList.toggle('active')">
                    <div class="faq-question">
                        <span>{f2_q}</span>
                        <span class="faq-icon">+</span>
                    </div>
                    <div class="faq-answer">
                        <p>{f2_a}</p>
                    </div>
                </div>
                <div class="faq-item" onclick="this.classList.toggle('active')">
                    <div class="faq-question">
                        <span>{f3_q}</span>
                        <span class="faq-icon">+</span>
                    </div>
                    <div class="faq-answer">
                        <p>{f3_a}</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <div class="whatsapp-wrapper">
        <div class="whatsapp-text">Fale agora conosco</div>
        <a href="https://wa.me/5567999128212" class="whatsapp-float" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" style="width: 35px; height: 35px; fill: #FFF;"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7 .9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
        </a>
    </div>

    <footer>
        <div class="container">
            <p>&copy; 2025 Sabedoria Revelada. Todos os direitos reservados.</p>
        </div>
    </footer>

    <script>
        const lenis = new Lenis({{ duration: 1.2, easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), direction: 'vertical', gestureDirection: 'vertical', smooth: true, mouseMultiplier: 1, smoothTouch: false, touchMultiplier: 2, infinite: false }})
        function raf(time) {{ lenis.raf(time); requestAnimationFrame(raf); }}
        requestAnimationFrame(raf);
        const observer = new IntersectionObserver((entries) => {{ entries.forEach(entry => {{ if (entry.isIntersecting) {{ entry.target.classList.add('active'); }} }}); }}, {{ threshold: 0.1 }});
        document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
        window.addEventListener('scroll', () => {{ document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50); }});
    </script>
</body>
</html>
"""

configs = {
    "index.html": {
        "lang": "pt-BR", "title": "Sabedoria Revelada - Uma Chave Por Dia", "brand_name": "Sabedoria Revelada", "brand_sub": "Uma Chave Por Dia",
        "pt_active": "active", "en_active": "", "es_active": "", "btn_nav": "Acesso Gratuito",
        "badge_text": "Acesso gratuito encerra em 10 de maio", "tooltip_text": "Clique na chave e receba sabedoria diária.",
        "h1_main": "Uma chave pode abrir o que", "h1_span": "anos não conseguiram.",
        "hero_p": "Não é um devocional comum. É uma chave escavada da Palavra com método real — entregue todo dia, diretamente no seu e-mail.",
        "bento_title": "O que você vai receber.",
        "b1_title": "Profundidade Real", "b1_p": "Camadas culturais, linguísticas e históricas que a leitura comum nunca alcança. Mergulhe no texto original.",
        "b2_title": "Linguagem que Confronta", "b2_p": "Frases curtas. Ritmo intencional. Impacto que permanece.",
        "b3_title": "Aplicação Imediata", "b3_p": "Uma pergunta incisiva ao final de cada texto que não te deixa sair igual de como entrou.",
        "b4_title": "Entregue Todo Dia", "b4_p": "Direto no e-mail. Leitura de 3 min. Impacto para 24 horas. Disciplina sem esforço.",
        "samples_title": "Amostras Reais", "samples_p": "Três chaves reais provadas no texto. Este é o nível do que você recebe.",
        "s1_title": '"Quietude Que Combate"<br>(Êx 14.13–14)', "s1_p": 'A palavra militar "ficai quietos" era ordem de batalha, não meditação.',
        "s2_title": '"O Anônimo Que Fugiu Nu"<br>(Mc 14.51)', "s2_p": 'O único humano que foge nu nas Escrituras é Adão. O Getsêmani ecoou o Éden.',
        "s3_title": '"A Água Que Virou Oferta"<br>(2Sm 23.16)', "s3_p": 'Três homens romperam linhas de guerra por água. Davi entendeu: era sangue.',
        "pricing_title": "Acesso Ilimitado.", "price_huge": "R$50", "price_sub": "Por mês. Apenas R$ 1,66 por dia.", "btn_pricing": "Quero Receber as Chaves", "pricing_p": "Sem contratos. Cancele quando quiser com um clique.",
        "faq_title": "FAQ",
        "f1_q": "Como vou receber?", "f1_a": "Todo dia pela manhã no e-mail. É só abrir e ler.",
        "f2_q": "Tem período de fidelidade?", "f2_a": "Não. Cancele a qualquer momento direto na plataforma.",
        "f3_q": "Terei acesso aos textos passados?", "f3_a": "Sim! Ao assinar, você desbloqueia o arquivo histórico completo."
    },
    "index-en.html": {
        "lang": "en", "title": "Revealed Wisdom - A Key A Day", "brand_name": "Revealed Wisdom", "brand_sub": "A Key A Day",
        "pt_active": "", "en_active": "active", "es_active": "", "btn_nav": "Claim Free Access",
        "badge_text": "Free access ends May 10th", "tooltip_text": "Click the key and receive daily wisdom.",
        "h1_main": "One key a day can unlock what", "h1_span": "years couldn't.",
        "hero_p": "Not a typical devotional. It's a key excavated from the Word with a real method — delivered every day.",
        "bento_title": "What you will receive.",
        "b1_title": "Real Biblical Depth", "b1_p": "Cultural, linguistic, and historical layers that common reading never reaches.",
        "b2_title": "Language That Confronts", "b2_p": "Short sentences. Intentional rhythm. Impact that remains.",
        "b3_title": "Immediate Application", "b3_p": "An incisive question at the end of each text that changes you.",
        "b4_title": "Delivered Every Day", "b4_p": "Straight to your inbox. A 3-minute read. Impact for 24 hours.",
        "samples_title": "Real Samples", "samples_p": "Three real keys proven in the text. This is the level of what you receive.",
        "s1_title": '"Quietness That Fights"<br>(Ex 14:13–14)', "s1_p": 'The military word "be still" was an order of battle, not meditation.',
        "s2_title": '"The Anonymous Who Fled Naked"<br>(Mk 14:51)', "s2_p": 'The only human who flees naked in the Scriptures is Adam. Gethsemane echoed Eden.',
        "s3_title": '"The Water That Became an Offering"<br>(2Sam 23:16)', "s3_p": 'Three men broke through enemy lines for water. David understood: it was blood.',
        "pricing_title": "Unlimited Access.", "price_huge": "US$10", "price_sub": "Per month. Only US$ 0.33 per day.", "btn_pricing": "I Want to Receive the Keys", "pricing_p": "No contracts. Cancel anytime with one click.",
        "faq_title": "FAQ",
        "f1_q": "How will I receive it?", "f1_a": "Every morning in your email. Just open and read.",
        "f2_q": "Is there a loyalty period?", "f2_a": "No. Cancel anytime directly on the platform.",
        "f3_q": "Will I have access to past texts?", "f3_a": "Yes! By subscribing, you unlock the entire historical archive."
    },
    "index-es.html": {
        "lang": "es", "title": "Sabiduría Revelada - Una Llave Por Día", "brand_name": "Sabiduría Revelada", "brand_sub": "Una Llave Por Día",
        "pt_active": "", "en_active": "", "es_active": "active", "btn_nav": "Acceso Gratuito",
        "badge_text": "El acceso gratuito finaliza el 10 de mayo", "tooltip_text": "Haga clic en la llave y reciba sabiduría diaria.",
        "h1_main": "Una llave al día puede abrir lo que", "h1_span": "años no lograron.",
        "hero_p": "No es un devocional común. Es una llave excavada de la Palabra con un método real — entregada todos los días.",
        "bento_title": "Lo que recibirá.",
        "b1_title": "Profundidad Bíblica Real", "b1_p": "Capas culturales, lingüísticas e históricas que la lectura común nunca alcanza.",
        "b2_title": "Lenguaje que Confronta", "b2_p": "Frases cortas. Ritmo intencional. Un impacto que permanece.",
        "b3_title": "Aplicación Inmediata", "b3_p": "Una pregunta incisiva al final de cada texto que te cambia.",
        "b4_title": "Entregado Todos los Días", "b4_p": "Directo a tu correo. Lectura de 3 minutos. Impacto para 24 horas.",
        "samples_title": "Muestras Reales", "samples_p": "Tres llaves reales probadas en el texto. Este es el nivel de lo que recibes.",
        "s1_title": '"La Quietud que Combate"<br>(Éx 14.13–14)', "s1_p": 'La palabra militar "estad quietos" era una orden de batalla, no de meditación.',
        "s2_title": '"El Anónimo que Huyó Desnudo"<br>(Mc 14.51)', "s2_p": 'El único humano que huye desnudo en las Escrituras es Adán. Getsemaní se hizo eco del Edén.',
        "s3_title": '"El Agua que se Hizo Ofrenda"<br>(2Sm 23.16)', "s3_p": 'Tres hombres rompieron líneas enemigas por agua. David entendió: era sangre.',
        "pricing_title": "Acceso Ilimitado.", "price_huge": "US$10", "price_sub": "Por mes. Solo US$ 0.33 por día.", "btn_pricing": "Quiero Recibir las Llaves", "pricing_p": "Sin contratos. Cancele cuando quiera con un clic.",
        "faq_title": "Preguntas Frecuentes",
        "f1_q": "¿Cómo lo recibiré?", "f1_a": "Cada mañana en su correo. Solo ábralo y lea.",
        "f2_q": "¿Hay período de permanencia?", "f2_a": "No. Puede cancelar en cualquier momento directamente en la plataforma.",
        "f3_q": "¿Tendré acceso a textos anteriores?", "f3_a": "¡Sí! Al suscribirse, desbloquea todo el archivo histórico."
    }
}

directory_path = r"C:\Users\Lindomar de Alencar\.gemini\antigravity\scratch\chaves-diarias"

for filename, cfg in configs.items():
    rendered = html_template.format(**cfg)
    with open(os.path.join(directory_path, filename), "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"Built {filename}")
