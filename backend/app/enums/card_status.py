from enum import Enum

class CardStatus(str, Enum):
    ACTIVE="active"
    BLOCKED="blocked"
    REPORTED_STOLEN="reported_stolen"
    REPORTED_LOST="reported_lost"