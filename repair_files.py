# repair_files.py

from pathlib import Path

FILES = [
    "openjarvis_core.py",
    "command_router.py",
    "tool_runner.py",
    "project_manager.py",
    "memory_store.py",
    "task_manager.py"
]

REPLACEMENTS = {

    "<br>": "",

    "lÃ¶schen": "löschen",
    "gelÃ¶scht": "gelöscht",

    "nÃ¤chste": "nächste",
    "NÃ¤chste": "Nächste",

    "GedÃ¤chtnis": "Gedächtnis",

    "heiÃŸe": "heiße",
    "heiÃŸt": "heißt",

    "AnhÃ¤ngen": "Anhängen",

    "LÃ¶schen": "Löschen",

    "â””â”€â”€": "└──",
    "â”œâ”€â”€": "├──",
    "â”‚": "│"
}


for filename in FILES:

    path = Path(filename)

    if not path.exists():
        continue

    text = path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    for old, new in REPLACEMENTS.items():

        text = text.replace(
            old,
            new
        )

    path.write_text(
        text,
        encoding="utf-8"
    )

    print(
        f"Repariert: {filename}"
    )

print(
    "\nFertig."
)