from PIL import Image

img = Image.open("in.png")
img = img.resize((img.width // 2, img.height // 2))
img.save("pp.png", optimize=True)

