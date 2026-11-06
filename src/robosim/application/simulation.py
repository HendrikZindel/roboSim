"""Anwendungsfall zum Ausführen eines Simulationsschritts."""

from robosim.application.robot_controller import RobotController
from robosim.domain.robot import Robot


class Simulation:
    """Verbindet eine Steuerung mit dem Roboter."""

    def __init__(self, controller: RobotController, robot: Robot | None = None) -> None:
        self.controller = controller
        self.robot = robot if robot is not None else Robot()

    def step(self, seconds: float) -> None:
        """Liest die Radgeschwindigkeiten und bewegt den Roboter."""
        left_speed, right_speed = self.controller.get_wheel_speeds()
        self.robot.move(left_speed, right_speed, seconds)
