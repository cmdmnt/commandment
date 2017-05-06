from enum import Enum, IntFlag, auto


class ScheduledPowerEventType(Enum):
    wake = 'wake'
    wakepoweron = 'wakepoweron'
    sleep = 'sleep'
    shutdown = 'shutdown'
    restart = 'restart'


class ScheduledPowerEventWeekdays(IntFlag):
    def _generate_next_value_(name, start, count, last_values):
        return 2 ** count

    Monday = auto()
    Tuesday = auto()
    Wednesday = auto()
    Thursday = auto()
    Friday = auto()
    Saturday = auto()
    Sunday = auto()

    All = Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday
