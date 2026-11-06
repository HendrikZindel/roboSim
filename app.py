
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from nicegui import ui

from robosim.adapters.nicegui_app import create_app


if __name__ == "__main__":
    ui.run(
        root=create_app,
        title="RoboSim | 5-Sensor-Linienfolger",
        host="127.0.0.1",
        port=8083,
        reload=False,
    )