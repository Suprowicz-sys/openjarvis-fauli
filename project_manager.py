import json
from pathlib import Path


class ProjectManager:

    def __init__(
        self,
        project_file=r"F:\Jarvis\projekte.json"
    ):

        self.project_file = Path(
            project_file
        )

        if not self.project_file.exists():

            self._save(
                {}
            )

    def _load(self):

        try:

            return json.loads(
                self.project_file.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            return {}

    def _save(
        self,
        projects
    ):

        self.project_file.write_text(
            json.dumps(
                projects,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

    def create_project(
        self,
        project_name
    ):

        projects = self._load()

        if project_name not in projects:

            projects[
                project_name
            ] = {

                "tasks": []
            }

            self._save(
                projects
            )

        return True

    def list_projects(self):

        projects = self._load()

        return list(
            projects.keys()
        )

    def add_project_task(
        self,
        project_name,
        title
    ):

        projects = self._load()

        if project_name not in projects:

            return None

        tasks = projects[
            project_name
        ]["tasks"]

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
            projects
        )

        return task

    def get_project(
        self,
        project_name
    ):

        projects = self._load()

        return projects.get(
            project_name
        )

    def next_project_task(
        self,
        project_name
    ):

        projects = self._load()

        if project_name not in projects:

            return None

        tasks = projects[
            project_name
        ]["tasks"]

        for task in tasks:

            if task[
                "status"
            ] == "offen":

                return task

        return None

    def complete_project_task(
        self,
        project_name,
        task_id
    ):

        projects = self._load()

        if project_name not in projects:

            return False

        for task in projects[
            project_name
        ]["tasks"]:

            if task[
                "id"
            ] == task_id:

                task[
                    "status"
                ] = "erledigt"

                self._save(
                    projects
                )

                return True

        return False

    def delete_project_task(
        self,
        project_name,
        task_id
    ):

        projects = self._load()

        if project_name not in projects:

            return False

        tasks = projects[
            project_name
        ]["tasks"]

        before = len(
            tasks
        )

        projects[
            project_name
        ]["tasks"] = [

            task

            for task in tasks

            if task[
                "id"
            ] != task_id
        ]

        self._save(
            projects
        )

        return (

            len(
                projects[
                    project_name
                ]["tasks"]
            )

            != before
        )

    def project_status(
        self,
        project_name
    ):

        projects = self._load()

        if project_name not in projects:

            return None

        tasks = projects[
            project_name
        ]["tasks"]

        total = len(
            tasks
        )

        completed = len(

            [

                task

                for task in tasks

                if task[
                    "status"
                ] == "erledigt"
            ]
        )

        open_tasks = (
            total -
            completed
        )

        progress = 0

        if total > 0:

            progress = round(

                (
                    completed
                    / total
                ) * 100,

                1
            )

        next_task = None

        for task in tasks:

            if task[
                "status"
            ] == "offen":

                next_task = task

                break

        return {

            "project":
                project_name,

            "total":
                total,

            "completed":
                completed,

            "open":
                open_tasks,

            "progress":
                progress,

            "next_task":
                next_task
        }

    def work_on_project(
        self,
        project_name
    ):

        projects = self._load()

        if project_name not in projects:

            return None

        next_task = self.next_project_task(
            project_name
        )

        if not next_task:

            return {

                "project":
                    project_name,

                "message":
                    "Keine offenen Aufgaben vorhanden."
            }

        return {

            "project":
                project_name,

            "task":
                next_task["title"],

            "steps": [

                "Anforderungen prüfen",

                "Aufgabe in kleine Schritte zerlegen",

                "Implementierung beginnen",

                "Zwischentest durchführen",

                "Aufgabe abschließen"
            ]
        }


if __name__ == "__main__":

    pm = ProjectManager()

    print(
        "\n=== PROJECT STATUS TEST ===\n"
    )

    print(
        pm.create_project(
            "OpenJarvis"
        )
    )

    print(
        pm.add_project_task(
            "OpenJarvis",
            "GUI bauen"
        )
    )

    print(
        pm.add_project_task(
            "OpenJarvis",
            "LLM integrieren"
        )
    )

    print(
        pm.complete_project_task(
            "OpenJarvis",
            1
        )
    )

    print(
        "\nSTATUS:"
    )

    print(
        pm.project_status(
            "OpenJarvis"
        )
    )

    print(
        "\nARBEITE AN PROJEKT:"
    )

    print(
        pm.work_on_project(
            "OpenJarvis"
        )
    )

    print(
        "\n=== TEST BEENDET ==="
    )