"""BSMP PS."""

from siriuspy.pwrsupply.bsmp.constants import ConstPSBSMP as _ConstPSBSMP


class BasePSAckError(Exception):
    """Exception raised when the ack response is not the expected"""

    def __init__(self, message, *args: object) -> None:
        super().__init__(*args)


class FunctionExecutionPSAckError(BasePSAckError):
    """."""


class InvalidCommandPSAckError(BasePSAckError):
    """."""


class DSPBusyPSAckError(BasePSAckError):
    """."""


class DSPTimeoutPSAckError(BasePSAckError):
    """."""


class ResourceBusyPSAckError(BasePSAckError):
    """."""


class UDCLockedPSAckError(BasePSAckError):
    """."""


class PSInterlockPSAckError(BasePSAckError):
    """."""


# def check_return_code(code: int):
#    """Check return code and raise the corresponding exception"""
#
#   if code == _ConstPSBSMP.ACK_INVALID_CMD:
#       raise InvalidCommandPSAckError()
#   elif code == _ConstPSBSMP.ACK_DSP_BUSY:
#       raise DSPBusyPSAckError()
#   elif code == _ConstPSBSMP.ACK_RESOURCE_BUSY:
#       raise ResourceBusyPSAckError()
