"""
An experimental python generative art generator
"""
import random
import traceback

from typing import Tuple
from PIL import Image, ImageDraw


def random_color(rgba=True):
    """Return a random RGBA color (or RGB) if rgba=False"""

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    a = random.randint(0, 255)
    if not rgba:
        return (r, g, b)
    return (r, g, b, a)


def random_slice(image, canvas_size, fill=True, max_diameter=None, slice_size=30):
    """Generate a random slice or arc somewhere on the canvas.

    This is basically a circle but without the full 360 degree start/stop
    """

    slice_start = random.randint(0, 360)
    slice_end = slice_start + slice_size
    slice_bounds = (slice_start, slice_end)

    image = random_circle(
        image, canvas_size, fill=fill, max_diameter=max_diameter, slice_bounds=slice_bounds
    )
    return image


def random_circle(image, canvas_size, fill=False, max_diameter=None, slice_bounds=(0, 360)):
    """Generate a random circle somewhere on the canvas"""

    width, height = canvas_size

    # Bounding box top left corner
    x0 = random.randint(0, width - 10)
    y0 = random.randint(0, height - 10)

    # Bounding box bottom right corner
    if not max_diameter:
        x1 = random.randint(x0 + 1, width)
        y1 = (x1 - x0) + y0
    else:
        x1 = random.randint(x0 + 1, x0 + 1 + max_diameter)
        y1 = (x1 - x0) + y0

    bounding_box_coords = (x0, y0, x1, y1)
    color = random_color()
    start, stop = slice_bounds
    line_width = random.randint(0, 5)
    draw = ImageDraw.Draw(image)
    if fill:
        draw.pieslice(bounding_box_coords, start, stop, fill=color, width=line_width)
    else:
        draw.arc(bounding_box_coords, start, stop, fill=color, width=line_width)
    return image


def random_box(image, canvas_size, max_dimensions=None):
    """Draw a random box on the canvas.

    Start by picking any point for the top left corner in the range
    of width/height minus 1. This means the most extreme place the box
    can start is (255, 255) for a 256 x 256 pixel image.

    - The top right, then, will be (256, 255)
    - The bottom right, then, will be (256, 256)
    - The bottom left, then, will be (255, 256)

    In that moxt extreme case, the box will be a single solid pixel
    (i.e. a 1x1 box) in the bottom right corner of the canvas.

    In all other cases, the minimum height/width of a box can be 1
    """
    # Canvas width/height
    width, height = canvas_size

    # Starting point
    x0 = random.randint(0, width - 1)
    y0 = random.randint(0, height - 1)

    # Top left corner
    top_left = (x0, y0)

    # Top right corner (random width)
    top_right = (random.randint(top_left[0] + 1, width), top_left[1])

    # Bottom right corner
    bottom_right = (top_right[0], random.randint(top_right[1] + 1, height))

    # Bottom left corner
    bottom_left = (top_left[0], bottom_right[1])

    # Draw the box
    draw = ImageDraw.Draw(image)
    color = random_color()
    line_width = random.randint(0, 3)
    draw.line(top_left + top_right, fill=color, width=line_width)
    draw.line(top_right + bottom_right, fill=color, width=line_width)
    draw.line(bottom_right + bottom_left, fill=color, width=line_width)
    draw.line(bottom_left + top_left, fill=color, width=line_width)
    return image


def generate_images(num_images: int = 1, size: Tuple[int, int] = (256, 256)) -> bool:
    """Generate some images of the given size

    Args:
        size (Tuple[int, int], optional): The image's width x height. Defaults to (256, 256).

    Returns:
        bool: True if the images were successfully generated, False otherwise
    """

    try:
        output_dir = "output"
        image_mode = "RGBA"

        # R, G, B, Alpha = A/255 (e.g. 240/255 = 80% opacity)

        # Create images and save files
        for i in range(num_images):
            background_color = (255, 255, 255, 255)
            max_diameter = random.randint(10, 100)
            image = Image.new(image_mode, size, background_color)
            elements = (
                ["box" for _ in range(5)]
                + ["circle" for _ in range(20)]
                + ["slice" for _ in range(75)]
            )
            # Add 1000 random elements to the image (weighted slice > circle > box)
            for _ in range(0, 1000):
                element = random.choice(elements)
                if element == "box":
                    image = random_box(image, size)
                elif element == "circle":
                    image = random_circle(
                        image, size, fill=random.choice([True, False]), max_diameter=max_diameter
                    )
                else:
                    image = random_slice(
                        image,
                        size,
                        fill=random.choice([True, False]),
                        max_diameter=max_diameter,
                        slice_size=random.randint(0, 30),
                    )

            # Save the image
            image.save(f"{output_dir}/random_white_{i}.png")
        return True
    except Exception:  # pylint: disable=broad-except
        print(traceback.format_exc())
        return False


if __name__ == "__main__":
    image_size = (1000, 1000)
    generate_images(num_images=4, size=image_size)
