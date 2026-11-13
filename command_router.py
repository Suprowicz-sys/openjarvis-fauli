from tool_runner import ToolRunner


class CommandRouter:

    def __init__(self):

        self.runner = ToolRunner()

    def format_tasks(self, tasks):

        if not tasks:
            return "Keine Aufgaben vorhanden."

        lines = []

        for task in tasks:

            lines.append(
                f"[{task['id']}] "
                f"{task['status'].upper()} "
                f"{task['title']}"
            )

        return "\n".join(lines)

    def handle(self, command):

        command = command.strip()

        if not command:
            return "Leerer Befehl."

        lower = command.lower()

        # ==================================
        # PROJEKTVERWALTUNG V1
        # ==================================

        if lower.startswith("neues projekt"):

            project_name = command.replace(
                "neues projekt",
                "",
                1
            ).strip()

            if not project_name:
                return (
                    "Verwendung:\n"
                    "neues projekt NAME"
                )

            self.runner.run(
                "create_project",
                project_name=project_name
            )

            return (
                f"Projekt erstellt: "
                f"{project_name}"
            )

        if lower == "zeige projekte":

            projects = self.runner.run(
                "list_projects"
            )

            if not projects:
                return (
                    "Keine Projekte vorhanden."
                )

            return "\n".join(projects)

        if lower.startswith("projektaufgabe"):

            try:

                parts = command.split(
                    "|",
                    1
                )

                project_name = (
                    parts[0]
                    .replace(
                        "projektaufgabe",
                        "",
                        1
                    )
                    .strip()
                )

                title = parts[1].strip()

                task = self.runner.run(
                    "add_project_task",
                    project_name=project_name,
                    title=title
                )

                if task is None:

                    return (
                        "Projekt nicht gefunden."
                    )

                return (
                    f"Aufgabe angelegt:\n"
                    f"[{task['id']}] "
                    f"{task['title']}"
                )

            except Exception:

                return (
                    "Verwendung:\n"
                    "projektaufgabe "
                    "PROJEKT | TEXT"
                )

        if lower.startswith("zeige projekt"):

            project_name = command.replace(
                "zeige projekt",
                "",
                1
            ).strip()

            project = self.runner.run(
                "get_project",
                project_name=project_name
            )

            if not project:

                return (
                    "Projekt nicht gefunden."
                )

            lines = [
                f"Projekt: {project_name}",
                ""
            ]

            tasks = project.get(
                "tasks",
                []
            )

            if not tasks:

                lines.append(
                    "Keine Aufgaben."
                )

            else:

                for task in tasks:

                    lines.append(
                        f"[{task['id']}] "
                        f"{task['status'].upper()} "
                        f"{task['title']}"
                    )

            return "\n".join(lines)

        if lower.startswith(
            "nächste projektaufgabe"
        ):

            project_name = command.replace(
                "nächste projektaufgabe",
                "",
                1
            ).strip()

            task = self.runner.run(
                "next_project_task",
                project_name=project_name
            )

            if task is None:

                return (
                    "Keine offene "
                    "Projektaufgabe gefunden."
                )

            return (
                "Nächste Projektaufgabe:\n"
                f"[{task['id']}] "
                f"{task['title']}"
            )

        # ==================================
        # AUFGABENVERWALTUNG
        # ==================================

        if lower.startswith(
            "neue aufgabe"
        ):

            title = command.replace(
                "neue aufgabe",
                "",
                1
            ).strip()

            task = self.runner.run(
                "add_task",
                title=title
            )

            return (
                f"Aufgabe angelegt:\n"
                f"[{task['id']}] "
                f"{task['title']}"
            )

        if lower == "zeige aufgaben":

            return self.format_tasks(
                self.runner.run(
                    "list_tasks"
                )
            )

        if lower.startswith(
            "erledige aufgabe"
        ):

            try:

                task_id = int(
                    command.replace(
                        "erledige aufgabe",
                        "",
                        1
                    ).strip()
                )

                success = self.runner.run(
                    "complete_task",
                    task_id=task_id
                )

                if success:

                    return (
                        f"Aufgabe "
                        f"{task_id} erledigt."
                    )

                return (
                    "Aufgabe nicht gefunden."
                )

            except Exception:

                return (
                    "Verwendung:\n"
                    "erledige aufgabe ID"
                )

        if lower.startswith(
            "lösche aufgabe"
        ):

            try:

                task_id = int(
                    command.replace(
                        "lösche aufgabe",
                        "",
                        1
                    ).strip()
                )

                success = self.runner.run(
                    "delete_task",
                    task_id=task_id
                )

                if success:

                    return (
                        f"Aufgabe "
                        f"{task_id} gelöscht."
                    )

                return (
                    "Aufgabe nicht gefunden."
                )

            except Exception:

                return (
                    "Verwendung:\n"
                    "lösche aufgabe ID"
                )

        if lower == (
            "was ist die nächste aufgabe"
        ):

            task = self.runner.run(
                "next_task"
            )

            if not task:

                return (
                    "Keine offene Aufgabe."
                )

            return (
                f"[{task['id']}] "
                f"{task['title']}"
            )

        # ==================================
        # GEDÄCHTNIS
        # ==================================

        if lower == "zeige gedächtnis":

            return str(
                self.runner.run(
                    "memory_all"
                )
            )

        if lower == "wie heiße ich":

            value = self.runner.run(
                "recall",
                key="name"
            )

            if value:

                return (
                    f"Du heißt "
                    f"{value}."
                )

            return (
                "Kein Name gespeichert."
            )

        # ==================================
        # DATEISYSTEM
        # ==================================

        if lower.startswith(
            "zeige baum"
        ):

            path = command.replace(
                "zeige baum",
                "",
                1
            ).strip()

            return self.runner.run(
                "directory_tree",
                path=path
            )

        return (
            f"Befehl nicht erkannt: "
            f"{command}"
        )


if __name__ == "__main__":

    router = CommandRouter()

    print(
        "\n=== OpenJarvis Router ==="
    )

    print(
        "\nProjektverwaltung:"
    )

    print(
        "neues projekt OpenJarvis"
    )

    print(
        "zeige projekte"
    )

    print(
        "projektaufgabe OpenJarvis | GUI bauen"
    )

    print(
        "zeige projekt OpenJarvis"
    )

    print(
        "nächste projektaufgabe OpenJarvis"
    )

    print(
        "\nAufgabenverwaltung:"
    )

    print(
        "neue aufgabe TEXT"
    )

    print(
        "zeige aufgaben"
    )

    print(
        "erledige aufgabe ID"
    )

    print(
        "lösche aufgabe ID"
    )

    print(
        "was ist die nächste aufgabe"
    )

    print(
        "\nexit = beenden\n"
    )

    while True:

        command = input(
            "Befehl: "
        )

        if command.lower() in (
            "exit",
            "quit",
            "ende"
        ):
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