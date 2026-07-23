These BMP files are converted to byte tables for use in the FT2 code.
They are then unpacked on runtime by routines in ft2_bmp.c.

If you plan to modify the graphics, you need to also update the table
length number in ft2_gfxdata.h for the corresponding graphics!
If you want to add more graphics, it's a bit more complicated. You need to
add the entry to the bmp struct list in ft2_bmp.h, then add a new line to
loadBMPs() and freeBMPs() in ft2_bmp.c.

Changing/adding graphics is not simple because stuff is quite hardcoded,
so Good Luck :-).

Please read LICENSE.txt (in this directory) if you plan on using these in
another project...

Note: The BMPs *must* be RLE compressed, at 4-bit or 8-bit only!
It's important that you don't change the palette colors in any of these
BMPs (except ft2AboutLogo.bmp which is converted to true-color internally).
Doing so will mess up the "pixel color -> FT2 palette number" conversion
when unpacking the graphics on runtime.

Tapehead Edition Fast Tracks logo:
- The external 154x128 fastTracksLogoBadges.bmp is loaded at runtime.
- Put it in a bmp directory beside the executable, or in src/gfxdata/bmp
  while developing from the repository.
- Grayscale artwork is recolored through the current FT2 theme at runtime.
- Full-color artwork is displayed unchanged.
- The old embedded logo remains available as a fallback.
