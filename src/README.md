# Einfacher Architekturentwurf

Die Simulation ist nach dem Prinzip **Ports und Adapter** aufgebaut. Die Fachlogik kennt weder NiceGUI noch Tastatur oder konkrete Regler. Adapter können ausgetauscht werden, ohne die Bewegungsberechnung im Roboter zu ändern.

```text
NiceGUI / Tastatur
        |
        v
Anwendungsfall: Simulation
        |
        +---- Port: RobotController
        |          ^
        |          |
        |     Manueller Regler
        |     Linienfolger
        v
Domäne: Robot
```

## Ordner

- `robosim/domain/robot.py`: Roboterzustand und Berechnung der Bewegung.
- `robosim/domain/line_track.py`: geschlossener Rundkurs und Sensorabweichung.
- `robosim/application/robot_controller.py`: Port für austauschbare Steuerungen.
- `robosim/application/simulation.py`: Anwendungsfall, der Regler und Roboter verbindet.
- `robosim/adapters/`: konkrete Regler und die NiceGUI-Oberfläche als Eingabe- und Visualisierungsadapter.

Die Steuerung liefert die Geschwindigkeit des linken und rechten Rades. Im Automatikmodus misst eine Reihe aus fünf virtuellen Reflexsensoren die Lage der Linie vor dem Roboter. Der Linienfolger-Regler bildet aus den Sensorwerten die seitliche Abweichung und korrigiert damit die Radgeschwindigkeiten.

## Kleines Beispiel

```python
from robosim.adapters.manual_controller import ManualController
from robosim.application.simulation import Simulation

controller = ManualController()
controller.set_wheel_speeds(0.5, 0.5)
simulation = Simulation(controller)
simulation.step(seconds=1.0)
print(simulation.robot)
```

## Bewegungstests

Die Testdatei kann direkt in VS Code mit **Run Python File** gestartet werden. Alternativ kannst du sie im Projektordner über das Terminal ausführen:

```powershell
python .\tests\test_robot.py
```

Oder du lässt alle Tests durch `unittest` entdecken:

```powershell
python -m unittest discover -s tests -v
```

Die Tests ergänzen den `src`-Ordner selbst zum Importpfad. Sie prüfen Roboterbewegung, Linienmessung, die Reaktion des Reglers und das Folgen des Rundkurses über eine vollständige Runde.

## NiceGUI starten

Starte im Projektordner die Web-Anwendung:

```powershell
python .\app.py
```

Öffne anschließend `http://localhost:8083` im Browser. Die Anwendung zeigt den Titel „RoboSim | 5-Sensor-Linienfolger“. Wähle zwischen „Manuell“ und „Automatisch geregelt“. Im manuellen Modus stellst du die Geschwindigkeit ein und lenkst mit W/A/S/D, den Pfeiltasten oder den Richtungsbuttons; einen Lenkungsschieber gibt es nicht. Im automatischen Modus folgt der Regler dem geschlossenen Rundkurs anhand der fünf virtuellen Reflexsensoren. Ziellinie, Fahrspur, Fahrzeugkörper und erkannte Sensoren sind in der Grafik sichtbar. „Start“, „Pause“ und „Auf Startposition zurücksetzen“ steuern den Simulationslauf.
