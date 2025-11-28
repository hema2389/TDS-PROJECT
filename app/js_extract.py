import re
import base64

def extract_embedded_html(html: str) -> str:
    """
    Extracts innerHTML content set inside <script> tags.
    Handles:
      atob("...")
      atob(`...`)
      element.innerHTML = "..."
      element.innerHTML = `...`
    """
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", html, flags=re.S)

    extracted = []

    for s in scripts:

        # Case 1: atob("...")
        b64 = re.findall(r'atob\(["`\' ]*([A-Za-z0-9+/=]+)["`\' ]*\)', s)
        for b in b64:
            try:
                decoded = base64.b64decode(b).decode("utf-8", errors="ignore")
                extracted.append(decoded)
            except Exception:
                pass

        # Case 2: innerHTML = "..."
        inner = re.findall(r'innerHTML\s*=\s*["`\' ](.*?)["`\' ]', s, flags=re.S)
        extracted.extend(inner)

    return "\n".join(extracted)
