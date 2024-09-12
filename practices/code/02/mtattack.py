# The MT19937 used by python's ‘random’ module uses a 32-bit word length and a
# working area/internal state of 624 words.
# As such, after observing the first 624 words (or any 625 consecutive words),
# we are able to recover the internal state, and predict subsequent output.

import random

TEMPER_U = 11
TEMPER_S = 7
TEMPER_T = 15
TEMPER_L = 18

TEMPERING_MASK_B = 0x9D2C5680
TEMPERING_MASK_C = 0xEFC60000

NUM_WORDS = 624
WORD_LEN_BITS = 32
WORD_LEN_BYTES = WORD_LEN_BITS // 8


def untemper(y: int) -> int:
    # Bit-hacking magic.
    y ^= y >> TEMPER_L
    y ^= y << TEMPER_T & TEMPERING_MASK_C
    for _ in range(7):
        y ^= y << TEMPER_S & TEMPERING_MASK_B
    for _ in range(3):
        y ^= y >> TEMPER_U
    return y


def prepare_state(nums: list[int], index: int) \
        -> tuple[int, tuple[int, ...], None]:
    # Simply replace the state in rand.getstate():
    # (3, (int1, int2, ..., 624), None)
    return 3, tuple(nums + [index]), None


def recover(mt_bytes: bytes, first2496: bool = False) -> random.Random | None:
    """Recover the ``random.Random()`` internal state.

    The method requires at least 2500 bytes of data for the recovery of the
    PRNG state. The bytes need to align with the PRNG integer output.
    :param mt_bytes: The PRNG output bytes
    :param first2496: Whether the bytes are the first 2496 PRNG output bytes
    :return: the generator initialised with the recovered state, or ``None`` if
        recovery failed
    :raise ValueError: Raised if not enough bytes are provided for recovery
    """
    min_required = (NUM_WORDS + 1) * WORD_LEN_BYTES
    if len(mt_bytes) < min_required:
        raise ValueError(f"recovery requires at least {min_required} bytes")

    untempered: list[int] = []
    idx = 0
    for _ in range(NUM_WORDS):
        word = int.from_bytes(mt_bytes[idx:idx + WORD_LEN_BYTES], "little")
        untempered.append(untemper(word))
        idx += WORD_LEN_BYTES

    # The expected continuation of the PRNG output.
    b_next = int.from_bytes(
        mt_bytes[min_required - WORD_LEN_BYTES:min_required], "little"
    )

    rand = random.Random()

    # Assume first that the bytes follow a twist.
    state = prepare_state(untempered, NUM_WORDS)
    rand.setstate(state)
    if b_next == rand.getrandbits(WORD_LEN_BITS):
        # Reset the state since we consumed it in the IF check.
        rand.setstate(state)
        return rand

    # Recovery was unsuccessful.
    if first2496:
        return None

    # Brute force the state index. State index starts with 1.
    for i in range(1, NUM_WORDS + 1):
        state = prepare_state(untempered, i)
        rand.setstate(state)
        if b_next == rand.getrandbits(WORD_LEN_BITS):
            rand.setstate(state)
            return rand

    # Recovery was unsuccessful.
    return None
