import argparse
from PIL import Image
import sys

def process_image(mode, input_path, output_path, key=None, decrypt=False):
    """
    Encrypt or decrypt an image using pixel manipulation.
    """
    # Load the image
    try:
        img = Image.open(input_path)
    except FileNotFoundError:
        print(f"Error: Input image '{input_path}' not found.")
        sys.exit(1)

    # Ensure the image is in RGB or RGBA mode
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGBA')

    # Get pixel data as a list of tuples
    pixels = list(img.getdata())
    new_pixels = []

    if mode == 'xor':
        if key is None:
            print("Error: --key is required for xor mode")
            sys.exit(1)
        # XOR is symmetric; decrypt flag does not change behaviour
        for pixel in pixels:
            # Apply XOR to each channel
            new_pixel = tuple((ch ^ key) for ch in pixel)
            new_pixels.append(new_pixel)

    elif mode == 'add':
        if key is None:
            print("Error: --key is required for add mode")
            sys.exit(1)
        # For decryption we subtract, otherwise add
        shift = -key if decrypt else key
        for pixel in pixels:
            new_pixel = tuple((ch + shift) % 256 for ch in pixel)
            new_pixels.append(new_pixel)

    elif mode == 'swap':
        # Swap Red and Blue channels (RGB <-> BGR)
        # For RGBA we swap R and B, keep A unchanged
        for pixel in pixels:
            if len(pixel) == 3:  # RGB
                new_pixel = (pixel[2], pixel[1], pixel[0])
            else:                # RGBA
                new_pixel = (pixel[2], pixel[1], pixel[0], pixel[3])
            new_pixels.append(new_pixel)

    else:
        print(f"Unsupported mode: {mode}. Use 'xor', 'add', or 'swap'.")
        sys.exit(1)

    # Create a new image and save
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    new_img.save(output_path)
    print(f"Success! Output saved to '{output_path}'")


def main():
    parser = argparse.ArgumentParser(
        description="Simple image encryption/decryption using pixel manipulation."
    )
    parser.add_argument("mode", choices=['xor', 'add', 'swap'],
                        help="Encryption method")
    parser.add_argument("input_image", help="Path to input image")
    parser.add_argument("output_image", help="Path to save output image")
    parser.add_argument("-k", "--key", type=int, default=None,
                        help="Key (0-255) for xor/add modes")
    parser.add_argument("-d", "--decrypt", action="store_true",
                        help="Perform decryption (for 'add' mode; ignored for 'xor' and 'swap')")

    args = parser.parse_args()

    # Validate key range
    if args.key is not None and not (0 <= args.key <= 255):
        print("Error: Key must be between 0 and 255.")
        sys.exit(1)

    process_image(args.mode, args.input_image, args.output_image,
                  args.key, args.decrypt)


if __name__ == "__main__":
    main()
