"""Roboter und seine Bewegungsberechnung."""

from dataclasses import dataclass
from math import cos, sin


@dataclass
class Robot:
    """Ein differentiell angetriebener Roboter."""

    x: float = 0.0
    y: float = 0.0
    heading: float = 0.0
    wheel_base: float = 0.5

    def __post_init__(self) -> None:
        if self.wheel_base <= 0:
            raise ValueError("Der Abstand zwischen den Rädern muss positiv sein.")

    def move(self, left_speed: float, right_speed: float, seconds: float) -> None:
        """Bewegt den Roboter für die angegebene Zeit in Sekunden."""
        if seconds < 0:
            raise ValueError("Die Simulationszeit darf nicht negativ sein.")

        speed = (left_speed + right_speed) / 2
        angular_speed = (right_speed - left_speed) / self.wheel_base

        if angular_speed == 0:
            self.x += speed * cos(self.heading) * seconds
            self.y += speed * sin(self.heading) * seconds
            return

        new_heading = self.heading + angular_speed * seconds
        radius = speed / angular_speed
        self.x += radius * (sin(new_heading) - sin(self.heading))
        self.y -= radius * (cos(new_heading) - cos(self.heading))
        self.heading = new_heading
