from bs4 import BeautifulSoup
from .js_extract import extract_embedded_html

async def extract_question(html: str) -> dict:
    """
    Combine raw HTML text + JS-decoded content.
    """
    extracted_js = extract_embedded_html(html)

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    return {"raw_text": text + " " + extracted_js}
