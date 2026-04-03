from enum import Enum

class SchedulesFrequency(str,Enum):
    DAILY="daily"
    WEEKLY="weekly"
    MONTHLY="monthly"