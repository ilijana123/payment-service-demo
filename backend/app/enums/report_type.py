from enum import Enum

class CardReportType(str,Enum):
    STOLEN="stolen"
    LOST="lost"
    MANUAL_BLOCK="manual_block"