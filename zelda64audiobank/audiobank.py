"""
Audiobank
=====
"""
import struct

from .structures.metadata import AudiobankEntry
from .structures.instrument import Instrument
from .structures.drum import Drum
from .structures.tuned_sample import TunedSample

class Audiobank:
    """
    Represents a Zelda64 instrument bank.

    Attributes:
        from_bytes (method): Parses binary data and creates an `Audiobank` object in memory.
    """
    def __init__(self):
        self.metadata: AudiobankEntry = None
        self.instruments: list[Instrument] = []
        self.drums: list[Drum] = []
        self.effects: list[TunedSample] = []
        self.drum_list_offset: int = 0
        self.effect_list_offset: int = 0

    @classmethod
    def from_bytes(cls, table_entry: bytes, bank_data: bytes):
        """
        Instantiates an instrument bank object using binary data.

        Args:
            table_entry (bytes): Binary table entry data. Can be either truncated (0x08) or full (0x10) bytes long.
            bank_data (bytes): Binary instrument bank data.

        Returns:
            object (Audiobank): A fully parsed instrument bank.
        """
        # There are two table_entry lengths possible at the current time taking OOTR and MMR music into account.
        # The regular table_entry length from the audiobank index in code is 16 bytes long and includes an address
        # to the audiobank and its size in bytes. The truncated tables used by custom music files for OOTR and MMR
        # are only 8 bytes long because the address and size are built by the randomizers.
        match len(table_entry):
            case 0x08:
                _table_entry: bytes = (b'\x00' * 8) + table_entry
            case 0x10:
                _table_entry: bytes = table_entry
            case _:
                raise ValueError(f'Unexpected table entry size, expected 0x08 or 0x10 bytes, but got {hex(len(table_entry))} bytes instead!')

        obj = cls()

        obj.metadata = AudiobankEntry.from_bytes(_table_entry)
        obj.drum_list_offset, obj.effect_list_offset = struct.unpack('>2I', bank_data[:0x08])

        # From this point, the from_bytes method will walk through every structure that has a pointer or data (effects)
        # and fully instantiate every required child structure. Effects are just a TunedSample struct, so the effect list
        # is just a list of TunedSample structs instead of a list of pointers to another struct. This means each entry is
        # 8 bytes long instead of 4 bytes, because that is the size of the TunedSample struct.

        # Drums
        for i in range(0, obj.metadata.num_drums):
            offset = obj.drum_list_offset + (i * 4)
            drum_offset = struct.unpack_from('>I', bank_data, offset)[0]
            if drum_offset != 0:
                obj.drums.append(Drum.from_bytes(bank_data, drum_offset))

        # Effects
        for i in range(0, obj.metadata.num_effects):
            offset = obj.effect_list_offset + (8 * i)
            effect = bank_data[offset:offset + 0x08]
            if effect != (b'\x00' * 8):
                obj.effects.append(TunedSample.from_bytes(bank_data, offset))

        # Instruments
        for i in range(0, obj.metadata.num_instruments):
            offset = 0x08 + (i * 4)
            instrument_offset = struct.unpack_from('>I', bank_data, offset)[0]
            if instrument_offset != 0:
                obj.instruments.append(Instrument.from_bytes(bank_data, instrument_offset))

        return obj

    def __repr__(self):
        ...
