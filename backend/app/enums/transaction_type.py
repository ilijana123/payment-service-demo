from enum import Enum

class TransactionType(str,Enum):
    SIMPLE="simple"
    RECURRING="recurring"