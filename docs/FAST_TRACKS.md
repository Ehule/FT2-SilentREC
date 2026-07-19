# Fast Tracks — Experimental Design and Test Notes

Fast Tracks is an experimental Tapehead Edition playback and visualization system. It allows the first eight FT2 channels to interpret one shared master transport through separate per-track row positions.

The feature does **not** create eight unrelated songs or eight independent BPM clocks. All tracks continue to share FT2's song position, pattern order, BPM, speed, and tick engine. A Fast Track instead advances through the current pattern at a different row-reading ratio.

## Current prototype

The present implementation supports:

- Tracks 1–8;
- a fixed 2× rate;
- independent activation with `Ctrl+Shift+1` through `Ctrl+Shift+8`;
- independent phase determined by the moment each track is activated;
- an independently scrolling column for each active track;
- a fixed miniature playhead marker;
- a `2X` label and hexadecimal source-row readout;
- theme-safe coloring of populated Fast Track events.

## Visual model

The pattern is treated like a rotating music-box barrel or tape loop.

The tiny arrow is the stationary read head. The pattern information moves past it. Only populated musical information is recolored, so notes, instruments, volume commands, and effects visibly travel around the barrel while empty cells remain visually quiet.

Inactive tracks retain the stock FT2 pattern presentation.

## Phase behavior

Each Fast Track has a private source-row state.

Activating Tracks 1–8 at different moments creates different phase relationships even though all active tracks currently run at 2×. This free-phase activation is musically useful and should remain available.

Disabling an individual Fast Track returns it to the shared master row. Re-enabling it begins Fast Track operation again according to the current implementation's activation behavior.

Future global controls are intended to distinguish these operations:

- **Suspend/resume:** temporarily return all selected tracks to normal presentation and playback while retaining their private Fast Tracks phase state.
- **Phase reset:** align all selected Fast Tracks to a common source position.
- **Select all:** arm or disarm the first eight tracks without erasing future per-track ratio settings.

The proposed main Fast Tracks logo behavior is:

- click: global suspend/resume while preserving phase;
- Shift+click: reset selected tracks into phase;
- Ctrl+Shift+click: select or activate all eight tracks.

These controls are design decisions and are not implemented yet.

## Editing behavior

Editing has been tested while Fast Tracks playback visualization is active.

Pattern data is still stored successfully, but the visible Fast Track column is centered around its private playback row rather than necessarily showing the master edit row. A newly entered note can therefore be hidden until the rotating column reaches it again.

When playback is stopped, the experimental independent column can appear to move with the master edit cursor, as if the stopped barrels are mechanically coupled. A future option should provide an aligned composition view while stopped and automatically switch to independent transport-centered columns during playback.

## Effect behavior

Fast Tracks currently execute the events encountered at their private source rows.

This has an important consequence for effects that influence global replay state:

- a global effect on an ordinary track is encountered at the master rate;
- a global effect on a 2× Fast Track is encountered at the Fast Track's row-reading rate;
- the global consequence still applies to the complete song.

### E6 test

E6 pattern-loop commands were tested in three configurations:

1. E6 on a normal track with Fast Tracks disabled behaved like stock FT2.
2. E6 on a normal track while another channel used Fast Tracks continued to execute at the normal rate.
3. E6 placed on an active 2× Fast Track affected the complete song while being encountered at the faster transport rate, creating a faster rhythmic loop behavior.

This behavior is currently intentional. It makes a Fast Track capable of acting as a high-rate global modulation lane rather than restricting Fast Tracks to notes alone.

Conflicting effects, multiple E6 commands, position jumps, pattern breaks, tempo commands, and multi-pattern songs require systematic testing before this behavior can be considered stable.

## Compatibility

Fast Tracks currently changes runtime interpretation and visualization without altering the standard XM pattern representation.

A stock FT2-compatible player will not reproduce Fast Tracks timing from the same pattern data. Future work must preserve Tapehead-specific state separately and provide a baking process that expands Fast Tracks behavior into ordinary XM rows and effects when stock compatibility is required.

## Regression test module

An eight-channel XM containing percussion and scale material is being used as the first Fast Tracks regression test.

Useful checks include:

- toggle each of Tracks 1–8 independently;
- activate several tracks at different moments and verify free phase;
- activate all eight and observe renderer stability;
- disable tracks and verify clean return to the master row;
- enter notes while active and verify that they appear when the private view reaches them;
- test global effects on normal and Fast Track lanes;
- test multiple patterns and unusual pattern lengths;
- compile and run the same checkpoint on Linux and Windows.

Internally, this test has acquired the accidental nickname **Proof of Contracept**: the test that ensures no unrelated behavior is born from a Fast Tracks change.
