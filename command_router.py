from tool_runner import ToolRunner


class CommandRouter:

    def __init__(self):

        self.runner = ToolRunner()

    def handle(self, command):

        command = command.strip()

        if not command:
            return "Leerer Befehl."

        lower = command.lower()

        # ------------------------
        # Datei lesen
        # ------------------------

        if lower.startswith("lies datei"):

            path = command.replace(
                "lies datei",
                "",
                1
            ).strip()

            return self.runner.run(
                "read_file",
                path=path
            )

        # ------------------------
        # Datei schreiben
        # ------------------------

        if lower.startswith("schreibe datei"):

            try:

                parts = command.split("|", 1)

                path = (
                    parts[0]
                    .replace(
                        "schreibe datei",
                        "",
                        1
                    )
                    .strip()
                )

                content = parts[1].strip()

                success = self.runner.run(
                    "write_file",
                    path=path,
                    content=content
                )

                if success:
                    return (
                        f"Datei geschrieben: {path}"
                    )

                return "Fehler beim Schreiben."

            except Exception:

                return (
                    "Verwendung:\n"
                    "schreibe datei PFAD | TEXT"
                )

        # ------------------------
        # Datei anhängen
        # ------------------------

        if lower.startswith("hänge an datei"):

            try:

                parts = command.split("|", 1)

                path = (
                    parts[0]
                    .replace(
                        "hänge an datei",
                        "",
                        1
                    )
                    .strip()
                )

                content = (
                    "\n" +
                    parts[1].strip()
                )

                success = self.runner.run(
                    "append_file",
                    path=path,
                    content=content
                )

                if success:
                    return (
                        f"Text angehängt: {path}"
                    )

                return "Fehler beim Anhängen."

            except Exception:

                return (
                    "Verwendung:\n"
                    "hänge an datei PFAD | TEXT"
                )

        # ------------------------
        # Text ersetzen
        # ------------------------

        if lower.startswith("ersetze in datei"):

            try:

                parts = command.split(
                    "|"
                )

                file_path = (
                    parts[0]
                    .replace(
                        "ersetze in datei",
                        "",
                        1
                    )
                    .strip()
                )

                old_text = (
                    parts[1]
                    .strip()
                )

                new_text = (
                    parts[2]
                    .strip()
                )

                success = self.runner.run(
                    "replace_in_file",
                    path=file_path,
                    old_text=old_text,
                    new_text=new_text
                )

                if success:
                    return (
                        "Text ersetzt."
                    )

                return (
                    "Ersetzen fehlgeschlagen."
                )

            except Exception:

                return (
                    "Verwendung:\n"
                    "ersetze in datei PFAD | ALT | NEU"
                )

        # ------------------------
        # In Datei suchen
        # ------------------------

        if lower.startswith("suche in datei"):

            try:

                parts = command.split("|", 1)

                file_path = (
                    parts[0]
                    .replace(
                        "suche in datei",
                        "",
                        1
                    )
                    .strip()
                )

                search_text = parts[1].strip()

                return self.runner.run(
                    "search_in_file",
                    path=file_path,
                    query=search_text
                )

            except Exception:

                return (
                    "Verwendung:\n"
                    "suche in datei PFAD | SUCHTEXT"
                )

        # ------------------------
        # Ordner anzeigen
        # ------------------------

        if lower.startswith("zeige ordner"):

            path = command.replace(
                "zeige ordner",
                "",
                1
            ).strip()

            return self.runner.run(
                "list_files",
                path=path
            )

        # ------------------------
        # Directory Tree
        # ------------------------

        if lower.startswith("zeige baum"):

            path = command.replace(
                "zeige baum",
                "",
                1
            ).strip()

            return self.runner.run(
                "directory_tree",
                path=path
            )

        # ------------------------
        # Ordner erstellen
        # ------------------------

        if lower.startswith("erstelle ordner"):

            path = command.replace(
                "erstelle ordner",
                "",
                1
            ).strip()

            success = self.runner.run(
                "create_folder",
                path=path
            )

            if success:
                return (
                    f"Ordner erstellt: {path}"
                )

            return "Fehler beim Erstellen."

        # ------------------------
        # Datei löschen
        # ------------------------

        if lower.startswith("lösche datei"):

            path = command.replace(
                "lösche datei",
                "",
                1
            ).strip()

            success = self.runner.run(
                "delete_file",
                path=path
            )

            if success:
                return (
                    f"Datei gelöscht: {path}"
                )

            return "Fehler beim Löschen."

        return (
            f"Befehl nicht erkannt: {command}"
        )


if __name__ == "__main__":

    router = CommandRouter()

    print(
        "\n=== OpenJarvis Command Router ==="
    )

    print(
        "\nVerfügbare Befehle:"
    )

    print(
        "lies datei <pfad>"
    )

    print(
        "schreibe datei <pfad> | <text>"
    )

    print(
        "hänge an datei <pfad> | <text>"
    )

    print(
        "ersetze in datei <pfad> | <alt> | <neu>"
    )

    print(
        "suche in datei <pfad> | <text>"
    )

    print(
        "zeige ordner <pfad>"
    )

    print(
        "zeige baum <pfad>"
    )

    print(
        "erstelle ordner <pfad>"
    )

    print(
        "lösche datei <pfad>"
    )

    print(
        "\nexit = beenden\n"
    )

    while True:

        command = input(
            "Befehl: "
        )

        if command.lower() in [
            "exit",
            "quit",
            "ende"
        ]:
            break

        try:

            result = router.handle(
                command
            )

            print(
                "\nErgebnis:"
            )

            print(result)

        except Exception as e:

            print(
                f"\nFehler: {e}"
            )