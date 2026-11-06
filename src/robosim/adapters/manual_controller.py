"""Einfache manuelle Steuerung, zum Beispiel für Tastatureingaben."""


class ManualController:
    """Speichert die vom Nutzer vorgegebenen Radgeschwindigkeiten."""

    def __init__(self) -> None:
        self.left_speed = 0.0
        self.right_speed = 0.0

    def set_wheel_speeds(self, left_speed: float, right_speed: float) -> None:
        """Setzt die Sollgeschwindigkeit für beide Räder."""
        self.left_speed = left_speed
        self.right_speed = right_speed

    def get_wheel_speeds(self) -> tuple[float, float]:
        """Liefert die aktuellen Sollgeschwindigkeiten."""
        return self.left_speed, self.right_speed
