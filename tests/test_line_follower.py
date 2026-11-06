"""Tests für Liniensensor und Linienfolger-Regler."""

import sys
import unittest
from math import hypot, pi
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from robosim.adapters.line_follower_controller import LineFollowerController
from robosim.application.simulation import Simulation
from robosim.domain.line_track import LineTrack
from robosim.domain.robot import Robot


class LineTrackTests(unittest.TestCase):
    def test_sensor_reports_positive_when_line_is_on_robot_right(self) -> None:
        track = LineTrack(((-2.0, -0.1), (2.0, -0.1)))

        error = track.sensor_error(Robot())

        self.assertGreater(error, 0.0)

    def test_sensor_reports_negative_when_line_is_on_robot_left(self) -> None:
        track = LineTrack(((-2.0, 0.1), (2.0, 0.1)))

        error = track.sensor_error(Robot())

        self.assertLess(error, 0.0)

    def test_sensor_array_has_five_readings(self) -> None:
        track = LineTrack.circular_course()

        self.assertEqual(len(track.sensor_readings(Robot(y=-3.0))), 5)

    def test_sensor_reports_when_line_is_lost(self) -> None:
        track = LineTrack(((-2.0, 2.0), (2.0, 2.0)))

        self.assertIsNone(track.sensor_error(Robot()))

    def test_track_requires_at_least_two_points(self) -> None:
        with self.assertRaises(ValueError):
            LineTrack(((0.0, 0.0),))

    def test_track_rejects_repeated_consecutive_points(self) -> None:
        with self.assertRaises(ValueError):
            LineTrack(((0.0, 0.0), (0.0, 0.0)))

    def test_circular_course_is_closed_and_starts_at_bottom(self) -> None:
        track = LineTrack.circular_course(radius=3.0)

        self.assertTrue(track.closed)
        self.assertEqual(len(track.points), 180)
        self.assertAlmostEqual(track.points[0][0], 0.0)
        self.assertAlmostEqual(track.points[0][1], -3.0)

class LineFollowerTests(unittest.TestCase):
    def test_controller_turns_towards_the_line(self) -> None:
        controller = LineFollowerController(
            base_speed=0.5,
            correction_gain=1.0,
            max_wheel_speed=1.5,
        )

        controller.set_line_error(0.2)
        left_for_line_on_right, right_for_line_on_right = controller.get_wheel_speeds()
        controller.set_line_error(-0.2)
        left_for_line_on_left, right_for_line_on_left = controller.get_wheel_speeds()

        self.assertGreater(left_for_line_on_right, right_for_line_on_right)
        self.assertGreater(right_for_line_on_left, left_for_line_on_left)

    def test_controller_stops_when_all_sensors_lose_the_line(self) -> None:
        controller = LineFollowerController()
        controller.set_line_error(None)

        self.assertEqual(controller.get_wheel_speeds(), (0.0, 0.0))

    def test_line_follower_stays_on_the_circular_course(self) -> None:
        track = LineTrack.circular_course(radius=3.0)
        controller = LineFollowerController()
        robot = Robot(x=0.0, y=-3.0, heading=0.0)
        simulation = Simulation(controller, robot=robot)

        for _ in range(600):
            controller.set_line_error(track.sensor_error(robot))
            simulation.step(seconds=0.05)

        final_error = abs(track.sensor_error(robot))
        self.assertLess(final_error, 0.15)
        self.assertLess(abs(hypot(robot.x, robot.y) - 3.0), 0.15)
        self.assertGreater(robot.heading, 2 * pi)


if __name__ == "__main__":
    unittest.main()
