from enum import Enum


class CaseType(Enum):
    STANDARD = "standard"
    OPEN = "open"
    HMRC = "hmrc"
    END_USER_ADVISORY = "end_user_advisory"
    APPLICATION = "application"
    GOODS = "goods"
    EXHIBITION = "exhibition_clearance"
