import os

file_path = "build_html.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove the dark overlay inside the modal if it exists to let the scroll show
content = content.replace('.scroll-overlay-dark {\n            position: absolute; inset: 0; background: rgba(10, 10, 10, 0.7);\n            border-radius: 20px; pointer-events: none;\n        }', '.scroll-overlay-dark { display: none; }')

# Change h3 color to dark brown for parchment
old_h3 = "        .scroll-content h3 { font-family: var(--font-display); font-size: 2.5rem; color: var(--accent); margin-bottom: 1rem; text-shadow: 0 2px 10px rgba(0,0,0,0.8); }"
new_h3 = "        .scroll-content h3 { font-family: var(--font-display); font-size: 2.5rem; color: #3d2314; margin-bottom: 1rem; text-shadow: none; display: none; }" 
# Note: The title is already in the text as <b>Dois Gravetos</b>, and scroll_title is empty, but just in case.
content = content.replace(old_h3, new_h3)

# Change p style to Times New Roman, dark text, no background box
old_p = "        .scroll-content p {\n            color: #f2f2f2; font-size: 1.1rem; line-height: 1.6; text-shadow: 0 2px 10px rgba(0,0,0,0.8); margin-bottom: 2rem; background: rgba(0,0,0,0.4); padding: 35px; border-radius: 12px; border: 1px solid rgba(229, 192, 123, 0.1); backdrop-filter: blur(10px); text-align: left;\n        }"
new_p = """        .scroll-content p {
            font-family: 'Times New Roman', Times, serif;
            color: #1a1a1a; font-size: 1.25rem; line-height: 1.6; text-shadow: none; margin-bottom: 2rem; background: transparent; padding: 0 10px; border: none; backdrop-filter: none; text-align: left;
        }"""
content = content.replace(old_p, new_p)

# Add custom scrollbar to the scroll-modal
css_scroll = """        .scroll-modal {
            width: 95vw; max-width: 800px;
            max-height: 90vh; overflow-y: auto;"""
css_scroll_new = """        .scroll-modal {
            width: 95vw; max-width: 800px;
            max-height: 90vh; overflow-y: auto;
            scrollbar-width: thin;
            scrollbar-color: rgba(139, 69, 19, 0.5) transparent;
        }
        .scroll-modal::-webkit-scrollbar { width: 8px; }
        .scroll-modal::-webkit-scrollbar-track { background: transparent; }
        .scroll-modal::-webkit-scrollbar-thumb { background: rgba(139, 69, 19, 0.5); border-radius: 10px; }"""
content = content.replace(css_scroll, css_scroll_new)

# Make the close button dark so it's visible on the bright parchment
old_close = "color: #fff; cursor: pointer;\n            font-size: 1.5rem; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);"
new_close = "color: #000; cursor: pointer;\n            font-size: 1.5rem; background: rgba(0,0,0,0.1); border: 1px solid rgba(0,0,0,0.2);"
content = content.replace(old_close, new_close)

# Increase padding of the modal to give the text room to breathe inside the parchment
content = content.replace("padding: 4rem 3rem; text-align: center;", "padding: 6rem 4rem; text-align: center;")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
