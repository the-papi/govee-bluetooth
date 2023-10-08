import enum
from functools import reduce


class GoveePower(enum.IntEnum):
    BOTH_OFF = 0x00
    BOTH_ON = 0x11
    LEFT_ON_RIGHT_OFF = 0x10
    LEFT_OFF_RIGHT_ON = 0x01


class GoveeSegment(enum.IntEnum):
    LEFT_SEGMENT_0 = 0b00000001_00000000
    LEFT_SEGMENT_1 = 0b00000010_00000000
    LEFT_SEGMENT_2 = 0b00000100_00000000
    LEFT_SEGMENT_3 = 0b00001000_00000000
    LEFT_SEGMENT_4 = 0b00010000_00000000
    LEFT_SEGMENT_5 = 0b00100000_00000000

    RIGHT_SEGMENT_0 = 0b01000000_00000000
    RIGHT_SEGMENT_1 = 0b10000000_00000000
    RIGHT_SEGMENT_2 = 0b00000000_00000001
    RIGHT_SEGMENT_3 = 0b00000000_00000010
    RIGHT_SEGMENT_4 = 0b00000000_00000100
    RIGHT_SEGMENT_5 = 0b00000000_00001000


GOVEE_LEFT_SEGMENTS_ALL = \
    GoveeSegment.LEFT_SEGMENT_0 \
    | GoveeSegment.LEFT_SEGMENT_1 \
    | GoveeSegment.LEFT_SEGMENT_2 \
    | GoveeSegment.LEFT_SEGMENT_3 \
    | GoveeSegment.LEFT_SEGMENT_4 \
    | GoveeSegment.LEFT_SEGMENT_5

GOVEE_RIGHT_SEGMENTS_ALL = \
    GoveeSegment.RIGHT_SEGMENT_0 \
    | GoveeSegment.RIGHT_SEGMENT_1 \
    | GoveeSegment.RIGHT_SEGMENT_2 \
    | GoveeSegment.RIGHT_SEGMENT_3 \
    | GoveeSegment.RIGHT_SEGMENT_4 \
    | GoveeSegment.RIGHT_SEGMENT_5

GOVEE_SEGMENTS_ALL = GOVEE_LEFT_SEGMENTS_ALL | GOVEE_RIGHT_SEGMENTS_ALL


class GoveeProtocol:

    @staticmethod
    def checksum(packet: bytes) -> int:
        """Calculate checksum for packet."""
        return reduce(lambda x, y: x ^ y, packet)

    @classmethod
    def add_checksum(cls, packet: bytes) -> bytes:
        """Add checksum to packet."""
        return packet + bytes([cls.checksum(packet)])

    @staticmethod
    def power(power: GoveePower) -> bytes:
        """Generate packet for power control."""
        return bytes([0x33, 0x33, int(power)])

    @staticmethod
    def keep_alive() -> bytes:
        """Generate keep alive packet."""
        return bytes([0xAA, 0x33, *([0x0] * 17), 0x99])

    @classmethod
    def rgb(cls, segments: int, red: int, green: int, blue: int) -> bytes:
        """Generate packet for RGB control."""
        packet = bytes([
            0x33, 0x05, 0x15, 0x01,
            red, green, blue,
            *([0x0] * 5),
            (segments >> 8) & 0xFF, segments & 0xFF,
            *([0x0] * 5),
        ])

        return cls.add_checksum(packet)

    @classmethod
    def brightness(cls, segments: int, brightness: int) -> bytes:
        """Generate packet for brightness control."""
        if brightness < 0 or brightness > 100:
            raise ValueError("Brightness must be between 0 and 100.")

        packet = bytes([
            0x33, 0x05, 0x15, 0x02,
            brightness,
            (segments >> 8) & 0xFF, segments & 0xFF,
            *([0x0] * 12),
        ])

        return cls.add_checksum(packet)
