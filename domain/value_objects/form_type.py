from enum import Enum


class FormType(str, Enum):
    PRODUCT_FEEDBACK = "product_feedback"
    SUPPORT_TICKET = "support_ticket"
    SURVEY = "survey"
    CUSTOM = "custom"
