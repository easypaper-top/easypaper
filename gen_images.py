# -*- coding: utf-8 -*-
import requests, base64, os

API_URL = "https://api.mcxhm.cn/v1/images/generations"
API_KEY = "sk-3YF565NKFT9PuOegwfTMyAa7U4xRCFc19ZlttWXDloPgf6Zi"
PROXIES = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
OUT_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(OUT_DIR, exist_ok=True)


def gen_image(prompt, filename, size="1536x1024"):
    print(f"Generating {filename}...")
    r = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={"model": "gpt-image-2", "prompt": prompt, "n": 1, "size": size},
        proxies=PROXIES,
        timeout=120,
    )
    if r.status_code == 200:
        data = r.json()
        b64 = data["data"][0]["b64_json"]
        path = os.path.join(OUT_DIR, filename)
        with open(path, "wb") as f:
            f.write(base64.b64decode(b64))
        print(f"  OK: {filename} ({os.path.getsize(path) // 1024}KB)")
        return True
    else:
        print(f"  FAIL: {r.status_code} - {r.text[:200]}")
        return False


# 1. Hero banner: paper formatting pain vs one-click solution
gen_image(
    "Flat illustration, split screen design. Left side: a stressed graduate student surrounded by messy Word documents with red track-changes marks, formatting chaos, clock showing deadline pressure. Right side: the same student relaxed and smiling, with a clean beautifully typeset LaTeX paper on screen, a magic one-click conversion arrow between the two sides. Color palette: left side warm red/orange tones (stress), right side cool blue/purple tones (calm). Modern minimal vector style, no text, academic setting.",
    "hero.png",
)

# 2. Feature: Word format-preserving translation
gen_image(
    "Clean flat illustration showing a Word document being translated from Chinese to English. The document has tables, figures, headers and formatting that remain perfectly intact after translation. Show two documents side by side connected by a glowing translation arrow. Left doc has Chinese text, right doc has English text, both with identical layout, tables, and images. Soft gradient background in light blue. Modern SaaS product illustration style, no text labels.",
    "feature_translate.png",
)

# 3. Feature: Word to LaTeX conversion
gen_image(
    "Clean flat illustration showing document conversion workflow. A Word/docx file icon on the left transforms into a beautifully formatted LaTeX academic paper on the right. Show the conversion process with a stylized arrow or pipeline. The LaTeX output shows proper mathematical equations, structured sections, bibliography. Academic journal style (Elsevier). Soft purple gradient background. Modern minimal vector style, no text.",
    "feature_latex.png",
)
