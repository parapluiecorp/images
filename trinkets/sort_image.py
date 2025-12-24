import argparse
from pathlib import Path
from typing import List, Tuple, Sequence
from PIL import Image


class RadixSorter:
    """
    Generalized radix sorter for sequences of fixed-length integer tuples.
    """

    def __init__(self, max_value: int = 255):
        """
        Initialize the sorter.

        Args:
            max_value (int): Maximum value of an integer component (e.g., 255 for 8-bit channels)
        """
        self.max_value = max_value

    def sort(self, items: Sequence[Tuple[int, ...]]) -> List[Tuple[int, ...]]:
        """
        Sort a sequence of integer tuples using radix sort.

        Args:
            items (Sequence[Tuple[int, ...]]): Sequence of tuples to sort.

        Returns:
            List[Tuple[int, ...]]: Sorted list of tuples.
        """
        if not items:
            return []

        num_channels = len(items[0])
        sorted_items = list(items)

        for channel in reversed(range(num_channels)):
            buckets = [[] for _ in range(self.max_value + 1)]
            for item in sorted_items:
                buckets[item[channel]].append(item)
            sorted_items = [item for bucket in buckets for item in bucket]

        return sorted_items


def sort_image(input_path: Path, output_path: Path):
    """
    Load an image, sort its pixels using radix sort, and save the result.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input image not found: {input_path}")

    img = Image.open(input_path).convert("RGB")
    width, height = img.size
    pixels = list(img.getdata())

    sorter = RadixSorter(max_value=255)
    sorted_pixels = sorter.sort(pixels)

    sorted_img = Image.new("RGB", (width, height))
    sorted_img.putdata(sorted_pixels)
    sorted_img.save(output_path)
    print(f"Sorted image saved to: {output_path}")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Sort image pixels using radix sort.")
    parser.add_argument(
        "input",
        type=Path,
        help="Path to input image (JPEG, PNG, WebP, etc.)"
    )
    parser.add_argument(
        "output",
        type=Path,
        help="Path to save the sorted output image"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        sort_image(args.input, args.output)
    except Exception as e:
        print(f"Error: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

