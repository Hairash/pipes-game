from PIL import Image
im = Image.open(r'images/pipes_full.png')

# Size of the image in pixels (size of orginal image)
# (This is not mandatory)
width, height = im.size
cell_size = 64

for y in range(height // cell_size):
    for x in range(width // cell_size):
        left = x * cell_size
        right = (x + 1) * cell_size
        top = y * cell_size
        bottom = (y + 1) * cell_size

        im1 = im.crop((left, top, right, bottom))
        im1.save(f'{y}_{x}.png')
