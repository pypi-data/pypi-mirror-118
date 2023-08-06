from enum import Enum


class ErrorCode(Enum):
    """
    Enumeration for internal error code
    """
    FH_NO_ERROR = 0
    FH_STREAM_NO_HEADER = 10001
    FH_STREAM_WRONG_VERSION = 10002
    FH_END_OF_STREAM = 10003
    FH_MESSAGE_DECODE_ERROR = 10004
    FH_COULD_NOT_CONNECT = 10005
    FH_SOCKET_ERROR = 10006
    FH_UNEXPECTED_END_OF_FILE_SEQUENCE = 10007


class InternalError(Exception):
    """
    Internal error raised by py_fort_hermes
    """

    def __init__(self, code: ErrorCode, message):
        self.message = message
        self.code = code
        super().__init__(self.message)


class UnexpectedEndOfFileSequence(Exception):
    """
    The reading of a sequence of file was interrupted by an error

    Fields:
        segmentPath (str): the segment where the error occured
    """

    def __init__(self, what, segmentPath):
        self.segmentPath = segmentPath
        self.message = "Unexpected end of file sequence in '%s': %s" % (
            segmentPath, what)
        super().__init__(self.message)
