import argparse
from pathlib import Path
from PIL import Image


def pixelate_image(input_path: Path, output_path: Path, block_size: int):
    """
    Pixelate an image using fixed-size blocks.

    Args:
        input_path (Path): Path to input image.
        output_path (Path): Path to save pixelated image.
        block_size (int): Pixel block size.
    """
    if block_size <= 0:
        raise ValueError("block_size must be a positive integer")

    if not input_path.exists():
        raise FileNotFoundError(f"Input image not found: {input_path}")

    with Image.open(input_path) as img:
        width, height = img.size

        # Reduce resolution
        reduced_width = max(1, width // block_size)
        reduced_height = max(1, height // block_size)

        small_img = img.resize(
            (reduced_width, reduced_height),
            resample=Image.BILINEAR
        )

        # Scale back up using nearest-neighbor
        pixelated_img = small_img.resize(
            (width, height),
            resample=Image.NEAREST
        )

        # Preserve original format if possible
        save_format = img.format
        pixelated_img.save(output_path, format=save_format)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Pixelate an image using fixed-size pixel blocks."
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Path to input image (jpg, png, webp, tiff, etc.)"
    )
    parser.add_argument(
        "output",
        type=Path,
        help="Path to output image"
    )
    parser.add_argument(
        "-b",
        "--block-size",
        type=int,
        required=True,
        help="Pixel block size (e.g. 10, 50)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        pixelate_image(
            input_path=args.input,
            output_path=args.output,
            block_size=args.block_size
        )
        print(f"Pixelated image saved to: {args.output}")
    except Exception as e:
        print(f"Error: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()


# -------------------- MANUAL LOOP DEMO --------------------
"""
import argparse
from pathlib import Path
from PIL import Image


def average_color(pixels):
    \"\"\"Compute average color for a list of pixels. Supports RGB and RGBA.\"\"\"
    num_pixels = len(pixels)
    channels = len(pixels[0])
    sums = [0] * channels
    for pixel in pixels:
        for i in range(channels):
            sums[i] += pixel[i]
    return tuple(int(s / num_pixels) for s in sums)


def pixelate_image(input_path: Path, output_path: Path, block_size: int):
    if block_size <= 0:
        raise ValueError("block_size must be a positive integer")
    if not input_path.exists():
        raise FileNotFoundError(f"Input image not found: {input_path}")

    with Image.open(input_path) as img:
        img = img.convert("RGBA")  # normalize for consistent processing
        pixels = img.load()
        width, height = img.size

        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                block_pixels = []

                # Collect pixels in the current block
                for by in range(y, min(y + block_size, height)):
                    for bx in range(x, min(x + block_size, width)):
                        block_pixels.append(pixels[bx, by])

                # Compute average color
                avg = average_color(block_pixels)

                # Write average color back to block
                for by in range(y, min(y + block_size, height)):
                    for bx in range(x, min(x + block_size, width)):
                        pixels[bx, by] = avg

        # Convert back if original image had no alpha
        if img.mode == "RGBA":
            img = img.convert("RGB")
        img.save(output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pixelate an image by averaging pixel blocks."
    )
    parser.add_argument("input", type=Path, help="Path to input image")
    parser.add_argument("output", type=Path, help="Path to output image")
    parser.add_argument(
        "-b",
        "--block-size",
        type=int,
        required=True,
        help="Pixel block size (e.g. 10, 50)"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        pixelate_image(
            input_path=args.input,
            output_path=args.output,
            block_size=args.block_size
        )
        print(f"Pixelated image saved to: {args.output}")
    except Exception as e:
        print(f"Error: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
"""

