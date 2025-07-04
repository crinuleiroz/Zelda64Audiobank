from ..bankstruct import *

from ..constants import AdsrOpcode
from ..helpers import safe_enum

class EnvelopePoint(BankStruct):
    """
    Represents a single pair of time or opcode and amp or index values in an envelope array.

    .. code-block:: c

        typedef struct EnvelopePoint {
            /* 0x00 */ s16 timeOrOpcode;
            /* 0x02 */ s16 ampOrIndex;
        } EnvelopePoint; // Size = 0x04
    """
    _fields_ = [
        ('_timeOrOpcode', s16),
        ('ampOrIndex', s16)
    ]

    @property
    def timeOrOpcode(self):
        val = self._timeOrOpcode

        if val <= 0:
            try:
                return AdsrOpcode(val)
            except ValueError:
                return val
        else:
            return val

    @property
    def is_opcode(self):
        return self._timeOrOpcode <= 0

class Envelope(BankStruct):
    """
    Represents an array of EnvelopePoint structures in the instrument bank.

    In MIPS, words *cannot* begin at an odd memory alignment, they must be 2-byte aligned.
    """
    _fields_ = []
    _align_ = 0x10

    def __init__(self):
        self.points: list[EnvelopePoint] = []

    @classmethod
    def from_bytes(cls, buffer: bytes, struct_offset: int = 0):
        obj = cls()
        offset = struct_offset

        while True:
            point = EnvelopePoint.from_bytes(buffer, offset)
            obj.points.append(point)
            offset += EnvelopePoint.size()

            if point.is_opcode:
                break

        return obj