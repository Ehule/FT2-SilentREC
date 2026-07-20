#!/usr/bin/env python3
"""Regenerate fastTracksLogoBadgesBMP[] from the editable BMP source asset."""

from __future__ import annotations

import argparse
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BMP = ROOT / "src/gfxdata/bmp/fastTracksLogoBadges.bmp"
DEFAULT_C = ROOT / "src/gfxdata/ft2_bmp_logo.c"
STOCK_BMP = ROOT / "src/gfxdata/bmp/ft2LogoBadges.bmp"
SYMBOL = "fastTracksLogoBadgesBMP"
WIDTH = 154
HEIGHT = 128


def bmp_info(data: bytes, path: Path) -> tuple[int, int, int, int, int, int]:
    if len(data) < 54 or data[:2] != b"BM":
        raise ValueError(f"{path} is not a Windows BMP file")

    pixel_offset = struct.unpack_from("<I", data, 10)[0]
    dib_size = struct.unpack_from("<I", data, 14)[0]
    if dib_size < 40:
        raise ValueError(f"unsupported BMP header size {dib_size}")

    width, height = struct.unpack_from("<ii", data, 18)
    planes, bits_per_pixel = struct.unpack_from("<HH", data, 26)
    compression = struct.unpack_from("<I", data, 30)[0]
    colors_used = struct.unpack_from("<I", data, 46)[0]

    if planes != 1:
        raise ValueError(f"expected one BMP plane, got {planes}")
    if (width, abs(height)) != (WIDTH, HEIGHT):
        raise ValueError(
            f"expected a {WIDTH}x{HEIGHT} logo sheet, got {width}x{abs(height)}"
        )

    return pixel_offset, dib_size, width, height, bits_per_pixel, compression


def read_palette(data: bytes, dib_size: int, bits_per_pixel: int) -> list[tuple[int, int, int]]:
    palette_offset = 14 + dib_size
    max_entries = 1 << bits_per_pixel
    available = max(0, (len(data) - palette_offset) // 4)
    count = min(max_entries, available)
    palette = []
    for i in range(count):
        b, g, r, _ = struct.unpack_from("<BBBB", data, palette_offset + i * 4)
        palette.append((r, g, b))
    return palette



def decode_uncompressed_4bit(
    data: bytes, pixel_offset: int, width: int, height: int
) -> list[list[int]]:
    row_stride = ((width * 4 + 31) // 32) * 4
    rows = []
    top_down = height < 0
    abs_height = abs(height)

    for out_y in range(abs_height):
        src_y = out_y if top_down else abs_height - 1 - out_y
        start = pixel_offset + src_y * row_stride
        end = start + ((width + 1) // 2)
        if end > len(data):
            raise ValueError("truncated 4-bit BMP pixel data")

        row = []
        for packed in data[start:end]:
            row.append((packed >> 4) & 0x0F)
            if len(row) < width:
                row.append(packed & 0x0F)
        rows.append(row)

    return rows

def decode_uncompressed_8bit(
    data: bytes, pixel_offset: int, width: int, height: int
) -> list[list[int]]:
    row_stride = (width + 3) & ~3
    rows = []
    top_down = height < 0
    abs_height = abs(height)
    for out_y in range(abs_height):
        src_y = out_y if top_down else abs_height - 1 - out_y
        start = pixel_offset + src_y * row_stride
        end = start + width
        if end > len(data):
            raise ValueError("truncated 8-bit BMP pixel data")
        rows.append(list(data[start:end]))
    return rows


def decode_rle8(
    data: bytes, pixel_offset: int, width: int, height: int
) -> list[list[int]]:
    abs_height = abs(height)
    rows_bottom_up = [[0] * width for _ in range(abs_height)]
    x = y = 0
    i = pixel_offset

    while i + 1 < len(data) and y < abs_height:
        count = data[i]
        value = data[i + 1]
        i += 2

        if count:
            for _ in range(count):
                if x < width:
                    rows_bottom_up[y][x] = value
                x += 1
            continue

        if value == 0:  # end of line
            x = 0
            y += 1
        elif value == 1:  # end of bitmap
            break
        elif value == 2:  # delta
            if i + 1 >= len(data):
                raise ValueError("truncated RLE8 delta")
            x += data[i]
            y += data[i + 1]
            i += 2
        else:  # absolute run
            run = value
            if i + run > len(data):
                raise ValueError("truncated RLE8 absolute run")
            for j in range(run):
                if x < width and y < abs_height:
                    rows_bottom_up[y][x] = data[i + j]
                x += 1
            i += run
            if run & 1:
                i += 1

    if height < 0:
        return rows_bottom_up
    return list(reversed(rows_bottom_up))


def decode_editable_bmp(data: bytes, path: Path) -> tuple[list[list[int]], list[tuple[int, int, int]]]:
    pixel_offset, dib_size, width, height, bpp, compression = bmp_info(data, path)
    palette = read_palette(data, dib_size, bpp)

    if bpp == 4 and compression == 0:
        indices = decode_uncompressed_4bit(data, pixel_offset, width, height)
    elif bpp == 8 and compression == 0:
        indices = decode_uncompressed_8bit(data, pixel_offset, width, height)
    elif bpp == 8 and compression == 1:
        indices = decode_rle8(data, pixel_offset, width, height)
    else:
        raise ValueError(
            "editable BMP must be 4-bit or 8-bit indexed "
            "(uncompressed, or BI_RLE8 for 8-bit); "
            f"got {bpp}-bit compression type {compression}"
        )

    return indices, palette


def canonical_palette() -> list[tuple[int, int, int]]:
    data = STOCK_BMP.read_bytes()
    _, dib_size, _, _, bpp, _ = bmp_info(data, STOCK_BMP)
    palette = read_palette(data, dib_size, bpp)
    if len(palette) < 8:
        raise ValueError(f"{STOCK_BMP} does not contain the expected eight palette entries")
    return palette[:8]


def remap_to_canonical(
    indices: list[list[int]],
    source_palette: list[tuple[int, int, int]],
    target_palette: list[tuple[int, int, int]],
) -> list[list[int]]:
    color_to_target = {rgb: i for i, rgb in enumerate(target_palette)}
    remap: dict[int, int] = {}

    for row in indices:
        for source_index in row:
            if source_index in remap:
                continue
            if source_index >= len(source_palette):
                raise ValueError(f"pixel uses missing palette index {source_index}")
            rgb = source_palette[source_index]
            if rgb not in color_to_target:
                raise ValueError(
                    f"image uses non-FT2 palette color {rgb} at palette index {source_index}; "
                    "disable antialiasing and use only the original eight logo colors"
                )
            remap[source_index] = color_to_target[rgb]

    return [[remap[index] for index in row] for row in indices]


def encode_rle4_bmp(indices: list[list[int]], palette: list[tuple[int, int, int]]) -> bytes:
    encoded = bytearray()

    for row in reversed(indices):
        encoded.extend((0, WIDTH))  # absolute-mode scanline
        packed = bytearray()
        for x in range(0, WIDTH, 2):
            hi = row[x] & 0x0F
            lo = row[x + 1] & 0x0F if x + 1 < WIDTH else 0
            packed.append((hi << 4) | lo)
        encoded.extend(packed)
        if len(packed) & 1:
            encoded.append(0)
        encoded.extend((0, 0))  # end of line

    encoded.extend((0, 1))  # end of bitmap

    palette_entries = 8
    pixel_offset = 14 + 40 + palette_entries * 4
    file_size = pixel_offset + len(encoded)

    header = struct.pack("<2sIHHI", b"BM", file_size, 0, 0, pixel_offset)
    dib = struct.pack(
        "<IiiHHIIiiII",
        40, WIDTH, HEIGHT, 1, 4, 2, len(encoded),
        2834, 2834, palette_entries, palette_entries,
    )
    palette_bytes = bytearray()
    for r, g, b in palette:
        palette_bytes.extend((b, g, r, 0))

    return header + dib + palette_bytes + encoded


def normalize_bmp(data: bytes, path: Path) -> tuple[bytes, bool]:
    _, _, _, _, bpp, compression = bmp_info(data, path)
    if bpp == 4 and compression == 2:
        return data, False

    indices, source_palette = decode_editable_bmp(data, path)
    target_palette = canonical_palette()
    remapped = remap_to_canonical(indices, source_palette, target_palette)
    return encode_rle4_bmp(remapped, target_palette), True


def format_array(data: bytes) -> str:
    lines = []
    for offset in range(0, len(data), 24):
        chunk = data[offset : offset + 24]
        lines.append("\t" + ",".join(f"0x{byte:02X}" for byte in chunk) + ",")

    return (
        f"const uint8_t {SYMBOL}[{len(data)}] =\n"
        "{\n"
        + "\n".join(lines)
        + "\n};"
    )


def update_array(c_path: Path, replacement: str) -> bool:
    text = c_path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"const uint8_t {re.escape(SYMBOL)}\[\d+\] =\s*\n"
        rf"\{{.*?\n\}};",
        re.DOTALL,
    )

    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise ValueError(
            f"expected exactly one {SYMBOL} array in {c_path}, found {len(matches)}"
        )

    updated = pattern.sub(replacement, text, count=1)
    if updated == text:
        return False

    c_path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize and embed the editable Fast Tracks logo BMP."
    )
    parser.add_argument("--bmp", type=Path, default=DEFAULT_BMP)
    parser.add_argument("--output", type=Path, default=DEFAULT_C)
    args = parser.parse_args()

    try:
        source_data = args.bmp.read_bytes()
        embedded_data, converted = normalize_bmp(source_data, args.bmp)
        if converted:
            args.bmp.write_bytes(embedded_data)
            print(f"Converted {args.bmp} to canonical 4-bit BI_RLE4 format.")
        changed = update_array(args.output, format_array(embedded_data))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if changed:
        print(f"Updated {args.output} from {args.bmp} ({len(embedded_data)} bytes).")
    else:
        print(f"No change: {args.output} already matches {args.bmp}.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
