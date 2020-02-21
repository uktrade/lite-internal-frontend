from enum import Enum


class CaseType(Enum):
    APPLICATION = "application"
    STANDARD = "standard"
    OPEN = "open"
    HMRC = "hmrc"
    # The case_type_reference for HMRC
    HMRC_REFERENCE = "cre"
    GOODS = "goods"
    END_USER_ADVISORY = "end_user_advisory"
    EXHIBITION = "exhibition_clearance"
    GIFTING = "gifting_clearance"
    F680 = "f680_clearance"
