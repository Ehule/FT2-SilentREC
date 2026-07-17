from pathlib import Path
import sys

path = Path("src/ft2_replayer.c")

if not path.exists():
    sys.exit(f"ERROR: {path} not found. Run this from the ft2-clone repository root.")

source = path.read_text()

old = """\t\t// FT2 doesn't clamp the volume, but let's do it just in case
\t\tif (fVol > 1.0f)
\t\t\tfVol = 1.0f;

\t\tch->fFinalVol = fVol;
"""

new = """\t\t// Temporary proof-of-concept: attenuate channel 1 by 50%
\t\tconst int32_t channelIndex = (int32_t)(ch - channel);
\t\tif (songPlaying && channelIndex == 0)
\t\t\tfVol *= 0.5f;

\t\t// FT2 doesn't clamp the volume, but let's do it just in case
\t\tif (fVol > 1.0f)
\t\t\tfVol = 1.0f;

\t\tch->fFinalVol = fVol;
"""

if new in source:
    sys.exit("Patch is already applied.")

if old not in source:
    sys.exit(
        "ERROR: Expected code block was not found.\n"
        "The source may differ from the version this patch expects."
    )

backup = path.with_suffix(path.suffix + ".bak")
if not backup.exists():
    backup.write_text(source)
    print(f"Backup created: {backup}")

patched = source.replace(old, new, 1)
path.write_text(patched)

print("Patched src/ft2_replayer.c")
print("Channel 1 will now be attenuated to 50% during song/pattern playback.")
print("Other channels and stopped sample auditioning should remain unchanged.")
