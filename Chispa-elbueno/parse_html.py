from bs4 import BeautifulSoup

with open('/Users/macbook/.gemini/antigravity/brain/09f84b8f-e5c3-440a-abee-054fc84eeaf4/.system_generated/steps/57/content.md', 'r', encoding='utf-8') as f:
    html = f.read()

# Skip the header lines added by the system
html = html.split('---', 1)[-1] if '---' in html else html

soup = BeautifulSoup(html, 'html.parser')
print(soup.get_text(separator='\n', strip=True)[:1500])
