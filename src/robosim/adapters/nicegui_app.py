"""NiceGUI-Oberfläche als Eingabe- und Visualisierungsadapter."""

from math import cos, degrees, sin

from nicegui import events, ui

from robosim.adapters.line_follower_controller import LineFollowerController
from robosim.adapters.manual_controller import ManualController
from robosim.application.simulation import Simulation
from robosim.domain.line_track import LineTrack
from robosim.domain.robot import Robot


def create_app() -> None:
    """Erstellt die manuelle Simulation und den automatischen Linienfolger."""
    track = LineTrack.circular_course(radius=3.0)
    start_position = (0.0, -3.0)
    manual_controller = ManualController()
    line_follower = LineFollowerController()
    controller: ManualController | LineFollowerController = manual_controller
    simulation = Simulation(
        controller,
        robot=Robot(x=start_position[0], y=start_position[1]),
    )
    path: list[list[float]] = [[start_position[0], start_position[1]]]
    pressed_keys: set[str] = set()
    mode = "manual"
    manual_direction = 0.0
    manual_steering = 0.0

    ui.query("body").classes("bg-slate-100")
    with ui.column().classes("w-full max-w-6xl mx-auto p-4 md:p-8 gap-6"):
        with ui.card().classes(
            "w-full bg-gradient-to-r from-blue-700 to-indigo-700 text-white "
            "rounded-2xl shadow-lg"
        ):
            with ui.row().classes("w-full items-center justify-between"):
                with ui.column().classes("gap-1"):
                    ui.label("RoboSim").classes("text-3xl font-bold")
                    ui.label(
                        "5-Sensor-Linienfolger · aktuelle Version"
                    ).classes("text-blue-100")
                ui.icon("precision_manufacturing", size="xl").classes(
                    "text-blue-100"
                )

            with ui.row().classes("w-full items-center gap-4 mt-4"):
                mode_select = ui.select(
                    {
                        "manual": "Manuell",
                        "line_follower": "Automatisch geregelt",
                    },
                    value="manual",
                    label="Steuerungsmodus",
                ).classes("w-full max-w-sm").props(
                    "dark outlined options-dense"
                )
                mode_description = ui.label(
                    "Du steuerst den Roboter selbst über Tastatur oder Buttons."
                ).classes("text-blue-100")

        with ui.row().classes("w-full gap-4"):
            with ui.card().classes("flex-1 rounded-xl shadow-sm"):
                ui.label("Position").classes("text-sm text-slate-500")
                position_label = ui.label("x 0.00 m · y -3.00 m").classes(
                    "text-xl font-semibold text-slate-800"
                )
            with ui.card().classes("flex-1 rounded-xl shadow-sm"):
                ui.label("Ausrichtung").classes("text-sm text-slate-500")
                heading_label = ui.label("0.0°").classes(
                    "text-xl font-semibold text-slate-800"
                )
            with ui.card().classes("flex-1 rounded-xl shadow-sm"):
                ui.label("Radgeschwindigkeit").classes("text-sm text-slate-500")
                speed_label = ui.label("L 0.00 · R 0.00 m/s").classes(
                    "text-xl font-semibold text-slate-800"
                )

        with ui.row().classes("w-full items-stretch gap-6"):
            with ui.card().classes("flex-[2] min-w-0 rounded-2xl shadow-sm p-3"):
                with ui.row().classes("w-full items-center justify-between px-3 pt-2"):
                    ui.label("Rundkurs").classes(
                        "text-xl font-semibold text-slate-800"
                    )
                    ui.label("Geschlossene Strecke").classes(
                        "text-sm text-slate-500"
                    )

                chart = ui.echart(
                    {
                        "animation": False,
                        "tooltip": {"trigger": "item"},
                        "grid": {"left": 45, "right": 25, "top": 30, "bottom": 40},
                        "xAxis": {
                            "type": "value",
                            "name": "x (m)",
                            "min": -4,
                            "max": 4,
                            "splitLine": {"lineStyle": {"color": "#e2e8f0"}},
                            "axisLine": {"lineStyle": {"color": "#94a3b8"}},
                        },
                        "yAxis": {
                            "type": "value",
                            "name": "y (m)",
                            "min": -4,
                            "max": 4,
                            "splitLine": {"lineStyle": {"color": "#e2e8f0"}},
                            "axisLine": {"lineStyle": {"color": "#94a3b8"}},
                        },
                        "series": [
                            {
                                "name": "Ziellinie",
                                "type": "line",
                                "data": [list(point) for point in track.points],
                                "showSymbol": False,
                                "lineStyle": {
                                    "color": "#334155",
                                    "width": 5,
                                    "cap": "round",
                                },
                                "z": 1,
                            },
                            {
                                "name": "Fahrspur",
                                "type": "line",
                                "data": path,
                                "showSymbol": False,
                                "lineStyle": {"color": "#38bdf8", "width": 3},
                                "z": 2,
                            },
                            {
                                "name": "Roboter",
                                "type": "scatter",
                                "data": [[start_position[0], start_position[1]]],
                                "symbol": "circle",
                                "symbolSize": 30,
                                "itemStyle": {
                                    "color": "#2563eb",
                                    "borderColor": "#ffffff",
                                    "borderWidth": 4,
                                    "shadowBlur": 12,
                                    "shadowColor": "#64748b",
                                },
                                "z": 4,
                            },
                            {
                                "name": "Fahrtrichtung",
                                "type": "line",
                                "data": [
                                    [start_position[0], start_position[1]],
                                    [start_position[0] + 0.55, start_position[1]],
                                ],
                                "showSymbol": False,
                                "lineStyle": {"color": "#1d4ed8", "width": 5},
                                "z": 5,
                            },
                            {
                                "name": "Sensor",
                                "type": "scatter",
                                "data": [[start_position[0] + 0.6, start_position[1]]],
                                "symbol": "circle",
                                "symbolSize": 11,
                                "itemStyle": {
                                    "color": "#f97316",
                                    "borderColor": "#ffffff",
                                    "borderWidth": 2,
                                },
                                "z": 6,
                            },
                        ],
                    }
                ).classes("w-full h-[560px]")

                with ui.row().classes("items-center gap-5 px-3 pb-2"):
                    with ui.row().classes("items-center gap-2"):
                        ui.element("span").classes(
                            "inline-block w-3 h-3 rounded-full bg-slate-700"
                        )
                        ui.label("Ziellinie").classes("text-sm text-slate-600")
                    with ui.row().classes("items-center gap-2"):
                        ui.element("span").classes(
                            "inline-block w-3 h-3 rounded-full bg-sky-400"
                        )
                        ui.label("Fahrspur").classes("text-sm text-slate-600")
                    with ui.row().classes("items-center gap-2"):
                        ui.element("span").classes(
                            "inline-block w-3 h-3 rounded-full bg-orange-500"
                        )
                        ui.label("Reflexsensoren").classes("text-sm text-slate-600")

            with ui.card().classes(
                "flex-1 min-w-[280px] rounded-2xl shadow-sm p-5 gap-4"
            ):
                ui.label("Steuerung").classes("text-xl font-semibold text-slate-800")
                status_label = ui.label("Bereit").classes(
                    "text-sm font-medium text-slate-500"
                )

                ui.label("Geschwindigkeit").classes(
                    "text-sm font-medium text-slate-600"
                )
                speed_slider = ui.slider(
                    min=0.1, max=1.2, value=0.5, step=0.1
                ).props("label color=blue")

                with ui.column().classes("w-full gap-2") as manual_controls:
                    ui.label("Manuell fahren").classes(
                        "text-sm font-medium text-slate-600"
                    )
                    with ui.row().classes("w-full justify-center"):
                        forward_button = ui.button(
                            "Vorwärts", icon="keyboard_arrow_up"
                        ).props("color=blue unelevated")
                    with ui.row().classes("w-full justify-center"):
                        left_button = ui.button(
                            "Links", icon="keyboard_arrow_left"
                        ).props("color=blue unelevated")
                        stop_button = ui.button("Stopp", icon="stop").props(
                            "color=red outline"
                        )
                        right_button = ui.button(
                            "Rechts", icon="keyboard_arrow_right"
                        ).props("color=blue unelevated")
                    with ui.row().classes("w-full justify-center"):
                        reverse_button = ui.button(
                            "Rückwärts", icon="keyboard_arrow_down"
                        ).props("color=blue unelevated")
                    ui.label(
                        "Tastatur: W/A/S/D oder Pfeiltasten"
                    ).classes("text-xs text-slate-400")

                with ui.row().classes("w-full gap-2 mt-2"):
                    start_button = ui.button(
                        "Start", icon="play_arrow"
                    ).props("color=positive unelevated").classes("flex-1")
                    pause_button = ui.button(
                        "Pause", icon="pause"
                    ).props("color=blue outline").classes("flex-1")
                reset_button = ui.button(
                    "Auf Startposition zurücksetzen", icon="restart_alt"
                ).props("color=grey outline").classes("w-full")

                ui.separator()
                sensor_label = ui.label()
                ui.label(
                    "Im Automatikmodus lenkt der Regler anhand der fünf virtuellen "
                    "Reflexsensoren."
                ).classes("text-xs text-slate-400")

    def update_display() -> None:
        robot = simulation.robot
        chart.options["series"][1]["data"] = path
        chart.options["series"][2]["data"] = [[robot.x, robot.y]]
        chart.options["series"][3]["data"] = [
            [robot.x, robot.y],
            [
                robot.x + 0.55 * cos(robot.heading),
                robot.y + 0.55 * sin(robot.heading),
            ],
        ]
        sensor_readings = track.sensor_readings(robot)
        chart.options["series"][4]["data"] = [
            {
                "value": [
                    robot.x
                    + track.sensor_distance * cos(robot.heading)
                    + offset * sin(robot.heading),
                    robot.y
                    + track.sensor_distance * sin(robot.heading)
                    - offset * cos(robot.heading),
                ],
                "itemStyle": {
                    "color": "#22c55e" if reading > 0 else "#cbd5e1",
                    "borderColor": "#ffffff",
                    "borderWidth": 2,
                },
            }
            for offset, reading in zip(track.sensor_offsets, sensor_readings)
        ]
        chart.update()

        position_label.set_text(f"x {robot.x:.2f} m · y {robot.y:.2f} m")
        heading_label.set_text(f"{degrees(robot.heading) % 360:.1f}°")
        left_speed, right_speed = controller.get_wheel_speeds()
        speed_label.set_text(
            f"L {left_speed:.2f} · R {right_speed:.2f} m/s"
        )
        sensor_error = track.sensor_error(robot)
        line_status = (
            f"Linienabweichung {sensor_error:+.3f} m"
            if sensor_error is not None
            else "Linie nicht erkannt"
        )
        sensor_label.set_text(
            "Sensorreihe L→R: "
            + " ".join("●" if reading > 0 else "○" for reading in sensor_readings)
            + f"   ·   {line_status}"
        )

    def set_manual_control(direction: float, steering: float) -> None:
        nonlocal manual_direction, manual_steering
        if mode != "manual":
            return
        manual_direction = direction
        manual_steering = steering
        speed = float(speed_slider.value)
        manual_controller.set_wheel_speeds(
            speed * (direction - steering),
            speed * (direction + steering),
        )
        update_display()

    def update_keyboard_control() -> None:
        if mode != "manual":
            return
        forward = "w" in pressed_keys or "ArrowUp" in pressed_keys
        backward = "s" in pressed_keys or "ArrowDown" in pressed_keys
        turn_left = "a" in pressed_keys or "ArrowLeft" in pressed_keys
        turn_right = "d" in pressed_keys or "ArrowRight" in pressed_keys

        direction = float(forward) - float(backward)
        steering = float(turn_left) - float(turn_right)
        set_manual_control(direction, steering)

    def handle_key(event: events.KeyEventArguments) -> None:
        key_name = event.key.name
        key = key_name.lower() if len(key_name) == 1 else key_name
        supported_keys = {
            "w",
            "a",
            "s",
            "d",
            "ArrowUp",
            "ArrowDown",
            "ArrowLeft",
            "ArrowRight",
        }
        if key not in supported_keys:
            return
        if event.action.keydown:
            pressed_keys.add(key)
        elif event.action.keyup:
            pressed_keys.discard(key)
        update_keyboard_control()

    def tick() -> None:
        if mode == "line_follower":
            line_follower.set_line_error(track.sensor_error(simulation.robot))
        simulation.step(seconds=0.1)
        robot = simulation.robot
        path.append([robot.x, robot.y])
        if len(path) > 3000:
            del path[1]
        update_display()

    timer = ui.timer(0.1, tick, active=False)

    def start() -> None:
        timer.activate()
        status_label.set_text("Simulation läuft")
        status_label.classes(replace="text-sm font-medium text-emerald-600")

    def pause() -> None:
        timer.deactivate()
        status_label.set_text("Pausiert")
        status_label.classes(replace="text-sm font-medium text-amber-600")

    def reset() -> None:
        nonlocal simulation, controller, manual_direction, manual_steering
        timer.deactivate()
        manual_controller.set_wheel_speeds(0.0, 0.0)
        line_follower.base_speed = float(speed_slider.value)
        controller = manual_controller if mode == "manual" else line_follower
        simulation = Simulation(
            controller,
            robot=Robot(x=start_position[0], y=start_position[1]),
        )
        path.clear()
        path.append([start_position[0], start_position[1]])
        pressed_keys.clear()
        manual_direction = 0.0
        manual_steering = 0.0
        status_label.set_text("Bereit")
        status_label.classes(replace="text-sm font-medium text-slate-500")
        update_display()

    def switch_mode(event: events.ValueChangeEventArguments) -> None:
        nonlocal mode, controller, simulation
        mode = str(event.value)
        manual_controller.set_wheel_speeds(0.0, 0.0)
        pressed_keys.clear()
        controller = manual_controller if mode == "manual" else line_follower
        line_follower.base_speed = float(speed_slider.value)
        simulation = Simulation(controller, robot=simulation.robot)
        manual_controls.set_visibility(mode == "manual")
        keyboard.active = mode == "manual"
        if mode == "manual":
            mode_description.set_text(
                "Du steuerst den Roboter selbst über Tastatur oder Buttons."
            )
        else:
            mode_description.set_text(
                "Der Regler folgt dem Rundkurs und passt die Radgeschwindigkeiten an."
            )
        update_display()

    def update_speed() -> None:
        if mode == "manual":
            set_manual_control(manual_direction, manual_steering)
        else:
            line_follower.base_speed = float(speed_slider.value)
            update_display()

    forward_button.on_click(lambda: set_manual_control(1.0, 0.0))
    reverse_button.on_click(lambda: set_manual_control(-1.0, 0.0))
    left_button.on_click(lambda: set_manual_control(0.0, 1.0))
    right_button.on_click(lambda: set_manual_control(0.0, -1.0))
    stop_button.on_click(lambda: set_manual_control(0.0, 0.0))
    start_button.on_click(start)
    pause_button.on_click(pause)
    reset_button.on_click(reset)

    keyboard = ui.keyboard(on_key=handle_key, ignore=[])
    mode_select.on_value_change(switch_mode)
    speed_slider.on_value_change(lambda _: update_speed())

    update_display()
