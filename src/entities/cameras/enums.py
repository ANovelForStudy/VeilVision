from enum import Enum


class CameraStatusEnum(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"
    CONNECTING = "connecting"
    UNKNOWN = "unknown"
