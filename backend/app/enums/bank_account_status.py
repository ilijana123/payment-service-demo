from enum import Enum

class BankAccountStatus(str,Enum):
    ACTIVE="active"
    SUSPENDED="suspended"
    CLOSED="closed"