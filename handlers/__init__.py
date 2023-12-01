from dataclasses import dataclass

@dataclass
class SystemVariables:
    USER_MSG = {}
    SPAM_LIST = []
    BLACK_LIST = []
    ACTIVE = 0
    BREAK = False
