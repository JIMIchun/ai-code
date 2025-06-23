# 枚举文件
from enum import Enum

class IdentityType(Enum):
    MODEL = 'MODEL'
    USER = 'USER'

class MessageType(Enum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    VIDEO = 'VIDEO'