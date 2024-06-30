from pygame.mixer import Sound
from pygame.font import Font
from pygame.image import load


def load_sound(path, volume=0.5):
    sound = Sound(path)
    sound.set_volume(volume)
    return sound


def load_font(path, size=32):
    font = Font(path, size)
    return font


def load_image(path):
    image = load(path)
    return image
