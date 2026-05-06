import os
import re

file_path = "build_html.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CSS for Scroll Modal
old_scroll_css = """        /* Scroll Modal behind doors */
        .scroll-modal-container {
            position: fixed; inset: 0; z-index: 99997; pointer-events: none;
            display: flex; align-items: center; justify-content: center;
            background: rgba(0,0,0,0.85); backdrop-filter: blur(20px);
            opacity: 0; transition: opacity 0.5s ease 0.5s; /* fades in after doors start opening */
        }
        body.portal-active .scroll-modal-container { pointer-events: auto; opacity: 1; z-index: 99999; }

        .scroll-modal {
            width: 95vw; max-width: 800px;
            max-height: 90vh; overflow-y: auto;
            scrollbar-width: thin; scrollbar-color: rgba(139, 69, 19, 0.5) transparent;
            background-image: url('mystical_ancient_scroll_1778070821283.png');
            background-size: cover; background-position: center;
            border-radius: 20px; box-shadow: 0 30px 100px rgba(0,0,0,0.9), 0 0 80px rgba(229,192,123,0.3);
            padding: 6rem 4rem; text-align: center;
            position: relative;
            transform: translateY(0);
            clip-path: polygon(0 0, 100% 0, 100% 0, 0 0); /* Rolled up completely */
            transition: clip-path 2.5s cubic-bezier(0.25, 1, 0.5, 1) 0.5s; /* Unrolls after doors open */
        }
        .scroll-modal::-webkit-scrollbar { width: 8px; }
        .scroll-modal::-webkit-scrollbar-track { background: transparent; }
        .scroll-modal::-webkit-scrollbar-thumb { background: rgba(139, 69, 19, 0.5); border-radius: 10px; }
        
        body.portal-active .scroll-modal { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); }
        
        .scroll-overlay-dark {
            display: none;
        }

        .scroll-close {
            position: absolute; top: 20px; right: 20px; color: #000; cursor: pointer;
            font-size: 1.5rem; background: rgba(0,0,0,0.1); border: 1px solid rgba(0,0,0,0.2);
            width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 10;
            transition: all 0.3s;
        }
        .scroll-close:hover { background: rgba(255,255,255,0.2); transform: scale(1.1); }

        .scroll-content { position: relative; z-index: 2; }
        .scroll-content h3 { display: none; }
        .scroll-content p { 
            font-family: 'Times New Roman', Times, serif; 
            color: #1a1a1a; font-size: 1.25rem; line-height: 1.6; text-shadow: none; 
            margin-bottom: 2rem; background: transparent; padding: 0 10px; 
            border: none; backdrop-filter: none; text-align: left; 
        }"""

new_scroll_css = """        /* Scroll Modal behind doors */
        .scroll-modal-container {
            position: fixed; inset: 0; z-index: 99997; pointer-events: none;
            display: flex; justify-content: center;
            background-color: #f4ecd8; /* Parchment base */
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.4'/%3E%3C/svg%3E");
            opacity: 0; transition: opacity 2s ease 1s; /* Fades in smoothly as doors open */
        }
        body.portal-active .scroll-modal-container { pointer-events: auto; opacity: 1; z-index: 99999; }

        .scroll-modal {
            width: 100vw; max-width: 900px; height: 100vh;
            overflow-y: auto; overflow-x: hidden;
            padding: 15vh 5vw 20vh; /* Plenty of space top and bottom */
            scrollbar-width: thin; scrollbar-color: rgba(139, 69, 19, 0.5) transparent;
            position: relative;
            scroll-behavior: smooth;
        }
        .scroll-modal::-webkit-scrollbar { width: 8px; }
        .scroll-modal::-webkit-scrollbar-track { background: transparent; }
        .scroll-modal::-webkit-scrollbar-thumb { background: rgba(139, 69, 19, 0.5); border-radius: 10px; }
        
        .scroll-close {
            position: fixed; top: 30px; right: 30px; color: #fff; cursor: pointer;
            font-size: 1.5rem; background: rgba(0,0,0,0.8); border: 1px solid rgba(255,255,255,0.2);
            width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 100000;
            transition: all 0.3s; box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }
        .scroll-close:hover { background: #000; transform: scale(1.1); }

        .scroll-content { position: relative; z-index: 2; }
        .scroll-content h3 { display: none; }
        .scroll-content p { 
            font-family: 'Times New Roman', Times, serif; 
            color: #2E1F11; font-size: 1.4rem; line-height: 1.8; text-shadow: none; 
            margin-bottom: 2rem; background: transparent; padding: 0; 
            border: none; backdrop-filter: none; text-align: left; 
        }
        
        /* Make button match parchment style */
        .scroll-content .btn-huge {
            background: #2E1F11; color: #f4ecd8; border: 2px solid #2E1F11; box-shadow: none;
        }
        .scroll-content .btn-huge::before { background: #4a331c; }
        .scroll-content .btn-huge:hover { color: #fff; box-shadow: 0 10px 30px rgba(46, 31, 17, 0.4); }"""

content = content.replace(old_scroll_css, new_scroll_css)

# 2. Add Javascript for Auto-Scroll
js_insert = """
        let autoScrollInterval;
        let isHovered = false;

        function startAutoScroll() {
            const modal = document.querySelector('.scroll-modal');
            modal.scrollTop = 0; // reset scroll
            clearInterval(autoScrollInterval);
            
            // Start scrolling after 4 seconds to give user time to start reading
            setTimeout(() => {
                autoScrollInterval = setInterval(() => {
                    if (!isHovered && document.body.classList.contains('portal-active') && modal.scrollTop < (modal.scrollHeight - modal.clientHeight - 50)) {
                        modal.scrollTop += 1;
                    }
                }, 40); // Controls speed (higher is slower)
            }, 4000);
        }

        document.querySelector('.scroll-modal').addEventListener('mouseenter', () => isHovered = true);
        document.querySelector('.scroll-modal').addEventListener('mouseleave', () => isHovered = false);
        document.querySelector('.scroll-modal').addEventListener('touchstart', () => isHovered = true);
        document.querySelector('.scroll-modal').addEventListener('touchend', () => { setTimeout(() => isHovered=false, 2000) });
"""

# Insert js_insert before function turnKey
content = content.replace("function turnKey(e) {", js_insert + "\n        function turnKey(e) {")

# Call startAutoScroll inside turnKey
content = content.replace("document.body.classList.add('portal-active');", "document.body.classList.add('portal-active');\n                startAutoScroll();")

# Clear interval on close
content = content.replace("document.body.classList.remove('portal-active');", "document.body.classList.remove('portal-active');\n            clearInterval(autoScrollInterval);")

# Save changes
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
