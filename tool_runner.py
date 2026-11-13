from openjarvis_core import OpenJarvisFileSystem
from memory_store import MemoryStore
from task_manager import TaskManager
from project_manager import ProjectManager


class ToolRunner:

    def __init__(self):

        self.fs = OpenJarvisFileSystem(
            [
                r"F:\Jarvis",
                r"F:\TestDaten"
            ]
        )

        self.memory = MemoryStore()

        self.tasks = TaskManager()

        self.projects = ProjectManager()

        self.tools = {

            # -------------------
            # Dateisystem
            # -------------------

            "list_files":
                self.fs.list_files,

            "read_file":
                self.fs.read_file,

            "write_file":
                self.fs.write_file,

            "append_file":
                self.fs.append_file,

            "search_in_file":
                self.fs.search_in_file,

            "replace_in_file":
                self.fs.replace_in_file,

            "create_folder":
                self.fs.create_folder,

            "delete_file":
                self.fs.delete_file,

            "directory_tree":
                self.fs.directory_tree,

            # -------------------
            # Gedächtnis
            # -------------------

            "remember":
                self.memory.remember,

            "recall":
                self.memory.recall,

            "forget":
                self.memory.forget,

            "memory_all":
                self.memory.all,

            "remember_interest":
                self.memory.remember_interest,

            "add_memory":
                self.memory.add_memory,

            # -------------------
            # Aufgabenverwaltung
            # -------------------

            "add_task":
                self.tasks.add_task,

            "list_tasks":
                self.tasks.list_tasks,

            "complete_task":
                self.tasks.complete_task,

            "delete_task":
                self.tasks.delete_task,

            "next_task":
                self.tasks.next_task,

            "clear_completed":
                self.tasks.clear_completed,

            # -------------------
            # Projektverwaltung
            # -------------------

            "create_project":
                self.projects.create_project,

            "list_projects":
                self.projects.list_projects,

            "add_project_task":
                self.projects.add_project_task,

            "get_project":
                self.projects.get_project,

            "next_project_task":
                self.projects.next_project_task,

            "complete_project_task":
                self.projects.complete_project_task,

            "delete_project_task":
                self.projects.delete_project_task,
        }

    def run(
        self,
        tool_name,
        **kwargs
    ):

        if tool_name not in self.tools:

            raise ValueError(
                f"Unbekanntes Tool: {tool_name}"
            )

        tool = self.tools[
            tool_name
        ]

        return tool(
            **kwargs
        )


if __name__ == "__main__":

    runner = ToolRunner()

    print(
        "\n=== PROJECT TOOL TEST V2 ===\n"
    )

    print(
        "1. Projekt anlegen"
    )

    print(
        runner.run(
            "create_project",
            project_name="OpenJarvis"
        )
    )

    print(
        "\n2. Projektaufgaben"
    )

    print(
        runner.run(
            "add_project_task",
            project_name="OpenJarvis",
            title="GUI bauen"
        )
    )

    print(
        runner.run(
            "add_project_task",
            project_name="OpenJarvis",
            title="Lokales LLM"
        )
    )

    print(
        "\n3. Projekt anzeigen"
    )

    print(
        runner.run(
            "get_project",
            project_name="OpenJarvis"
        )
    )

    print(
        "\n4. Projektaufgabe erledigen"
    )

    print(
        runner.run(
            "complete_project_task",
            project_name="OpenJarvis",
            task_id=1
        )
    )

    print(
        "\n5. Projekt anzeigen"
    )

    print(
        runner.run(
            "get_project",
            project_name="OpenJarvis"
        )
    )

    print(
        "\n6. Projektaufgabe löschen"
    )

    print(
        runner.run(
            "delete_project_task",
            project_name="OpenJarvis",
            task_id=2
        )
    )

    print(
        "\n7. Projekt anzeigen"
    )

    print(
        runner.run(
            "get_project",
            project_name="OpenJarvis"
        )
    )

    print(
        "\n=== TEST BEENDET ==="
    )