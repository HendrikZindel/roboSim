"""Ein einfacher proportionaler Linienfolger-Regler."""


class LineFollowerController:
    """Lenkt mit der gemessenen seitlichen Abweichung des Liniensensors."""

    def __init__(
        self,
        base_speed: float = 0.7,
        correction_gain: float = 1.5,
        max_wheel_speed: float = 1.5,
    ) -> None:
        if base_speed <= 0:
            raise ValueError("Die Grundgeschwindigkeit muss positiv sein.")
        if correction_gain < 0:
            raise ValueError("Die Reglerverstärkung darf nicht negativ sein.")
        if max_wheel_speed <= 0:
            raise ValueError("Die maximale Radgeschwindigkeit muss positiv sein.")

        self.base_speed = base_speed
        self.correction_gain = correction_gain
        self.max_wheel_speed = max_wheel_speed
        self.line_error: float | None = 0.0

    def set_line_error(self, line_error: float | None) -> None:
        """Setzt die Sensorabweichung; None bedeutet, dass kein Sensor die Linie sieht."""
        self.line_error = line_error

    def get_wheel_speeds(self) -> tuple[float, float]:
        """Lenkt durch die gemessene Linienabweichung zurück zur Ziellinie."""
        if self.line_error is None:
            return 0.0, 0.0
        correction = self.base_speed * self.correction_gain * self.line_error
        left_speed = self.base_speed + correction
        right_speed = self.base_speed - correction
        return (
            min(self.max_wheel_speed, max(0.0, left_speed)),
            min(self.max_wheel_speed, max(0.0, right_speed)),
        )
