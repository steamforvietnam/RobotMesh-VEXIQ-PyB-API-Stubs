"""Drive Train."""


from collections.abc import Sequence
from typing import Literal, Optional
from typing_extensions import Self

from abm.decor import act, sense

from ..motor import Motor
from ..motor.brake_type import BrakeType, BRAKE
from ..motor.direction_type import DirectionType, FORWARD
from ..motor.turn_type import TurnType, RIGHT
from ..motor.velocity_units import VelocityUnits, PERCENT
from ..time.time_units import TimeUnits
from ..units_common.distance import DistanceUnits, MM
from ..units_common.electric import CurrentUnits
from ..units_common.rotation import RotationUnits, DEGREES
from ..util.doc import vexcode_doc

from .motor_group import MotorGroup


__all__: Sequence[str] = ('DriveTrain',)


class DriveTrain(MotorGroup):
    """Drive Train."""

    def __init__(self, left_motor: Motor, right_motor: Motor,
                 wheel_base: float = 200, track_width: float = 176,
                 length_unit: DistanceUnits = MM, gear_ratio: float = 1, /):
        """Initialize Drivetrain."""
        super().__init__(motor_a=left_motor, motor_b=right_motor)

        self.left_motor: Motor = left_motor
        self.right_motor: Motor = right_motor
        self.wheel_base: float = wheel_base
        self.track_width: float = track_width
        self.length_unit: DistanceUnits = length_unit
        self.gear_ratio: float = gear_ratio

        self.drive_velocities: dict[VelocityUnits, float] = \
            dict[VelocityUnits, float]()
        self.turn_velocities: dict[VelocityUnits, float] = \
            dict[VelocityUnits, float]()
        self.stopping_mode: Optional[BrakeType] = None

    def __eq__(self, other: Self) -> bool:
        """Check equality."""
        return (isinstance(other, DriveTrain) and
                (other.left_motor == self.left_motor) and
                (other.right_motor == self.right_motor) and
                (other.wheel_base == self.wheel_base) and
                (other.track_width == self.track_width) and
                (other.length_unit == self.length_unit) and
                (other.gear_ratio == self.gear_ratio))

    def __hash__(self) -> int:
        """Return integer hash."""
        return hash((self.left_motor, self.right_motor,
                     self.wheel_base, self.track_width,
                     self.length_unit, self.gear_ratio))

    @vexcode_doc("""
        Drive

        Moves the Drivetrain forever in the direction
        specified inside the parentheses.

        All Drivetrain motors run forward or in reverse
        at the velocity set using the Drivetrain's Set Drive Velocity command.
        The default velocity is 50%.

        Negative values will cause the Drivetrain to
        drive forward with a REVERSE input and in reverse with a FORWARD input.

        The Drive command will run the Drivetrain forever,
        until a new drivetrain command is used, or the program is stopped.
    """)
    @act
    def drive(self, direction: DirectionType = FORWARD, /):
        """Drive in specified direction."""

    @vexcode_doc("""
        Drive For

        Moves the Drivetrain for a given distance.
        All Drivetrain motors run forward or in reverse at the velocity
        set by the Drivetrain's Set Drive Velocity command.
        After the Drivetrain has moved the specified distance
        the Drivetrain will stop.

        Set how far the Drivetrain will move by entering at least
        three valid arguments inside of the parentheses, separated by commas.

        - The first argument specifies the direction.
          Valid inputs are either FORWARD or REVERSE in all capital letters.

        - The second argument specifies the distance
          that the IQ Robot should drive.

        - The third argument specifies the unit of measurement
          that should be used. Valid inputs are either INCHES or MM
          (millimeters) in all-capital letters.

        The DISTANCE parameter accepts numeric values.
        Negative values will cause the IQ Robot to drive
        in the opposite of the input DIRECTION.

        The Drive For command is by default a blocking command.
        It will prevent subsequent commands from executing
        until the Drivetrain movement has completed.

        You can set a fourth parameter to wait=False to allow
        proceeding commands to run even before the Drivetrain is done moving.
    """)
    @act
    def drive_for(self, direction: DirectionType = FORWARD,
                  distance: float = 200, unit: DistanceUnits = MM,
                  wait: bool = True, /):
        """Drive for a distance."""

    @vexcode_doc("""
        Turn

        Turns the Drivetrain to the right or left indefinitely.

        The Turn command will rotate the Drivetrain in the given direction
        forever until a new Drivetrain command is used,
        or until the program is stopped.

        Use the LEFT argument in all-capital letters
        to turn the Drivetrain to the left.

        Use the RIGHT argument in all-capital letters
        to turn the Drivetrain to the right.
    """)
    @act
    def turn(self, direction: TurnType = RIGHT, /):
        """Turn."""

    @vexcode_doc("""
        Turn For

        Turns the Drivetrain in the specified direction
        for a set number of degrees.

        - The first argument specifies the turn direction: LEFT or RIGHT,
          written in all-capital letters.

        - The second argument specifies the turn angle as a numeric value;
          this can be any number or numeric variable.

        - The third argument is the turn unit.
          This should be set as DEGREES in all-capital letters.

        The Turn For command is by default a blocking command.
        It prevents any proceeding code from executing until
        the Drivetrain has completed its turn.

        If the fourth argument is set to wait=False,
        proceeding commands will be allowed to execute
        even before the Drivetrain has completed its turn.
    """)
    @act
    def turn_for(  # pylint: disable=unused-argument
            self, direction: TurnType = RIGHT,
            angle: float = 90, unit: Literal[DEGREES] = DEGREES,
            wait: bool = True, /):
        """Turn for an angle."""
        assert unit is DEGREES, ValueError('*** ANGULAR UNIT MUST BE DEGREES ***')  # noqa: E501

    @vexcode_doc("""
        Stop

        Stops the Drivetrain.

        The Stop command stops the Drivetrain.
        It does not take any arguments in its parentheses.
    """)
    @act
    def stop(self):
        """Stop motors."""

    @vexcode_doc("""
        Set Drive Velocity

        Sets the velocity of the Drivetrain for Drive and Drive For commands.

        Set Drive Velocity will set the Drivetrain's velocity
        when used with a Drive or Drive For command.
        It will not cause the Drivetrain to move when used by itself.

        Set Drive Velocity accepts a range of values
        depending on what units are passed as the second parameter.

        If PERCENT is used as the second parameter,
        VELOCITY accepts a range from -100 to 100.

        Set Drive Velocity can also use RPM as a valid UNITS parameter,
        accepting a range from -127 to 127.

        Setting a Drivetrain's drive velocity to a negative value
        will cause the Drivetrain to drive opposite of the DIRECTION
        passed into a Drive or Drive For command.

        Setting a Drivetrain's drive velocity to 0 will prevent the Drivetrain
        from moving even if a Drive or Drive For command is used.
    """)
    @act
    def set_drive_velocity(self, velocity: int, unit: VelocityUnits = PERCENT, /):  # noqa: E501
        """Set driving velocity."""
        self.drive_velocities[unit] = velocity

    @vexcode_doc("""
        Set Turn Velocity

        Sets the Drivetrain's turn velocity.

        Set Turn Velocity will set the velocity of the Drivetrain when turning,
        but will not cause the Drivetrain to move
        when used without a Turn or Turn For command.

        Set Turn Velocity accepts a range of values
        depending on what units are passed as the second parameter.

        If PERCENT is used as the second parameter,
        VELOCITY accepts a range from -100 to 100.

        Alternatively, Set Turn Velocity can also use RPM as a valid UNITS
        parameter, accepting a range from -127 to 127 as the VELOCITY.

        Setting a Drivetrain's turn velocity to a negative value
        will cause the Drivetrain to turn in the opposite of the direction
        passed into any following drivtrain.turn commands.

        Setting a Drivetrain's turn velocity to 0
        will prevent the Drivetrain from turning.
    """)
    @act
    def set_turn_velocity(self, velocity: int, unit: VelocityUnits = PERCENT, /):  # noqa: E501
        """Set turning velocity."""
        self.turn_velocities[unit] = velocity

    @vexcode_doc("""
        Set Motor Stopping

        Sets the behavior of an IQ Motor or Motor Group once it stops moving.

        The MODE parameter can be replaced with any of the following options:
        - BRAKE: will cause the Motor/Motor Group to come to an immediate stop.
        - COAST: lets the Motor/Motor Group spin gradually to a stop.
        - HOLD: will cause the Motor/Motor Group to come to an immediate stop,
                and returns it to its stopped position if moved.

        The stopping behavior set by this command
        will apply to subsequent Motor/Motor Group Stop commands
        for the entirety of the project, unless otherwise changed.
    """)
    @act
    def set_stopping(self, mode: BrakeType = BRAKE, /):
        """Set motor stopping mode."""
        self.stopping: BrakeType = mode
