import os

html_files = [f for f in os.listdir('static') if f.endswith('.html')]

for file in html_files:
    filepath = os.path.join('static', file)
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace the placeholder logo with our new logo
    content = content.replace(
        '<img src="https://via.placeholder.com/150x80/ffffff/E83D7C?text=CHISPA" alt="Chispa Logo" style="border-radius: 50%;">',
        '<img src="/static/logo.jpg" alt="Chispa Logo">'
    )
    
    with open(filepath, 'w') as f:
        f.write(content)
        print(f"Updated logo in {file}")

