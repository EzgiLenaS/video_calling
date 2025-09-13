# .github/scripts/update_readme_template.py

import random, re, subprocess, time, hashlib, json
from datetime import datetime
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None

README = Path("README.md")
STATE  = Path(".github/scripts/_auto_state.json")

# 1–3 commit/gün
commit_count = random.randint(1, 3)
# her kategoride tutulacak maksimum satır
PER_CAT_KEEP = 12

# Kategoriler (istediğin gibi sırayı/öğeleri değiştirebilirsin)
CATEGORIES = ["Feature", "Tip", "Status"]

FEATURES = [
    "Stylish dark and light UI themes included.",
    "Screen sharing now works smoothly in group calls.",
    "Recording option saves sessions for later playback.",
    "Real-time reactions make chats more interactive.",
    "Secure login with JWT-based authentication.",
]

TIPS = [
    "Use Chrome for the best WebRTC stability.",
    "Share only a single window for better privacy.",
    "Check your .env configuration before running locally.",
    "Use headphones to avoid audio echo during calls.",
    "Update dependencies regularly for smoother builds.",
]

STATUSES = [
    "Average call setup time < 500ms in last tests.",
    "Message delivery success rate > 99%.",
    "Error handling improved on both frontend & backend.",
    "TURN servers active for strict NAT environments.",
    "Deployment ready with free hosting platforms.",
]

def now_tr():
    if ZoneInfo:
        return datetime.now(ZoneInfo("Europe/Istanbul"))
    return datetime.now()

def read_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"seq": 0, "last_cat": None}

def write_state(st):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")

# --- README içindeki AUTO-UPDATED bloğunu ve kategori başlıklarını yönetim ---

SKELETON = (
    "<!-- AUTO-UPDATED:START -->\n"
    "### Feature\n\n"
    "### Tip\n\n"
    "### Status\n"
    "<!-- AUTO-UPDATED:END -->"
)

# Bölüm aralıklarını yakalamak için regex
# Not: DOTALL ile çalışır; non-greedy (.*?) ve lookahead ile bir sonraki başlığa kadar alır
SECTION_PATTERNS = {
    "Feature": re.compile(r"(### Feature\s*\n)(.*?)(?=\n### Tip|\n### Status|<!-- AUTO-UPDATED:END -->)", re.S),
    "Tip":     re.compile(r"(### Tip\s*\n)(.*?)(?=\n### Feature|\n### Status|<!-- AUTO-UPDATED:END -->)", re.S),
    "Status":  re.compile(r"(### Status\s*\n)(.*?)(?=\n### Feature|\n### Tip|<!-- AUTO-UPDATED:END -->)", re.S),
}

AUTO_WRAPPER_RE = re.compile(r"(<!-- AUTO-UPDATED:START -->)(.*?)(<!-- AUTO-UPDATED:END -->)", re.S)

def ensure_block(body: str) -> str:
    if "<!-- AUTO-UPDATED:START -->" in body and "<!-- AUTO-UPDATED:END -->" in body:
        return body
    # Yoksa en sona iskeleti ekle
    base = body if body else "# Auto Updates\n\n"
    if not base.endswith("\n"):
        base += "\n"
    return base + "\n" + SKELETON + "\n"

def read_readme() -> str:
    return README.read_text(encoding="utf-8") if README.exists() else ""

def write_readme(txt: str):
    README.write_text(txt, encoding="utf-8")

def get_section_lines(section_text: str):
    # mevcut bullet'ları al; boş satırları at
    lines = [l.rstrip() for l in section_text.strip().splitlines() if l.strip()]
    return lines

def set_section(body_inside: str, category: str, new_lines: list) -> str:
    """
    AUTO-UPDATED bloğunun İÇ kısmını alır, category bölümünü new_lines ile günceller ve geri döner.
    """
    pat = SECTION_PATTERNS[category]
    m = pat.search(body_inside)
    if not m:
        # başlık yoksa (olmaz ama), sonuna ekleyelim
        body_inside = body_inside.rstrip() + f"\n\n### {category}\n" + "\n".join(new_lines) + "\n"
        return body_inside
    start_hdr, cur_section = m.group(1), m.group(2)
    updated = start_hdr + ("\n".join(new_lines) + ("\n" if new_lines else ""))  # başlığın altını yaz
    # Eski bölümü updated ile değiştir
    body_inside = body_inside[:m.start()] + updated + body_inside[m.end():]
    return body_inside

def insert_item(category: str, item_text: str):
    """
    İlgili kategori altına "- [#XXXX] item_text" maddesi ekler; per-cat limit uygular.
    """
    body = read_readme()
    body = ensure_block(body)

    # AUTO bloğunun içini yakala
    m = AUTO_WRAPPER_RE.search(body)
    if not m:
        # çok düşük ihtimal; güvenli fallback
        body = ensure_block(body)
        m = AUTO_WRAPPER_RE.search(body)

    before, middle, after = body[:m.start(2)], m.group(2), body[m.end(2):]

    # İlgili bölümün mevcut satırlarını oku
    pat = SECTION_PATTERNS[category]
    sec = pat.search(middle)
    if sec:
        cur_lines = get_section_lines(sec.group(2))
    else:
        cur_lines = []

    # yeni maddeyi ekle (timestamp yok)
    cur_lines.append(item_text)
    # sadece son PER_CAT_KEEP maddeleri tut
    cur_lines = cur_lines[-PER_CAT_KEEP:]

    # bölümü güncelle
    middle = set_section(middle, category, cur_lines)

    # geri yaz
    new_body = before + middle + after
    write_readme(new_body)

# --- Git yardımcı ---

def git(args):
    subprocess.run(args, check=True)

# --- Satır üretimi (kategori bazlı metin seçer) ---

def pick_line_text(cat: str) -> str:
    if cat == "Feature": return random.choice(FEATURES)
    if cat == "Tip":     return random.choice(TIPS)
    if cat == "Status":  return random.choice(STATUSES)
    return "Minor maintenance."

def cycle_next(last):
    if last in CATEGORIES:
        return CATEGORIES[(CATEGORIES.index(last)+1) % len(CATEGORIES)]
    return CATEGORIES[0]

# --- Ana akış ---

def main():
    st = read_state()
    for i in range(1, commit_count + 1):
        st["seq"] = int(st.get("seq", 0)) + 1
        cat = cycle_next(st.get("last_cat"))
        # zaman damgası YOK; sadece sıra numarası + metin
        bullet = f"- [#{st['seq']:04d}] {pick_line_text(cat)}"

        insert_item(cat, bullet)
        st["last_cat"] = cat
        write_state(st)

        git(["git", "add", str(README), str(STATE)])
        git(["git", "commit", "-m", f"chore(readme): {cat.lower()} note #{st['seq']:04d} ({i}/{commit_count}) [auto-readme] [skip ci]"])
        git(["git", "push"])
        time.sleep(1)

if __name__ == "__main__":
    main()