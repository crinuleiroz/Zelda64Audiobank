from enum import IntEnum

from ..bankstruct import *

class VadpcmLoopCount(IntEnum):
    NO_LOOP = 0
    """ Represents an audio sample that plays once. """

    INDEFINITE_LOOP = 0xFFFFFFFF # 4294967295
    """ Represents an audio sample that plays indefinitely. """

class VadpcmLoopHeader(BankStruct):
    """
    Represents the first 16 bytes of the VadpcmLoop structure.

    .. code-block:: c

        typedef struct VadpcmLoopHeader {
            /* 0x00 */ u32 loopStart;
            /* 0x04 */ u32 loopEnd;
            /* 0x08 */ u32 loopCount;
            /* 0x0C */ u32 numSamples;
        } VadpcmLoopHeader; // Size = 0x10
    """
    _fields_ = [
        ('loop_start', u32),
        ('loop_end', u32),
        ('loop_count', u32),
        ('num_samples', u32)
    ]
    _enum_fields_ = {
        'loop_count': VadpcmLoopCount
    }

class VadpcmLoop(BankStruct):
    """
    Represents audio sample loop information in the instrument bank.

    .. code-block:: c

        typedef struct VadpcmLoop {
            /* 0x00 */ VadpcmLoopHeader header;
            /* 0x10 */ s16 predictorCoeff[16];
        } VadpcmLoop; // Size = 0x10 or 0x30
    """
    _fields_ = [
        ('header', VadpcmLoopHeader),
        ('predictors', array(s16, 0))
    ]

    # Override because the array is conditional based on header values
    @classmethod
    def from_bytes(cls, buffer: bytes, struct_offset:int = 0):
        obj = cls.__new__(cls)

        obj.header = VadpcmLoopHeader.from_bytes(buffer, struct_offset)
        header_size = VadpcmLoopHeader.size()

        if obj.header.loop_start == 0:
            obj.predictors = array(s16, 0)
        else:
            predictor_offset = struct_offset + header_size
            obj.predictors = array(s16, 16).from_bytes(buffer, predictor_offset)

        return obj

    def __repr__(self):
        header_repr = repr(self.header).replace('\n', '\n  ')
        if not self.predictors or len(self.predictors) == 0:
            preds = '[]'
        else:
            grouped = [
                ', '.join(f'{v}' for v in self.predictors[i:i+4])
                for i in range(0, len(self.predictors), 4)
            ]
            preds = '[\n' + '\n'.join(f'    {line},' for line in grouped) + '\n  ]'
        return (
            f'{type(self).__name__}(\n'
            f'  header={header_repr}\n'
            f'  predictors={preds}\n'
            f')'
        )

class VadpcmBookHeader(BankStruct):
    """
    Represents the first 8 bytes of the VadpcmBook structure.

    .. code-block:: c

        typedef struct VadpcmBookHeader {
            /* 0x00 */ s32 order;
            /* 0x04 */ s32 numPredictors;
        } VadpcmBookHeader; // Size = 0x08
    """
    _fields_ = [
        ('order', s32),
        ('num_predictors', s32)
    ]

class VadpcmBook(BankStruct):
    """
    Represents audio sample decoding information in the instrument bank.

    .. code-block:: c

        typedef struct VadpcmBook {
            /* 0x00 */ VadpcmBookHeader header;
            /* 0x08 */ s16 predictorCoeff[1];
        } VadpcmBook; // Size = 0x08 * header.order * header.numPredeictors
    """
    _fields_ = [
        ('header', VadpcmBookHeader),
        ('predictors', array(s16, 0))
    ]
    _align_ = 0x10

    @classmethod
    def from_bytes(cls, buffer: bytes, struct_offset: int = 0):
        obj = cls.__new__(cls)

        obj.header = VadpcmBookHeader.from_bytes(buffer, struct_offset)
        header_size = VadpcmBookHeader.size()

        order = obj.header.order
        num_predictors = obj.header.num_predictors
        total_coeff = 8 * order * num_predictors

        predictor_offset = struct_offset + header_size
        obj.predictors = array(s16, total_coeff).from_bytes(buffer, predictor_offset)

        return obj

    def __repr__(self):
        header_repr = repr(self.header).replace('\n', '\n  ')
        if not self.predictors or len(self.predictors) == 0:
            preds_repr = '[]'
        else:
            grouped = [
                ', '.join(f'{v}' for v in self.predictors[i:i+4])
                for i in range(0, len(self.predictors), 4)
            ]
            preds_repr = '[\n' + '\n'.join(f'    {line},' for line in grouped) + '\n  ]'

        return (
            f'{type(self).__name__}(\n'
            f'  header={header_repr}\n'
            f'  predictors={preds_repr}\n'
            f')'
        )