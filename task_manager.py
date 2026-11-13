import json
from pathlib import Path


class TaskManager:

    def __init__(
        self,
        task_file=r"F:\Jarvis\aufgaben.json"
    ):

        self.task_file = Path(
            task_file
        )

        if not self.task_file.exists():

            self._save([])

    def _load(self):

        try:

            return json.loads(
                self.task_file.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            return []

    def _save(
        self,
        tasks
    ):

        self.task_file.write_text(
            json.dumps(
                tasks,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

    def add_task(
        self,
        title
    ):

        tasks = self._load()

        next_id = 1

        if tasks:

            next_id = (
                max(
                    task["id"]
                    for task in tasks
                ) + 1
            )

        task = {

            "id": next_id,

            "status": "offen",

            "title": title
        }

        tasks.append(
            task
        )

        self._save(
            tasks
        )

        return task

    def list_tasks(self):

        return self._load()

    def complete_task(
        self,
        task_id
    ):

        tasks = self._load()

        for task in tasks:

            if task["id"] == task_id:

                task["status"] = (
                    "erledigt"
                )

                self._save(
                    tasks
                )

                return True

        return False

    def delete_task(
        self,
        task_id
    ):

        tasks = self._load()

        original_count = (
            len(tasks)
        )

        tasks = [

            task
            for task in tasks

            if task["id"] != task_id
        ]

        self._save(
            tasks
        )

        return (
            len(tasks)
            != original_count
        )

    def next_task(self):

        tasks = self._load()

        for task in tasks:

            if (
                task["status"]
                == "offen"
            ):

                return task

        return None

    def clear_completed(self):

        tasks = self._load()

        tasks = [

            task
            for task in tasks

            if task["status"]
            != "erledigt"
        ]

        self._save(
            tasks
        )

        return True


if __name__ == "__main__":

    tm = TaskManager()

    print(
        "\n=== TASK MANAGER TEST ===\n"
    )

    print(
        "1. Aufgabe anlegen"
    )

    print(
        tm.add_task(
            "OpenJarvis GUI bauen"
        )
    )

    print(
        "\n2. Aufgabe anlegen"
    )

    print(
        tm.add_task(
            "Memory V3 entwickeln"
        )
    )

    print(
        "\n3. Aufgaben anzeigen"
    )

    print(
        tm.list_tasks()
    )

    print(
        "\n4. Nächste Aufgabe"
    )

    print(
        tm.next_task()
    )

    print(
        "\n5. Aufgabe erledigen"
    )

    print(
        tm.complete_task(
            1
        )
    )

    print(
        "\n6. Aufgaben anzeigen"
    )

    print(
        tm.list_tasks()
    )

    print(
        "\n=== TEST BEENDET ==="
    )