import os, random, re, subprocess
from datetime import datetime, timezone

README_PATH = "README.md"

# 1–3 commit arasında rastgele
commit_count = random.randint(1, 3)

def readme_text():
    with open(README_PATH, "r", encoding="utf-8") as f:
        return f.read()

def write_readme(text):
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(text)

def update_once(n):
    text = readme_text()

    # ISO saat damgası (İstanbul saati gibi görünsün)
    # GitHub runner UTC, ama çıktıda +03:00 göstermek için manüel ofset verelim.
    # Pratik: İstanbul hep UTC+3
    ist_now = datetime.utcnow()
    stamp = ist_now.replace(tzinfo=timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    block_re = re.compile(r"(<!-- AUTO-UPDATED:START -->)(.*?)(<!-- AUTO-UPDATED:END -->)", re.S)
    if not block_re.search(text):
        # Blok yoksa en sona ekleyelim
        text += "\n\n<!-- AUTO-UPDATED:START -->\n<!-- AUTO-UPDATED:END -->\n"

    def repl(m):
        start, body, end = m.group(1), m.group(2), m.group(3)
        lines = [l for l in body.strip().splitlines() if l.strip()]
        # README’yi “karışık” yapmadan küçük, anlamlı bir satır ekle
        new_line = f"Son otomatik güncelleme: {stamp} · sürüm {random.randint(1000,9999)}"
        # Aynı gün çoklu commitlerde fark yaratmak için satır dizisinin sonuna ekle/çıkar döngüsü
        lines.append(new_line)
        # Çok uzamasın diye en fazla son 10 satırı tut
        lines = lines[-10:]
        new_body = "\n" + "\n".join(lines) + "\n"
        return f"{start}{new_body}{end}"

    new_text = block_re.sub(repl, text)
    write_readme(new_text)

    # Commit ve push
    # [skip ci] koyarsak bu commit başka workflow tetiklemez.
    subprocess.run(["git", "add", README_PATH], check=True)
    subprocess.run(["git", "commit", "-m", f"chore: daily README update ({n}/{commit_count}) [skip ci]"], check=True)
    subprocess.run(["git", "push"], check=True)

for i in range(1, commit_count + 1):
    update_once(i)
