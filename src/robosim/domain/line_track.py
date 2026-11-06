"""Strecke und einfache Liniensensor-Berechnung."""

from dataclasses import dataclass
from math import cos, pi, sin

from robosim.domain.robot import Robot


@dataclass(frozen=True)
class LineTrack:
    """Eine Linie als Folge verbundener Streckenpunkte."""

    points: tuple[tuple[float, float], ...]
    closed: bool = False
    sensor_offsets: tuple[float, ...] = (-0.2, -0.1, 0.0, 0.1, 0.2)
    sensor_distance: float = 0.6
    detection_range: float = 0.14

    def __post_init__(self) -> None:
        if len(self.points) < 2:
            raise ValueError("Eine Strecke braucht mindestens zwei Punkte.")
        if not self.sensor_offsets:
            raise ValueError("Der Liniensensor braucht mindestens einen Sensor.")
        if self.sensor_distance < 0:
            raise ValueError("Der Sensorabstand darf nicht negativ sein.")
        if self.detection_range <= 0:
            raise ValueError("Der Erkennungsbereich muss positiv sein.")
        segments = list(zip(self.points, self.points[1:]))
        if self.closed:
            segments.append((self.points[-1], self.points[0]))
        if any(start == end for start, end in segments):
            raise ValueError("Aufeinanderfolgende Streckenpunkte müssen verschieden sein.")

    @classmethod
    def circular_course(
        cls, radius: float = 3.0, point_count: int = 180
    ) -> "LineTrack":
        """Erzeugt einen geschlossenen Rundkurs gegen den Uhrzeigersinn."""
        if radius <= 0:
            raise ValueError("Der Radius des Rundkurses muss positiv sein.")
        if point_count < 8:
            raise ValueError("Der Rundkurs braucht mindestens acht Streckenpunkte.")

        points = tuple(
            (
                radius * cos(-pi / 2 + 2 * pi * index / point_count),
                radius * sin(-pi / 2 + 2 * pi * index / point_count),
            )
            for index in range(point_count)
        )
        return cls(points, closed=True)

    def _segments(self) -> list[tuple[tuple[float, float], tuple[float, float]]]:
        segments = list(zip(self.points, self.points[1:]))
        if self.closed:
            segments.append((self.points[-1], self.points[0]))
        return segments

    def _closest_projection(
        self, x: float, y: float
    ) -> tuple[int, float, float, float]:
        """Gibt Segmentindex, Segmentanteil und nächsten Punkt zurück."""
        closest_x, closest_y = self.points[0]
        minimum_distance_squared = float("inf")
        closest_index = 0
        closest_projection = 0.0

        for index, (start, end) in enumerate(self._segments()):
            start_x, start_y = start
            end_x, end_y = end
            segment_x = end_x - start_x
            segment_y = end_y - start_y
            segment_length_squared = segment_x**2 + segment_y**2
            projection = (
                (x - start_x) * segment_x + (y - start_y) * segment_y
            ) / segment_length_squared
            projection = min(1.0, max(0.0, projection))
            candidate_x = start_x + projection * segment_x
            candidate_y = start_y + projection * segment_y
            distance_squared = (x - candidate_x) ** 2 + (y - candidate_y) ** 2

            if distance_squared < minimum_distance_squared:
                minimum_distance_squared = distance_squared
                closest_x, closest_y = candidate_x, candidate_y
                closest_index = index
                closest_projection = projection

        return closest_index, closest_projection, closest_x, closest_y

    def closest_point(self, x: float, y: float) -> tuple[float, float]:
        """Findet den nächstgelegenen Punkt auf der Strecke."""
        _, _, closest_x, closest_y = self._closest_projection(x, y)
        return closest_x, closest_y

    def sensor_readings(self, robot: Robot) -> tuple[float, ...]:
        """Liefert die Erkennungsstärke jedes virtuellen Liniensensors (0 bis 1)."""
        forward_x = cos(robot.heading)
        forward_y = sin(robot.heading)
        right_x = sin(robot.heading)
        right_y = -cos(robot.heading)

        readings = []
        for offset in self.sensor_offsets:
            sensor_x = robot.x + self.sensor_distance * forward_x + offset * right_x
            sensor_y = robot.y + self.sensor_distance * forward_y + offset * right_y
            line_x, line_y = self.closest_point(sensor_x, sensor_y)
            distance = ((line_x - sensor_x) ** 2 + (line_y - sensor_y) ** 2) ** 0.5
            reading = max(0.0, 1.0 - distance / self.detection_range)
            readings.append(reading)

        return tuple(readings)

    def sensor_error(self, robot: Robot) -> float | None:
        """Schätzt die Linienlage aus der Sensorreihe.

        Der Fehler ist positiv, wenn die Linie rechts vom Roboter liegt.
        """
        readings = self.sensor_readings(robot)
        total_signal = sum(readings)
        if total_signal == 0:
            return None
        weighted_offset = sum(
            offset * reading
            for offset, reading in zip(self.sensor_offsets, readings)
        )
        return weighted_offset / total_signal
