import json
from pathlib import Path

p = Path(r"C:\Users\OMEN\AppData\Roaming\Code\User\settings.json")
if not p.exists():
    raise FileNotFoundError(p)

data = json.loads(p.read_text(encoding="utf-8"))

data["workbench.colorTheme"] = "Default Dark+"
data["workbench.colorCustomizations"] = {}
data["editor.tokenColorCustomizations"] = {}
data["editor.semanticTokenColorCustomizations"] = {}
data["editor.semanticHighlighting.enabled"] = False

p.write_text(json.dumps(data, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
print("updated", p)
