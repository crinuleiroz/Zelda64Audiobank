from ..bankstruct import *

from .envelope import Envelope
from .tuned_sample import TunedSample

class Drum(BankStruct):
    """
    Represents drum data in the instrument bank.

    .. code-block:: c

        typdef struct Drum {
            /* 0x00 */ u8 decayIndex;
            /* 0x04 */ u8 pan;
            /* 0x08 */ u8 isRelocated;
            /* 0x04 */ TunedSample tunedSample;
            /* 0x0C */ struct Envelope* envelope;
        } Drum; // Size = 0x10
    """
    _fields_ = [
        ('decay_index', u8),
        ('pan', u8),
        ('is_relocated', u8),
        ('_pad', u8),
        ('tuned_sample', TunedSample),
        ('envelope', pointer(Envelope))
    ]
    _bool_fields_ = ['is_relocated']
    # _align_ = 0x10