from enum import Enum

class TransactionStatus(str,Enum):
    PENDING="pending"
    APPROVED="approved"
    DECLINED="declined"
    CANCELLED="cancelled"