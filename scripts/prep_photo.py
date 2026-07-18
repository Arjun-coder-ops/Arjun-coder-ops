from rembg import remove
from PIL import Image
import cv2
import numpy as np
import os
import sys


def preprocess(image_path):
    print("[1/5] Loading image...")

    image = Image.open(image_path).convert("RGBA")

    print("[2/5] Removing background...")

    no_bg = remove(image)

    # White background
    white_bg = Image.new("RGBA", no_bg.size, (255, 255, 255, 255))
    white_bg.paste(no_bg, mask=no_bg)

    rgb = white_bg.convert("RGB")

    print("[3/5] Converting to grayscale...")

    gray = cv2.cvtColor(np.array(rgb), cv2.COLOR_RGB2GRAY)

    print("[4/5] Enhancing contrast with CLAHE...")

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    print("[5/5] Saving output...")

    output_path = os.path.join(
        os.path.dirname(image_path),
        "source-prepped.png"
    )

    cv2.imwrite(output_path, enhanced)

    print("\nDone!")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:")
        print("python scripts/prep_photo.py assets/me.jpeg")
        sys.exit()

    preprocess(sys.argv[1])