import json
from pathlib import Path


class MemoryStore:

    def __init__(
        self,
        memory_file=r"F:\Jarvis\gedaechtnis.json"
    ):

        self.memory_file = Path(
            memory_file
        )

        if not self.memory_file.exists():

            self._save(
                {
                    "freundin": "",
                    "interessen": [],
                    "erinnerungen": []
                }
            )

    def _load(self):

        try:

            return json.loads(
                self.memory_file.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            return {
                "freundin": "",
                "interessen": [],
                "erinnerungen": []
            }

    def _save(
        self,
        data
    ):

        self.memory_file.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

    def remember(
        self,
        key,
        value
    ):

        data = self._load()

        data[key] = value

        self._save(data)

        return True

    def recall(
        self,
        key
    ):

        data = self._load()

        return data.get(key)

    def forget(
        self,
        key
    ):

        data = self._load()

        if key in data:

            del data[key]

            self._save(data)

            return True

        return False

    def remember_interest(
        self,
        interest
    ):

        data = self._load()

        if "interessen" not in data:

            data["interessen"] = []

        if interest not in data["interessen"]:

            data["interessen"].append(
                interest
            )

            self._save(data)

        return True

    def add_memory(
        self,
        text
    ):

        data = self._load()

        if "erinnerungen" not in data:

            data["erinnerungen"] = []

        data["erinnerungen"].append(
            text
        )

        self._save(data)

        return True

    def all(self):

        return self._load()