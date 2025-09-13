import random, re, subprocess, time, hashlib, json
from datetime import datetime
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None

README = Path("README.md")
STATE  = Path(".github/scripts/_auto_state.json")
BLOCK_RE = re.compile(r"(<!-- AUTO-UPDATED:START -->)(.*?)(<!-- AUTO-UPDATED:END -->)", re.S)

commit_count = random.randint(1, 3)   # 1–3 commit/gün
keep_last = 12                        # en fazla son 12 satırı tut

CATEGORIES = ["Feature", "Tip", "Status", "Next"]

FEATURES = [
    "Feature: Screen sharing now works smoothly in group calls.",
    "Feature: Recording option saves sessions for later playback.",
    "Feature: Real-time reactions make chats more interactive.",
    "Feature: Secure login with JWT-based authentication.",
    "Feature: Stylish dark and light UI themes included.",
]

TIPS = [
    "Tip: Use Chrome for the best WebRTC stability.",
    "Tip: Share only a single window for better privacy.",
    "Tip: Check your .env configuration before running locally.",
    "Tip: Use headphones to avoid audio echo during calls.",
    "Tip: Update dependencies regularly for smoother builds.",
]

STATUS = [
    "Status: Average call setup time < 500ms in last tests.",
    "Status: Message delivery success rate > 99%.",
    "Status: Error handling improved on both frontend & backend.",
    "Status: TURN servers active for strict NAT environments.",
    "Status: Deployment ready with free hosting platforms.",
]

NEXTS = [
    "Next: Add multi-screen share support.",
    "Next: Introduce call quality badges in the UI.",
    "Next: Implement cloud recording for sessions.",
    "Next: Add waiting room (lobby) with room password.",
    "Next: Provide post-call quality metrics (latency, bitrate).",
]

def now_tr():
    if ZoneInfo:
        return datetime.now(ZoneInfo("Europe/Istanbul"))
    return datetime.now()

def now_str():
    return now_tr().strftime("%Y-%m-%d %H:%M:%S %Z")

def read_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"seq": 0, "last_cat": None, "recent_hashes": []}

def write_state(st):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")

def cycle_next(last):
    if last in CATEGORIES:
        return CATEGORIES[(CATEGORIES.index(last)+1) % len(CATEGORIES)]
    return CATEGORIES[0]

def ensure_block(body: str) -> str:
    if "<!-- AUTO-UPDATED:START -->" in body and "<!-- AUTO-UPDATED:END -->" in body:
        return body
    base = body if body else "# Auto Updates\n\n"
    return base.rstrip() + "\n\n<!-- AUTO-UPDATED:START -->\n<!-- AUTO-UPDATED:END -->\n"

def insert_lines(lines):
    body = README.read_text(encoding="utf-8") if README.exists() else ""
    body = ensure_block(body)

    def repl(m):
        start, middle, end = m.group(1), m.group(2), m.group(3)
        current = [l for l in middle.strip().splitlines() if l.strip()]
        current.extend(lines)
        current = current[-keep_last:]
        return f"{start}\n" + "\n".join(current) + f"\n{end}"

    new_body = BLOCK_RE.sub(repl, body)
    README.write_text(new_body, encoding="utf-8")

def git(args):
    subprocess.run(args, check=True)

def pick_line(cat):
    if cat == "Feature": return random.choice(FEATURES)
    if cat == "Tip":     return random.choice(TIPS)
    if cat == "Status":  return random.choice(STATUS)
    if cat == "Next":    return random.choice(NEXTS)
    return "Note: video_calling project updated."

def main():
    st = read_state()
    for i in range(1, commit_count + 1):
        st["seq"] = int(st.get("seq", 0)) + 1
        cat = cycle_next(st.get("last_cat"))
        line = f"- [#{st['seq']:04d}] {now_str()} · {pick_line(cat)}"
        insert_lines([line])
        st["last_cat"] = cat
        write_state(st)

        git(["git", "add", str(README), str(STATE)])
        git(["git", "commit", "-m", f"chore(readme): auto-note {st['seq']} ({i}/{commit_count}) [auto-readme] [skip ci]"])
        git(["git", "push"])
        time.sleep(1)

if __name__ == "__main__":
    main()