#!/usr/bin/env python3
"""Deterministic model tests for Fast Tracks crossed-row transport integrity."""

from dataclasses import dataclass


@dataclass
class State:
    row: int = 0
    accumulator: int = 0
    started: bool = False


def advance(state: State, numerator: int, denominator: int, tpl: int, rows: int) -> list[int]:
    """Mirror advanceFastTracksPOCTransport and return every crossed row."""
    assert numerator > 0 and denominator > 0 and tpl > 0 and rows > 0
    if not state.started:
        state.started = True
        return []

    state.accumulator += numerator
    threshold = denominator * tpl
    crossed = []
    while state.accumulator >= threshold:
        state.accumulator -= threshold
        state.row = (state.row + 1) % rows
        crossed.append(state.row)
    return crossed


def run_ticks(ratio: tuple[int, int], tpl: int, ticks: int, rows: int = 64) -> list[list[int]]:
    state = State()
    return [advance(state, *ratio, tpl, rows) for _ in range(ticks)]


def test_two_to_one_tpl_one() -> None:
    events = run_ticks((2, 1), tpl=1, ticks=5)
    assert events == [[], [1, 2], [3, 4], [5, 6], [7, 8]]


def test_five_to_one_tpl_one() -> None:
    events = run_ticks((5, 1), tpl=1, ticks=3)
    assert events == [[], [1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]


def test_five_to_one_tpl_two() -> None:
    events = run_ticks((5, 1), tpl=2, ticks=5)
    assert events == [[], [1, 2], [3, 4, 5], [6, 7], [8, 9, 10]]


def test_wrap_preserves_order() -> None:
    state = State(row=62, started=True)
    assert advance(state, 5, 1, 1, 64) == [63, 0, 1, 2, 3]


def test_restore_event_cannot_be_skipped_into_apparent_mute() -> None:
    # Concrete failure: the voice is already OFF. This tick crosses a restoring
    # note-on followed by a blank row. The old Boolean/final-row path sees only
    # the blank and leaves the channel apparently muted forever; the integrity
    # path processes the note-on before the blank and restores playback.
    pattern = {1: "ON", 2: "BLANK"}
    state = State(started=True)
    crossed = advance(state, 2, 1, 1, 64)
    assert crossed == [1, 2]

    voice_old = "OFF"
    final_event = pattern[crossed[-1]]
    if final_event == "OFF":
        voice_old = "OFF"
    elif final_event == "ON":
        voice_old = "PLAYING"

    voice_new = "OFF"
    for row in crossed:
        event = pattern[row]
        if event == "OFF":
            voice_new = "OFF"
        elif event == "ON":
            voice_new = "PLAYING"

    assert voice_old == "OFF"
    assert voice_new == "PLAYING"


def test_clutch_hidden_transport_matches_audible_transport() -> None:
    audible = State()
    hidden = State()
    for _ in range(40):
        assert advance(audible, 5, 1, 2, 64) == advance(hidden, 5, 1, 2, 64)
    assert audible == hidden


def test_ratio_change_phase_carry() -> None:
    state = State(row=7, accumulator=5, started=True)
    old_threshold = 2 * 6
    new_threshold = 1 * 6
    state.accumulator = state.accumulator * new_threshold // old_threshold
    assert state.accumulator == 2
    assert advance(state, 5, 1, 6, 64) == [8]


def main() -> None:
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in sorted(tests, key=lambda fn: fn.__name__):
        test()
        print(f"PASS {test.__name__}")
    print(f"\n{len(tests)} Fast Tracks transport tests passed.")


if __name__ == "__main__":
    main()
