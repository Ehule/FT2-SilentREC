from pathlib import Path
import sys

path = Path("src/ft2_replayer.c")
source = path.read_text()

old = """\t\tfor (int32_t i = 0; i < MAX_CHANNELS; i++)
\t\t\tchannelVolumeTrim[i] = 256; // 100%

\t\ttrimValuesInitialized = true;
"""

new = """\t\tfor (int32_t i = 0; i < MAX_CHANNELS; i++)
\t\t\tchannelVolumeTrim[i] = 256; // 100%

\t\tchannelVolumeTrim[0] = 128; // temporary test: channel 1 at 50%
\t\ttrimValuesInitialized = true;
"""

if new in source:
    sys.exit("Test value is already applied.")

if old not in source:
    sys.exit("ERROR: Could not find trim initialization block.")

path.write_text(source.replace(old, new, 1))
print("Set channel 1 trim to 128 = 50% for testing.")
