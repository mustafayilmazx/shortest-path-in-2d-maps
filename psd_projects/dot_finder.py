from PIL import Image

def find_black_dot(image_path):
    # Open the image file
    img = Image.open(image_path).convert('RGB')

    # Get the size of the image
    width, height = img.size

    # Initialize a list to hold the coordinates of the black dots
    black_dots = []

    # Loop over the image pixels
    for y in range(height):
        for x in range(width):
            # Get the RGB values of the pixel
            r, g, b = img.getpixel((x, y))

            # If the pixel is black, add its coordinates to the list
            if r == 0 and g == 0 and b == 0:
                # black_dots.append((x, y))
                # break
                return x, y
            
    return black_dots

# Usage
# black_dots = find_black_dot('ev.png')
# print(black_dots)