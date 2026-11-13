from openjarvis_core import OpenJarvisFileSystem


class ToolRunner:

    def __init__(self):

        self.fs = OpenJarvisFileSystem(
            [
                r"F:\Jarvis",
                r"F:\TestDaten"
            ]
        )

        self.tools = {

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

        tool = self.tools[tool_name]

        return tool(**kwargs)


if __name__ == "__main__":

    runner = ToolRunner()

    print(
        "\n=== TOOL RUNNER TEST ===\n"
    )

    print(
        "1. Directory Tree\n"
    )

    print(
        runner.run(
            "directory_tree",
            path=r"F:\Jarvis"
        )
    )

    print(
        "\n2. Datei schreiben\n"
    )

    print(
        runner.run(
            "write_file",
            path=r"F:\TestDaten\tooltest.txt",
            content="Hallo ToolRunner"
        )
    )

    print(
        "\n3. Datei lesen\n"
    )

    print(
        runner.run(
            "read_file",
            path=r"F:\TestDaten\tooltest.txt"
        )
    )

    print(
        "\n4. Text ersetzen\n"
    )

    print(
        runner.run(
            "replace_in_file",
            path=r"F:\TestDaten\tooltest.txt",
            old_text="ToolRunner",
            new_text="OpenJarvis"
        )
    )

    print(
        "\n5. Datei erneut lesen\n"
    )

    print(
        runner.run(
            "read_file",
            path=r"F:\TestDaten\tooltest.txt"
        )
    )

    print(
        "\n=== TEST BEENDET ==="
    )