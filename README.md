
# FT2-Tapehead Edition

> **Compose like a tracker. Think like a tape machine.**

**FT2-Tapehead Edition** is a workflow-focused fork of **FT2 Clone** by **8bitbubsy**, inspired by the original **FastTracker II** by Triton Productions.

It reimagines tracker composition through the lens of tape-machine recording while preserving the classic FastTracker II interface and philosophy.


The goal is not to redesign FastTracker II---it is to preserve its
speed, familiarity, and philosophy while removing repetitive actions
that interrupt creative flow.



## Features

### Silent Record

Record into patterns without hearing every newly entered note, reducing
loop fatigue during composition.

### Inherit Pattern Length (IPL)

Automatically inherit the previous pattern's length when creating new
patterns, making mixed-length song structures effortless.

### Insert New Pattern (INP)

Insert a brand-new pattern instead of duplicating the current one.

### Automatic Pattern Generation (APG / REC+)

While recording in Song Record mode, **REC+** automatically extends the
song by creating new patterns as playback reaches the end.

This transforms FT2 from a pattern editor into a tape-inspired
composition environment while preserving its classic workflow.

### Pattern Data Zap (PatData)

Erase all musical note data while preserving:

-   Pattern lengths
-   Song order
-   Pattern allocation
-   Overall song structure

Think of it as erasing the tape while leaving the reels intact.

### REC+ Interface

When APG is enabled, the normal Song Record button becomes **REC+**,
clearly indicating the enhanced recording mode.

### Hidden Easter Egg

If you genuinely fill every available pattern through REC+ recording,
FT2-Tapehead Edition rewards you with a hidden **GAME OVER** screen.

Subsequent attempts display **REC+ FULL**.

## Philosophy

Every addition in FT2-Tapehead Edition is optional.

Disable the new features and the tracker behaves like the standard
FastTracker II Clone.

Enable them, and the tracker becomes a fast, improvisational composition
tool inspired by tape-machine workflows rather than repetitive pattern
editing.

> Spend less time managing patterns and more time making music.

## Roadmap

Planned ideas include:

-   Per-channel output trim / mixer view
-   Additional tape-inspired workflow improvements
-   Optional UI quality-of-life enhancements
-   More hidden easter eggs

------------------------------------------------------------------------

FT2-Tapehead Edition is developed with respect for the original
FastTracker II workflow and the FT2 Clone project. The goal is evolution
through optional workflow enhancements---not replacing what made FT2
great.

## Building

FT2-Tapehead Edition can be built on both Linux and Windows using the included build script.

### Linux

Install the required development packages for your distribution, then run:

```bash
./make-linux.sh
```

The compiled executable will be placed in:

```text
release/other/ft2-clone
```

### Windows

FT2-Tapehead Edition uses the included Visual Studio solution for Windows builds.

1. Install **Visual Studio 2026 Community**.
2. Install the **Desktop development with C++** workload.
3. Open `vs2026_project/ft2-clone.slnx`.
4. Select the **Release** configuration.
5. Select the **x64** platform.
6. Build the solution.

If Visual Studio reports that the Windows SDK is missing, change the project to use the SDK version installed on your system.

The compiled executable will be generated in the Visual Studio output directory.

## Acknowledgements

- Original **FastTracker II** by **Triton Productions**
- **FT2 Clone** by **8bitbubsy**
- **FT2-Tapehead Edition** design, testing, and project direction by **Ehule**
- Development assistance, code-patch generation, debugging support, and documentation assistance provided with **OpenAI ChatGPT**

FT2-Tapehead Edition builds upon FT2 Clone with optional workflow enhancements focused on improvisation, continuous recording, and tape-inspired composition.
