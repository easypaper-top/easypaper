# -*- coding: utf-8 -*-
"""Generate realistic before/after comparison images for landing page."""
import requests, base64, os

API_URL = "https://api.mcxhm.cn/v1/images/generations"
API_KEY = "sk-3YF565NKFT9PuOegwfTMyAa7U4xRCFc19ZlttWXDloPgf6Zi"
PROXIES = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
OUT_DIR = os.path.join(os.path.dirname(__file__), "images")


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


# Case 1: Translation before/after - a Chinese academic paper with tables translated to English
gen_image(
    "A realistic screenshot comparison of academic document translation. Left side labeled 'Before': a Microsoft Word document showing a Chinese academic paper with a complex table containing numerical data (3 columns, 5 rows with headers like '方法', '准确率', 'F1值'), Chinese paragraph text above the table, and a figure caption in Chinese below. Right side labeled 'After': the exact same document layout but all text is now in English, the table structure is perfectly preserved with same numbers, same formatting, same figure position. Both sides show the Word toolbar at top. Clean white background, realistic Word UI, 16:9.",
    "case_translate.png",
)

# Case 2: Word to LaTeX conversion - showing a Word doc becoming a beautifully typeset LaTeX PDF
gen_image(
    "A realistic screenshot comparison showing Word-to-LaTeX conversion. Left side labeled 'Word Input': a Microsoft Word document showing an academic paper with title 'Research on Deep Learning Methods', author names, abstract section, a mathematical equation (loss function with summation), and a numbered reference list [1][2][3]. Right side labeled 'LaTeX Output': a beautifully typeset two-column academic paper in Elsevier journal style, showing the same content but with professional LaTeX typography - proper math rendering, elegant fonts, structured bibliography, journal header. Realistic computer screen look, 16:9.",
    "case_latex.png",
)
