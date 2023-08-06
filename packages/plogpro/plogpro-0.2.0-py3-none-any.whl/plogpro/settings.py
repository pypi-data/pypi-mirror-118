from enum import Enum


class LogType(Enum):
    """An enumeration for indicating the severity of a log message

    Attributes:
        DEBUG
            Useful information for debugging only
        INFO
            General information
        WARNING
            A warning to the user
        ERROR
            Information about an error that has occurred
        FATAL
            Information about an error that resulted in a crash
    """
    DEBUG   = 1
    INFO    = 2
    WARNING = 3
    ERROR   = 4
    FATAL   = 5
