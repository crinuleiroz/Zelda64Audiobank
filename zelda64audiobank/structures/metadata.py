from ..bankstruct import *
from ..constants import AudioStorageMedium, AudioCacheLoadType
from ..helpers import safe_enum

class AudiobankEntry(BankStruct):
    """
    Represents an instrument bank's corresponding table entry.

    .. code-block:: c

        typdef struct AudiobankEntry {
            /* 0x00 */ uintptr_t romAddr;
            /* 0x04 */ size_t size;
            /* 0x08 */ s8 medium;
            /* 0x09 */ s8 cacheLoadType;
            /* 0x0A */ u8 sampleBankId1;
            /* 0x0B */ u8 sampleBankId2;
            /* 0x0C */ u8 numInstruments;
            /* 0x0D */ u8 numDrums;
            /* 0x0E */ u16 numEffects;
        } AudiobankEntry; // Size = 0x10
    """
    _fields_ = [
        ('rom_addr', u32),
        ('bank_size', u32),
        ('medium', u8),
        ('cache_load_type', u8),
        ('sample_bank_id_1', u8),
        ('sample_bank_id_2', u8),
        ('num_instruments', u8),
        ('num_drums', u8),
        ('num_effects', u16)
    ]
    _enum_fields_ = {
        'medium': AudioStorageMedium,
        'cache_load_type': AudioCacheLoadType
    }
    # _align_ = 0x10