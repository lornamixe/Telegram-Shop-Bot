import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV = ROOT / "venv"

VENV_PY = VENV / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")

def run(*args):
    subprocess.run([str(a) for a in args], check=True, cwd=ROOT)
    
def read_env(path):
    result = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                result[key.strip()]=value.strip()
    return result
    
def main():
    if sys.version_info < (3,10):
        sys.exit("[ERROR] Python 3.10 or newer is required")
       
    print("[1/4] Virtual environment...")
    if not VENV_PY.exists():
        venv.create(VENV, with_pip=True)
    else:
        print("Already exists, skipping")
    
    print("[2/4] Installing dependencies...")
    run(VENV_PY, "-m", "pip","install","--upgrade","pip","-q")
    run(VENV_PY, "-m", "pip","install","-r","requirements.txt")
    
    print("[3/4] .env file")
    
    env = ROOT / ".env"
    
    existing = read_env(env)
    additions = []
    
    if not existing.get("BOT_TOKEN"):
        token = input("Enter BOT_TOKEN from @BotFather: ").strip()
        additions.append(f"BOT_TOKEN={token}")
    if "ADMIN_IDS" not in existing:
        while True:
            raw = input("Admin Telegram IDs, comma-separated (press Enter to skip): ")
            ids = [x for x in raw.replace(" ", "").split(",") if x]
            if all(x.isdigit() for x in ids):
                break
            print("IDs must contain digits only, please try again.")
        additions.append(f"ADMIN_IDS={','.join(ids)}")
    if additions:
        text = env.read_text(encoding="utf-8") if env.exists() else ""
        if text and not text.endswith("\n"):
            text += "\n"
        env.write_text(text+"\n".join(additions)+"\n", encoding="utf-8")
        print(".env updated")
    else:
        print("everything is already filled in, skipping")
        
    print("[4/4] Database...")
    run(VENV_PY, "init_db.py")
    
    print("\nDone! Start the bot with: python run.py")
    
    
if __name__=="__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.exit(f"[ERROR] Command failed: {e}")