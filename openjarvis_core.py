from pathlib import Path

from path_sandbox import PathSandbox


class OpenJarvisFileSystem:

    def __init__(self, allowed_paths=None):

        self.base_path = Path.cwd().resolve()

        if allowed_paths is None:

            allowed_paths = [
                str(self.base_path)
            ]

        self.sandbox = PathSandbox(
            allowed_paths
        )

    def list_files(self, path):

        try:

            target = self.sandbox.validate(
                path
            )

            if not target.exists():
                return []

            return [
                str(item)
                for item in target.iterdir()
            ]

        except Exception as e:

            print(
                f"[WARN] Fehler beim Listen: {e}"
            )

            return []

    def read_file(self, path):

        try:

            target = self.sandbox.validate(
                path
            )

            if not target.exists():

                print(
                    f"[WARN] Datei nicht gefunden: {target}"
                )

                return None

            try:

                return target.read_text(
                    encoding="utf-8"
                )

            except UnicodeDecodeError:

                return target.read_text(
                    encoding="cp1252",
                    errors="ignore"
                )

        except Exception as e:

            print(
                f"[Fehler] Lesen: {e}"
            )

            return None

    def write_file(
        self,
        path,
        content
    ):

        try:

            target = self.sandbox.validate(
                path
            )

            target.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            target.write_text(
                content,
                encoding="utf-8"
            )

            return True

        except Exception as e:

            print(
                f"[Fehler] Schreiben: {e}"
            )

            return False

    def append_file(
        self,
        path,
        content
    ):

        try:

            target = self.sandbox.validate(
                path
            )

            target.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with open(
                target,
                "a",
                encoding="utf-8"
            ) as file:

                file.write(content)

            return True

        except Exception as e:

            print(
                f"[Fehler] Anhängen: {e}"
            )

            return False

    def search_in_file(
        self,
        path,
        query
    ):

        content = self.read_file(
            path
        )

        if content is None:
            return []

        matches = []

        for index, line in enumerate(
            content.splitlines(),
            start=1
        ):

            if query.lower() in line.lower():

                matches.append(
                    index
                )

        return matches

    def replace_in_file(
        self,
        path,
        old_text,
        new_text
    ):

        try:

            target = self.sandbox.validate(
                path
            )

            content = self.read_file(
                path
            )

            if content is None:
                return False

            updated_content = content.replace(
                old_text,
                new_text
            )

            target.write_text(
                updated_content,
                encoding="utf-8"
            )

            return True

        except Exception as e:

            print(
                f"[Fehler] Ersetzen: {e}"
            )

            return False

    def create_folder(
        self,
        path
    ):

        try:

            target = self.sandbox.validate(
                path
            )

            target.mkdir(
                parents=True,
                exist_ok=True
            )

            return True

        except Exception as e:

            print(
                f"[Fehler] Ordner erstellen: {e}"
            )

            return False

    def delete_file(
        self,
        path
    ):

        try:

            target = self.sandbox.validate(
                path
            )

            if target.exists():

                target.unlink()

            return True

        except Exception as e:

            print(
                f"[Fehler] Löschen: {e}"
            )

            return False

    def directory_tree(
        self,
        path
    ):

        try:

            root = self.sandbox.validate(
                path
            )

            if not root.exists():

                return (
                    "Pfad existiert nicht."
                )

            lines = [
                str(root)
            ]

            def walk(
                current_path,
                prefix=""
            ):

                entries = sorted(
                    current_path.iterdir(),
                    key=lambda p: (
                        not p.is_dir(),
                        p.name.lower()
                    )
                )

                for index, entry in enumerate(
                    entries
                ):

                    is_last = (
                        index ==
                        len(entries) - 1
                    )

                    connector = (
                        "└── "
                        if is_last
                        else "├── "
                    )

                    lines.append(
                        prefix +
                        connector +
                        entry.name
                    )

                    if entry.is_dir():

                        extension = (
                            "    "
                            if is_last
                            else "│   "
                        )

                        walk(
                            entry,
                            prefix +
                            extension
                        )

            walk(root)

            return "\n".join(
                lines
            )

        except Exception as e:

            return (
                f"Fehler: {e}"
            )


if __name__ == "__main__":

    fs = OpenJarvisFileSystem(
        [
            r"F:\Jarvis",
            r"F:\TestDaten"
        ]
    )

    print(
        "\n=== RECURSIVE TREE TEST ===\n"
    )

    print(
        fs.directory_tree(
            r"F:\Jarvis"
        )
    )