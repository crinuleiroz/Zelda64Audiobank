from enum import IntEnum

# Override the default IntEnum __str__ so it returns like a normal Enum
class NamedIntEnum(IntEnum):
    """ Enum where members are also (and must be) ints, but returns the enum name on print. """
    def __str__(self):
        return self.name

class AudioSampleCodec(NamedIntEnum):
    """
    Represents the possible compression formats of an audio sample.

    .. code-block:: c

        typedef enum AudioSampleCodec {
            /* 0 */ CODEC_ADPCM,
            /* 1 */ CODEC_S8,
            /* 2 */ CODEC_S16_INMEM,
            /* 3 */ CODEC_SMALL_ADPCM,
            /* 4 */ CODEC_REVERB,
            /* 5 */ CODEC_S16,
            /* 6 */ CODEC_UNK6,
            /* 7 */ CODEC_UNK7
        } AudioSampleCodec;
    """
    ADPCM = 0
    """ 16 2-byte samples compressed into 4-bit samples. """

    S8 = 1
    """ 16 2-byte samples compressed into 8-bit samples. """

    S16_INMEM = 2
    """ 16 2-byte samples stored as uncompressed 16-bit samples in memory. """

    SMALL_ADPCM = 3
    """ 16 2-byte samples compressed into 2-bit samples. """

    REVERB = 4
    """  """

    S16 = 5
    """ 16 2-byte samples stored as uncompressed 16-bit samples. """

    UNK6 = 6
    """ Unknonwn. """

    UNK7 = 7
    """ Unknown uncompressed. """

class AudioStorageMedium(NamedIntEnum):
    """
    Represents the possible storage mediums of an audio sample.

    .. code-block:: c

        typedef enum AudioStorageMedium {
            /* 0 */ MEDIUM_RAM,
            /* 1 */ MEDIUM_UNK,
            /* 2 */ MEDIUM_CART,
            /* 3 */ MEDIUM_DISK_DRIVE,
            /* 5 */ MEDIUM_RAM_UNLOADED = 5
        } AudioStorageMedium;
    """
    RAM = 0
    """ Data is stored in random-access memory. """

    UNK = 1
    """ Unknown. """

    CART = 2
    """ Data is stored in read-only memory on a cartridge. """

    DISK_DRIVE = 3
    """ Data is stored in read-only memory on a magnetic disk. """

    RAM_UNLOADED = 5
    """ Data is stored in random-access memory but has been unloaded. """


class AudioCacheLoadType(NamedIntEnum):
    """
    Represents the possible audio cache load types.

    .. code-block:: c

        typedef enum AudioCacheLoadType {
            /* 0 */ CACHE_LOAD_PERMAENT,
            /* 1 */ CACHE_LOAD_PERSISTENT,
            /* 2 */ CACHE_LOAD_TEMPORARY,
            /* 3 */ CACHE_LOAD_EITHER,
            /* 4 */ CACHE_LOAD_EITHER_NOSYNC,
        } AudioSampleCodec;
    """
    LOAD_PERMANENT = 0
    """ Audio data is loaded into the permanent audio cache. """

    LOAD_PERSISTENT = 1
    """ Audio data is loaded into the persistent audio cache. """

    LOAD_TEMPORARY = 2
    """ Audio data is loaded into the temporary audio cache. """

    LOAD_EITHER = 3
    """ Audio data is loaded into either the persistent or temporary audio cache. """

    LOAD_EITHER_NOSYNC = 4
    """ Audio data is loaded into either the persistent or temporary audio cache without syncing. """

class AdsrOpcode(NamedIntEnum):
    """
    Represents available ADSR opcodes. Any value above 0 is treated as a value of time.

    .. code-block:: c

        #define ADSR_DISABLE 0
        #define ADSR_HANG -1
        #define ADSR_GOTO -2
        #define ADSR_RESTART -3
    """
    DISABLE = 0
    """ Stops envelope processing. Notes are disabled and stop sounding immediately, bypassing their release phase. """

    HANG = -1
    """ Pauses envelope processing. Notes remain enabled and continue to sound until they enter their release phase. """

    GOTO = -2
    """ Jumps to the specified index in the envelope array. """

    RESTART = -3
    """ Restarts envelope processing. """