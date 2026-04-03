from enum import Enum

class EmailVerificationPurpose(str, Enum):
    REGISTRATION="registration"
    CARD_ADD="card_add"
    CARD_ACTION="card_action"
    LOGIN_2FA="login_2fa"