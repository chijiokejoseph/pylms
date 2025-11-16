import subprocess
from pathlib import Path

print("⚠️ Please activate your virtual environment before running script\n")

response = input("Confirm that your virtual env is active ['yes'/'no']: ").lower()

if response not in ["yes", "y"]:
    exit()

parent = Path(__file__).parent
target_dir = parent / ".venv" / "Lib" / "site-packages" / "src.pth"
activate_py = parent / ".venv" / "Scripts" / "activate_this.py"
src_dir = parent / "src"

with target_dir.open("w") as file:
    _ = file.write(str(src_dir))
print("✅ Configured src folder")

_ = subprocess.run(["uv", "sync"])
print("✅ synced virtual env")
