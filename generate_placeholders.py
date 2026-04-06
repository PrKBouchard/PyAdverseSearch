import os
from PIL import Image, ImageDraw

STATIC_IMAGES_DIR = r"C:\Users\Benjamin\PycharmProjects\PyAdverseSearch1\PyAdverseSearch\docs\_static\images"
os.makedirs(STATIC_IMAGES_DIR, exist_ok=True)

def create_placeholder(filename, text, size=(800, 600), color=(73, 109, 137)):
    img = Image.new('RGB', size, color=color)
    d = ImageDraw.Draw(img)
    # Simple centered text
    # Assuming text size and centering manually to keep it simple, without fonts
    d.text((size[0]//3, size[1]//2), text, fill=(255, 255, 255))
    img.save(os.path.join(STATIC_IMAGES_DIR, filename))

create_placeholder("schema_architecture.png", "Schéma d'Architecture PyAdverseSearch\n(Remplacer par le vrai schéma)", size=(800, 400), color=(44, 62, 80))
create_placeholder("menu.png", "Screenshot : Menu Principal\n(Remplacer par la capture)", color=(52, 73, 94))
create_placeholder("connect4.png", "Screenshot : Puissance 4\n(Remplacer par la capture)", color=(41, 128, 185))
create_placeholder("tictactoe.png", "Screenshot : Morpion (Tic Tac Toe)\n(Remplacer par la capture)", color=(192, 57, 43))
create_placeholder("reversi.png", "Screenshot : Reversi (Othello)\n(Remplacer par la capture)", color=(39, 174, 96))

print("Placeholders generated in", STATIC_IMAGES_DIR)
