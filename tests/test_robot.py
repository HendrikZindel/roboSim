"""Tests für die Bewegungsberechnung des Roboters."""

import unittest
from math import cos, sin
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from robosim.domain.robot import Robot


class RobotMovementTests(unittest.TestCase):
    def test_equal_wheel_speeds_move_straight_forward(self) -> None:
        robot = Robot()

        robot.move(left_speed=1.0, right_speed=1.0, seconds=2.0)

        self.assertAlmostEqual(robot.x, 2.0)
        self.assertAlmostEqual(robot.y, 0.0)
        self.assertAlmostEqual(robot.heading, 0.0)

    def test_different_wheel_speeds_move_robot_on_a_curve(self) -> None:
        robot = Robot()

        robot.move(left_speed=0.0, right_speed=0.5, seconds=1.0)

        self.assertAlmostEqual(robot.x, 0.25 * sin(1.0))
        self.assertAlmostEqual(robot.y, 0.25 * (1.0 - cos(1.0)))
        self.assertAlmostEqual(robot.heading, 1.0)

    def test_opposite_wheel_speeds_turn_in_place(self) -> None:
        robot = Robot()

        robot.move(left_speed=-0.5, right_speed=0.5, seconds=1.0)

        self.assertAlmostEqual(robot.x, 0.0)
        self.assertAlmostEqual(robot.y, 0.0)
        self.assertAlmostEqual(robot.heading, 2.0)

    def test_wheel_base_must_be_positive(self) -> None:
        for wheel_base in (0.0, -0.5):
            with self.subTest(wheel_base=wheel_base):
                with self.assertRaises(ValueError):
                    Robot(wheel_base=wheel_base)

    def test_simulation_time_must_not_be_negative(self) -> None:
        robot = Robot()

        with self.assertRaises(ValueError):
            robot.move(left_speed=1.0, right_speed=1.0, seconds=-1.0)


if __name__ == "__main__":
    unittest.main()
