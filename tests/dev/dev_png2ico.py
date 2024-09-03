import argparse
from pathlib import Path
from typing import Sequence

from PIL import Image

AUTO_RESIZE_OUTPUT_ICO_SIZES = (
    (16, 16),
    (24, 24),
    (32, 32),
    (48, 48),
    (64, 64),
    (128, 128),
    (255, 255),
)


def png2ico(pngs_paths: Sequence[str], ico_path: str, *, auto_resize: bool = False):
    if auto_resize:
        imgs = {Path(png_path).stat().st_size: png_path for png_path in pngs_paths}
        largest_img_path = imgs[max(imgs.keys())]
        img = Image.open(largest_img_path)
        img.save(ico_path, sizes=AUTO_RESIZE_OUTPUT_ICO_SIZES)
    else:
        data = bytes((0, 0, 1, 0, len(pngs_paths), 0))
        offset = 6 + len(pngs_paths) * 16

        for png_path in pngs_paths:
            img = Image.open(png_path)
            try:
                data += bytes(
                    (
                        img.width,
                        img.height,
                        0,
                        0,
                        1,
                        0,
                        32,
                        0,
                    )
                )
            except ValueError:
                raise ValueError(
                    "Image size can't be larger than 255x255 pixels. "
                    "Resize your image or use -r flag to continue."
                )
            bytesize = Path(png_path).stat().st_size
            data += bytesize.to_bytes(4, byteorder="little")
            data += offset.to_bytes(4, byteorder="little")
            offset += bytesize

        for png in pngs_paths:
            data += Path(png).read_bytes()

        Path(ico_path).write_bytes(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Converting multiple .PNG files to one multisize .ICO file"
    )
    parser.add_argument("files", nargs="+", type=str, help="Input .PNG filenames")
    parser.add_argument(
        "-o",
        "--output",
        default="icon.ico",
        type=str,
        required=False,
        help="Output .ICO filename",
    )
    parser.add_argument(
        "-r",
        "--resize",
        default=False,
        type=bool,
        action=argparse.BooleanOptionalAction,
        help="Resizes the largest .PNG file automatically. "
        "The output is multisize .ICO file with sizes: "
        "16x16, 24x24, 32x32, 48x48, 64x64, 128x128, 255x255.",
    )
    args = parser.parse_args()
    png2ico(pngs_paths=args.files, ico_path=args.output, auto_resize=args.resize)
