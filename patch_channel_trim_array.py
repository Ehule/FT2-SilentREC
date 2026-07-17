from pathlib import Path
import sys

replayer_c = Path("src/ft2_replayer.c")
replayer_h = Path("src/ft2_replayer.h")

for path in (replayer_c, replayer_h):
    if not path.exists():
        sys.exit(f"ERROR: {path} not found. Run this from the ft2-clone repository root.")

c_source = replayer_c.read_text()
h_source = replayer_h.read_text()

old_global = """channel_t channel[MAX_CHANNELS];
"""

new_global = """channel_t channel[MAX_CHANNELS];
uint16_t channelVolumeTrim[MAX_CHANNELS];
"""

old_trim_block = """\t\t// Temporary proof-of-concept: attenuate channel 1 by 50%
\t\tconst int32_t channelIndex = (int32_t)(ch - channel);
\t\tif (songPlaying && channelIndex == 0)
\t\t\tfVol *= 0.5f;

\t\t// FT2 doesn't clamp the volume, but let's do it just in case
"""

new_trim_block = """\t\t// Apply non-destructive per-channel output trim.
\t\tconst int32_t channelIndex = (int32_t)(ch - channel);
\t\tASSERT(channelIndex >= 0 && channelIndex < MAX_CHANNELS);
\t\tfVol *= channelVolumeTrim[channelIndex] * (1.0f / 256.0f);

\t\t// FT2 doesn't clamp the volume, but let's do it just in case
"""

old_header = """extern channel_t channel[MAX_CHANNELS];
"""

new_header = """extern channel_t channel[MAX_CHANNELS];
extern uint16_t channelVolumeTrim[MAX_CHANNELS];
"""

old_reset = """void resetChannels(void)
{
"""

new_reset = """void resetChannels(void)
{
\tstatic bool trimValuesInitialized = false;

\tif (!trimValuesInitialized)
\t{
\t\tfor (int32_t i = 0; i < MAX_CHANNELS; i++)
\t\t\tchannelVolumeTrim[i] = 256; // 100%

\t\ttrimValuesInitialized = true;
\t}
"""

checks = [
    (replayer_c, c_source, old_global, "global channel array"),
    (replayer_c, c_source, old_trim_block, "temporary trim block"),
    (replayer_h, h_source, old_header, "channel extern declaration"),
    (replayer_c, c_source, old_reset, "resetChannels() opening"),
]

for path, source, needle, description in checks:
    if needle not in source:
        sys.exit(f"ERROR: Could not find expected {description} in {path}.")

if new_global in c_source or new_header in h_source:
    sys.exit("Patch appears to be already applied.")

c_backup = replayer_c.with_suffix(".c.trimtest.bak")
h_backup = replayer_h.with_suffix(".h.trimtest.bak")

if not c_backup.exists():
    c_backup.write_text(c_source)
if not h_backup.exists():
    h_backup.write_text(h_source)

c_source = c_source.replace(old_global, new_global, 1)
c_source = c_source.replace(old_trim_block, new_trim_block, 1)
c_source = c_source.replace(old_reset, new_reset, 1)
h_source = h_source.replace(old_header, new_header, 1)

replayer_c.write_text(c_source)
replayer_h.write_text(h_source)

print("Applied real per-channel trim array.")
print("All channels initialize to 256 = 100%.")
print("For testing, edit one channelVolumeTrim value after initialization.")
