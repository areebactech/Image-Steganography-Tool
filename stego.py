from PIL import Image
import os

# ------------------ Helper Functions ------------------

def message_to_binary(message: str) -> str:
    """Convert text message to binary string"""
    return ''.join(format(ord(c), '08b') for c in message)

def binary_to_message(binary: str) -> str:
    """Convert binary string back to text"""
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)

# ------------------ Core Functions ------------------

def hide_message(image_path: str, output_path: str, message: str) -> str:
    """Hide a text message in an image using LSB steganography"""
    if not os.path.exists(image_path):
        return "Error: Input image not found!"

    try:
        img = Image.open(image_path)
        if img.mode not in ['RGB', 'RGBA']:
            img = img.convert('RGBA')
    except Exception as e:
        return f"Error: Cannot open image! ({e})"

    # Ensure output path ends with .png
    if not output_path.lower().endswith(".png"):
        output_path += ".png"

    binary_msg = message_to_binary(message) + "1111111111111110"  # delimiter
    total_bits = len(binary_msg)

    if img.width * img.height * 3 < total_bits:
        return "Error: Image too small to hide this message!"

    pixels = img.load()
    data_index = 0

    # Highlight image: only changed pixels will be red
    highlight_img = img.copy()
    highlight_pixels = highlight_img.load()

    for y in range(img.height):
        for x in range(img.width):
            if data_index >= total_bits:
                img.save(output_path)
                # avoid overwriting highlight image if it exists
                highlight_path = f"highlight_{os.path.basename(output_path)}"
                highlight_img.save(highlight_path)
                return f"Message hidden successfully!\nSaved as: {output_path}\nHighlighted pixels: {highlight_path}"

            r, g, b, *rest = pixels[x, y]  # works for RGB or RGBA
            a = rest[0] if rest else 255
            orig_pixel = (r, g, b, a)

            # Hide bits in RGB channels
            r = (r & ~1) | int(binary_msg[data_index]); data_index += 1
            if data_index < total_bits:
                g = (g & ~1) | int(binary_msg[data_index]); data_index += 1
            if data_index < total_bits:
                b = (b & ~1) | int(binary_msg[data_index]); data_index += 1

            pixels[x, y] = (r, g, b, a)

            # Highlight changed pixels in red
            highlight_pixels[x, y] = (255, 0, 0, a) if (r, g, b, a) != orig_pixel else (r, g, b, a)

    img.save(output_path)
    highlight_img.save(f"highlight_{os.path.basename(output_path)}")
    return f"Message hidden successfully!\nSaved as: {output_path}\nHighlighted pixels: highlight_{os.path.basename(output_path)}"

def extract_message(image_path: str) -> str:
    """Extract hidden message from an image"""
    if not os.path.exists(image_path):
        return "Error: Image not found!"

    try:
        img = Image.open(image_path)
        if img.mode not in ['RGB', 'RGBA']:
            img = img.convert('RGBA')
    except Exception as e:
        return f"Error: Cannot open image! ({e})"

    pixels = img.load()
    binary_data = ""
    delimiter = "1111111111111110"

    for y in range(img.height):
        for x in range(img.width):
            r, g, b, *rest = pixels[x, y]
            for color in (r, g, b):
                binary_data += str(color & 1)
                if binary_data.endswith(delimiter):
                    message_binary = binary_data[:-len(delimiter)]
                    return "Hidden message: " + binary_to_message(message_binary)

    return "No hidden message found!"
