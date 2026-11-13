from pathlib import Path


class PathSandbox:

    def __init__(self, allowed_paths):

        self.allowed_dirs = [
            Path(path).resolve()
            for path in allowed_paths
        ]

    def validate(self, path):

        if not path:
            raise PermissionError(
                "Leerer Pfad."
            )

        target = Path(path)

        if not target.is_absolute():
            raise PermissionError(
                "Nur absolute Pfade erlaubt."
            )

        target = target.resolve()

        for allowed_dir in self.allowed_dirs:

            try:

                target.relative_to(
                    allowed_dir
                )

                return target

            except ValueError:
                pass

        raise PermissionError(
            f"Pfad nicht erlaubt: {target}"
        )

    def is_allowed(self, path):

        try:

            self.validate(path)

            return True

        except Exception:

            return False


if __name__ == "__main__":

    sandbox = PathSandbox(
        [
            r"F:\Jarvis",
            r"F:\TestDaten"
        ]
    )

    print(
        "\n=== SANDBOX TEST ===\n"
    )

    print(
        sandbox.validate(
            r"F:\Jarvis\openjarvis_core.py"
        )
    )

    print(
        sandbox.validate(
            r"F:\TestDaten\test.txt"
        )
    )

    print(
        "\nErlaubt:",
        sandbox.is_allowed(
            r"F:\Jarvis\tool_runner.py"
        )
    )

    try:

        sandbox.validate(
            r"C:\Windows\System32"
        )

    except Exception as e:

        print(
            "\nBlockiert:"
        )

        print(e)