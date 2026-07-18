from PIL import Image
from xml.sax.saxutils import escape

# Bright → Dark
RAMP = " .`:-=+*cs#%@"

# Width of ASCII output
OUTPUT_WIDTH = 100

# SVG Settings
FONT_SIZE = 9
CHAR_WIDTH = 6
LINE_HEIGHT = 10

LEFT_PADDING = 10
TOP_PADDING = 20

TEXT_COLOR = "#c9d1d9"
BACKGROUND = "#0d1117"


def resize_image(img, width):
    aspect_ratio = img.height / img.width

    # Characters are taller than they are wide
    height = int(width * aspect_ratio * 0.55)

    return img.resize((width, height))


def image_to_ascii(img):
    pixels = img.load()

    rows = []

    for y in range(img.height):

        line = ""

        for x in range(img.width):

            brightness = pixels[x, y]

            index = int(
                brightness / 255 * (len(RAMP) - 1)
            )

            line += RAMP[index]

        rows.append(line)

    return rows


def generate_svg(ascii_rows):

    width = LEFT_PADDING * 2 + OUTPUT_WIDTH * CHAR_WIDTH
    height = TOP_PADDING * 2 + len(ascii_rows) * LINE_HEIGHT

    svg = []

    svg.append(
        f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{width}"
height="{height}"
viewBox="0 0 {width} {height}">
'''
    )

    svg.append(
        f'''
<rect
width="100%"
height="100%"
fill="{BACKGROUND}"/>
'''
    )

    svg.append(
        f'''
<g
font-family="Consolas, monospace"
font-size="{FONT_SIZE}"
fill="{TEXT_COLOR}">
'''
    )

    for row_index, row in enumerate(ascii_rows):

        y = TOP_PADDING + row_index * LINE_HEIGHT

        svg.append(
            f'<text x="{LEFT_PADDING}" y="{y}">{escape(row)}</text>\n'
        )

    svg.append("</g>")
    svg.append("</svg>")

    return "".join(svg)


def main():

    img = Image.open("assets/source-prepped.png")

    img = img.convert("L")

    img = resize_image(img, OUTPUT_WIDTH)

    ascii_rows = image_to_ascii(img)

    # Debug output
    with open("data/ascii.txt", "w", encoding="utf-8") as f:

        for row in ascii_rows:

            f.write(row + "\n")

    print("ASCII saved to data/ascii.txt")

    # SVG output
    svg = generate_svg(ascii_rows)

    with open("arjun-ascii.svg", "w", encoding="utf-8") as f:

        f.write(svg)

    print("SVG generated successfully!")


if __name__ == "__main__":
    main()