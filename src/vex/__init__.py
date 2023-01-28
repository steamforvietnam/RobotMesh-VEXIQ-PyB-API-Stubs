"""VEX module.

VEXcode IQ: codeiq.vex.com
VEXcode V5: codev5.vex.com
VEXcode VR: vr.vex.com

Robot Mesh VEX IQ Python B:
robotmesh.com/studio/content/docs/vexiq-python_b/html/namespacevex.html

Robot Mesh VEX V5 Python:
robotmesh.com/studio/content/docs/vexv5-python/html/namespacevex.html
"""


from collections.abc import Sequence
from importlib.metadata import version
import sys
from threading import Thread
from typing import LiteralString, Optional

from abm import interactive

# from ._abstract_device import Device

from .brain import (
    Brain, BrainBattery, BrainButton,
    BrainLcd,
    Font,
    MONO_M, MONO_L, MONO_XL, MONO_XXL, MONO_S, MONO_XS,
    PROP_M, PROP_L, PROP_XL, PROP_XXL,
    FontType,
    BrainSound, NoteType, SoundType)

from .brain.port import Ports

from .controller import (Controller,
                         ControllerAxis,
                         ControllerButton,
                         ControllerType, PRIMARY, PARTNER)

from .brain.inertial_sensor import Inertial

from .motor import (Motor,
                    BrakeType, COAST, BRAKE, HOLD,
                    CurrentUnits,
                    DirectionType, FORWARD, REVERSE,
                    TurnType, LEFT, RIGHT,
                    TorqueUnits,
                    VoltageUnits)

from .bumper_switch_sensor import Bumper
from .color_sensor import ColorSensor, Colorsensor
from .distance_sensor import Distance, ObjectSizeType, Sonar
from .gyro_sensor import Gyro, GyroCalibrationType
from .optical_sensor import Optical, LedStateType, GestureType
from .touch_led import Touchled, FadeType

from .multi_device_group import MotorGroup, DriveTrain, SmartDrive

from .time import TimeUnits, SECONDS, MSEC, clock, wait

from ._common_enums import (AxisType, XAXIS, YAXIS, ZAXIS,
                            Color, ColorHue,
                            OrientationType, ROLL, PITCH, YAW,
                            PercentUnits, PERCENT,
                            DistanceUnits, MM, INCHES,
                            RotationUnits, DEGREES, TURNS,
                            VelocityUnits, RPM, DPS)

from ._util.doc import robotmesh_doc
from ._util.type import NumType


__all__: Sequence[LiteralString] = (
    '__version__',

    # 'Device',

    'Brain', 'BrainBattery', 'BrainButton',
    'BrainLcd',
    'Font',
    'MONO_M', 'MONO_L', 'MONO_XL', 'MONO_XXL', 'MONO_S', 'MONO_XS',
    'PROP_M', 'PROP_L', 'PROP_XL', 'PROP_XXL',
    'FontType',
    'BrainSound', 'NoteType', 'SoundType',

    'Ports',

    'Controller',
    'ControllerAxis',
    'ControllerButton',
    'ControllerType', 'PRIMARY', 'PARTNER',

    'Inertial',

    'Motor',
    'BrakeType', 'COAST', 'BRAKE', 'HOLD',
    'CurrentUnits',
    'DirectionType', 'FORWARD', 'REVERSE',
    'TorqueUnits',
    'TurnType', 'LEFT', 'RIGHT',
    'VelocityUnits', 'RPM', 'DPS',
    'VoltageUnits',

    'Bumper',
    'ColorSensor', 'Colorsensor',
    'Optical', 'LedStateType', 'GestureType',
    'Distance', 'ObjectSizeType',
    'Sonar',
    'Gyro', 'GyroCalibrationType',
    'Touchled', 'FadeType',

    'MotorGroup', 'DriveTrain', 'SmartDrive',

    'TimeUnits', 'SECONDS', 'MSEC', 'wait',

    'AxisType', 'XAXIS', 'YAXIS', 'ZAXIS',
    'Color', 'ColorHue',
    'OrientationType', 'ROLL', 'PITCH', 'YAW',
    'PercentUnits', 'PERCENT',
    'DistanceUnits', 'MM', 'INCHES',
    'RotationUnits', 'DEGREES', 'TURNS',

    'SYSTEM_DISPLAY_WIDTH', 'SYSTEM_DISPLAY_HEIGHT', 'STATUS_BAR_HEIGHT',
    'RUMBLE_LONG', 'RUMBLE_SHORT', 'RUMBLE_PULSE',

    'interactive',
)


__version__: LiteralString = version(distribution_name='VEX-Py')


# CONSTANTS
# =========

INT29_MAX: int = 0x1FFFFFFF


SYSTEM_DISPLAY_WIDTH: int = 480
SYSTEM_DISPLAY_HEIGHT: int = 272
STATUS_BAR_HEIGHT: int = 32

RUMBLE_LONG: LiteralString = '----'
RUMBLE_SHORT: LiteralString = '....'
RUMBLE_PULSE: LiteralString = '-.-.'


# FUNCTIONS
# =========

@robotmesh_doc("""
    Runs the given function in a thread sharing the current global namespace.
""")
def run_in_thread(f: callable):  # pylint: disable=invalid-name
    """Run specified function in parallel thread."""
    Thread(group=None, target=f, name=None, args=(), kwargs={}, daemon=True).start()  # noqa: E501


@robotmesh_doc("""
    Wait until a function returns a value.

    Returns True when reached, False on timeout.

    Parameters
    - func: function to run until it returns the value
    - value: return value to wait for; default True
    - timeout: timeout in seconds; if reached returns False;
               default None (no timeout)
    - check_period: time to wait between checks, in seconds;
                    default 0 (no wait)
""")
def wait_for(func: callable, value: bool = True,
             timeout: Optional[int] = None, check_period: NumType = 0) -> bool:
    # pylint: disable=unused-argument
    """Wait for specified function to return specified target value."""


# ALIASES
# =======

sys.clock: callable = clock
sys.sleep: callable = wait
sys.maxint: int = INT29_MAX
sys.run_in_thread: callable = run_in_thread
sys.wait_for: callable = wait_for
