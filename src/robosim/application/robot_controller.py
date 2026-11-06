"""Port für austauschbare Steuerungen."""

from typing import Protocol


class RobotController(Protocol):
    """Liefert die Sollgeschwindigkeit der beiden Räder."""

    def get_wheel_speeds(self) -> tuple[float, float]:
        """Gibt (linke Geschwindigkeit, rechte Geschwindigkeit) zurück."""
