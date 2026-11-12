import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Settings:
    # Basisverzeichnisse
    FAULI_HOME: Path = field(
        default_factory=lambda: Path(
            os.getenv("FAULI_HOME", str(Path.home() / ".fauli"))
        )
    )

    MEMORY_DB: Path = field(
        default_factory=lambda: Path(
            os.getenv("FAULI_DB", "gedaechtnis.db")
        )
    )

    LOG_FILE: Path = field(
        default_factory=lambda: Path(
            os.getenv("FAULI_LOG", "fauli.log")
        )
    )

    # Whisper
    WHISPER_MODEL: str = "small"
    WHISPER_DEVICE: str = "cpu"
    SAMPLE_RATE: int = 16000
    CHANNELS: int = 1
    SILENCE_THRESHOLD: float = 0.03

    # Colibri / OpenAI-kompatibler Endpoint
    COLIBRI_URL: str = "http://127.0.0.1:8000"
    COLIBRI_TIMEOUT: float = 60.0
    COLIBRI_MODEL: str = "Qwen3.6-35B-A3B"

    # Sandbox
    SANDBOX_WHITELIST: list[str] = field(
        default_factory=lambda: [
            str(Path.home()),
            str(Path.home() / "Desktop"),
            str(Path.home() / "Documents"),
            str(Path.home() / "Downloads"),
            r"C:\Windows",
            r"C:\Windows\System32",
        ]
    )

    def __post_init__(self) -> None:
        self.FAULI_HOME.mkdir(parents=True, exist_ok=True)

        self.MEMORY_DB = (
            self.MEMORY_DB
            if self.MEMORY_DB.is_absolute()
            else self.FAULI_HOME / self.MEMORY_DB.name
        )

        self.LOG_FILE = (
            self.LOG_FILE
            if self.LOG_FILE.is_absolute()
            else self.FAULI_HOME / self.LOG_FILE.name
        )