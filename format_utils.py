import colorsys


def hex_to_rgb(hex_str=str):
    """
    Return (red, green, blue) for the color given as #rrggbb. Values are integers only, as they should be.
    """
    hex_str = hex_str.lstrip('#')
    len_hex = len(hex_str)
    if len_hex != 6:
        raise ValueError('Hex code must be 6 digits long.')
    return tuple(int(hex_str[i:i + len_hex // 3], 16) for i in range(0, len_hex, len_hex // 3))


def rgb_to_hex(red, green, blue):
    """
    Return color as #rrggbb for the given color values. Does not handle unbounded values (bigger than 255).
    """
    return '#%02x%02x%02x' % (abs(int(round(red))), abs(int(round(green))), abs(int(round(blue))))


def darken_color(hex_code, darkening_value):
    r, g, b = hex_to_rgb(hex_code)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    v = v * (1 - darkening_value)
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    hex_code = rgb_to_hex(r, g, b)
    return hex_code


def split_text_into_lines(text, max_line_length=32):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_line_length:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

