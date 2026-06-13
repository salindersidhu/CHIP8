def rgb_to_hex(r, g, b):
    '''Convert RGB values to a hexadecimal color string.'''
    return "#{:02X}{:02X}{:02X}".format(r, g, b)

def hex_to_rgb(hex_color):
    '''Convert a hexadecimal color string to RGB values.'''
    hex_color = hex_color.lstrip("#")
    return tuple(
        int(hex_color[i:i + 2], 16)
        for i in (0, 2, 4)
    )
