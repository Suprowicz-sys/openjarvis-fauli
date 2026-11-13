import json
from pathlib import Path
from datetime import datetime


class ProjectNotes:

    def __init__(
        self,
        notes_file=r"F:\Jarvis\projektnotizen.json"
    ):

        self.notes_file = Path(
            notes_file
        )

        if not self.notes_file.exists():

            self._save(
                {}
            )

    def _load(self):

        try:

            return json.loads(
                self.notes_file.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            return {}

    def _save(
        self,
        data
    ):

        self.notes_file.write_text(

            json.dumps(
                data,
                indent=4,
                ensure_ascii=False
            ),

            encoding="utf-8"
        )

    def add_note(
        self,
        project_name,
        text
    ):

        data = self._load()

        if project_name not in data:

            data[
                project_name
            ] = []

        data[
            project_name
        ].append(

            {
                "timestamp":

                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                "text":
                    text
            }
        )

        self._save(
            data
        )

        return True

    def get_notes(
        self,
        project_name
    ):

        data = self._load()

        return data.get(
            project_name,
            []
        )

    def list_projects(self):

        data = self._load()

        return list(
            data.keys()
        )


if __name__ == "__main__":

    notes = ProjectNotes()

    print(
        "\n=== PROJECT NOTES TEST ===\n"
    )

    print(

        notes.add_note(
            "OpenJarvis",
            "Directory Tree rekursiv fertiggestellt."
        )
    )

    print(

        notes.add_note(
            "OpenJarvis",
            "Projektstatus implementiert."
        )
    )

    print(
        "\nNOTIZEN:\n"
    )

    print(

        notes.get_notes(
            "OpenJarvis"
        )
    )

    print(
        "\n=== TEST BEENDET ==="
    )