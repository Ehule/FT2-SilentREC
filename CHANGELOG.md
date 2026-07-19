# Changelog

All notable changes to FT2 Tapehead Edition are documented here.

This project is under active development. Experimental features are identified clearly so that working checkpoints can be preserved before further changes are made.

## Unreleased

### Added — Fast Tracks experimental milestone

- Added independent 2× playback transports for Tracks 1–8.
- Added `Ctrl+Shift+1` through `Ctrl+Shift+8` shortcuts to toggle Fast Tracks independently for the first eight tracks.
- Added an independent scrolling pattern view for every enabled Fast Track.
- Added a compact `2X` indicator and hexadecimal private source-row readout for each enabled Fast Track.
- Added a tiny fixed playhead marker so pattern data appears to rotate past a stationary tape head.
- Added theme-safe coloring for populated Fast Track pattern data using FT2's existing emphasized-row palette color.
- Preserved stock coloring for empty pattern cells, channel headings, and inactive tracks.

### Fast Tracks behavior confirmed

- Fast Tracks share the normal FT2 master transport, pattern order, BPM, and tick timing while reading pattern rows at 2×.
- Each enabled track retains its own private source row and phase.
- Toggling tracks at different moments creates independent phase relationships.
- Disabling a Fast Track returns that track to the master pattern position.
- Up to eight independently scrolling Fast Tracks have been tested simultaneously without renderer failure.
- Pattern note entry remains functional while the independent column view is active. Newly entered data may not be visible immediately because the column is centered on its private playback row; it appears when the rotating view reaches that stored row.
- When playback is stopped, the current experimental view can appear mechanically coupled to the master edit cursor. A future composition-view option is planned to align columns while stopped.

### Global effect discovery

- Effects placed on ordinary tracks continue to execute at the master transport rate.
- Global effects placed on a Fast Track are encountered at that track's faster row-reading rate and can therefore affect the complete song more frequently.
- E6 pattern-loop behavior has been tested: placing E6 on a 2× Fast Track causes its global loop behavior to be encountered at the Fast Track rate, producing a faster rhythmic result.
- This behavior is considered musically useful and is intentionally preserved during the experimental phase.

### Current limitations

- All enabled Fast Tracks currently use a fixed 2× ratio.
- Only Tracks 1–8 can be enabled as Fast Tracks.
- Fast Tracks state and ratios are not yet stored in XM metadata.
- No global logo suspend/resume or phase-reset control is implemented yet.
- Multi-pattern behavior and conflicting global effects require broader testing.
- Fast Tracks-specific behavior is not represented in stock XM playback and will eventually require a baking/export strategy for translation to standard FT2 data.

### Planned next steps

- Add a global Fast Tracks logo control that suspends and resumes the selected Fast Tracks without erasing their phase state.
- Add a phase-reset command that aligns selected Fast Tracks to a common source position.
- Add an all-eight selection command.
- Add per-track ratios such as 1×, 1/2×, 2×, 3×, and 4× after the global state controls are stable.
- Investigate persistent Tapehead metadata while preserving ordinary XM compatibility.
- Test Linux and Windows builds from the same checkpoint.
