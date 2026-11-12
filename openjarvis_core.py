from pathlib import Path


class OpenJarvisFileSystem:

    def __init__(self, allowed_paths=None):

        self.base_path = Path.cwd().resolve()

        if allowed_paths:
            self.allowed_dirs = {
                Path(p).resolve()
                for p in allowed_paths
            }
        else:
            self.allowed_dirs = {
                self.base_path
            }

    def _is_allowed(self, file_path):

        try:
            resolved_path = file_path.resolve()

            for allowed_dir in self.allowed_dirs:

                try:
                    resolved_path.relative_to(allowed_dir)
                    return True

                except ValueError:
                    pass

            return False

        except Exception:
            return False

    def list_files(self, path):

        try:
            target = Path(path).resolve()

            if not self._is_allowed(target):
                raise PermissionError(
                    f"Zugriff verweigert auf {target}"
                )

            if not target.exists():
                return []

            files = []

            for item in target.iterdir():
                files.append(str(item))

            return files

        except Exception as e:

            print(
                f"[WARN] Fehler beim Listen: {e}"
            )

            return []

    def read_file(self, path):

        try:
            target = Path(path).resolve()

            if not self._is_allowed(target):
                raise PermissionError(
                    f"Zugriff verweigert auf {target}"
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

    def write_file(self, path, content):

        try:
            target = Path(path).resolve()

            if not self._is_allowed(target):
                raise PermissionError(
                    f"Schreiben verweigert auf {target}"
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

    def append_file(self, path, content):

        try:
            target = Path(path).resolve()

            if not self._is_allowed(target):
                raise PermissionError(
                    f"Schreiben verweigert auf {target}"
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

    def search_in_file(self, path, query):

        content = self.read_file(path)

        if content is None:
            return []

        matches = []

        for index, line in enumerate(
            content.splitlines(),
            start=1
        ):

            if query.lower() in line.lower():
                matches.append(index)

        return matches


if __name__ == "__main__":

    print(
        "--- OpenJarvis Core Test ---"
    )

    fs = OpenJarvisFileSystem(
        [
            str(Path.cwd()),
            r"F:\TestDaten"
        ]
    )

    output_path = (
        r"F:\TestDaten\test_output.txt"
    )

    print("\n1. list_files('.')")

    files = fs.list_files(".")

    print(files)

    print("\n2. write_file()")

    ok = fs.write_file(
        output_path,
        "Hallo Welt!\n"
        "Dies ist ein Test von OpenJarvis.\n"
        "Ich kann dir helfen, Code zu schreiben.\n"
    )

    print("Erfolg:", ok)

    print("\n3. read_file()")

    print(
        fs.read_file(output_path)
    )

    print(
        "\n4. search_in_file('OpenJarvis')"
    )

    print(
        fs.search_in_file(
            output_path,
            "OpenJarvis"
        )
    )

    print(
        "\n5. append_file()"
    )

    fs.append_file(
        output_path,
        "\nDies ist eine neue Zeile."
    )

    print(
        "\n6. Finaler Check"
    )

    print(
        fs.read_file(output_path)
    )

    print(
        "\n--- Test abgeschlossen ---"
    )