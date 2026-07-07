import os
import re

html_files = [f for f in os.listdir('static') if f.endswith('.html')]

footer_pattern = re.compile(r'<footer class="footer-suscribete">.*?</footer>', re.DOTALL)
new_footer = """<footer style="background-color: var(--mustard-bg); padding: 2rem 0; text-align: center; color: white; margin-top: auto;">
        <div class="container">
            <p>&copy; 2026 Chispa Experience. Todos los derechos reservados.</p>
        </div>
    </footer>"""

for file in html_files:
    if file in ['contacto.html', 'cafeteria.html']:
        continue
    filepath = os.path.join('static', file)
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace header links
    content = content.replace('<a href="#">CONTACTO</a>', '<a href="/contacto.html">CONTACTO</a>')
    content = content.replace('<a href="#">CAFETERÍA</a>', '<a href="/cafeteria.html">CAFETERÍA</a>')
    
    # Replace footer
    content = footer_pattern.sub(new_footer, content)
    
    with open(filepath, 'w') as f:
        f.write(content)
        print(f"Updated {file}")

