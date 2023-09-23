import pygame


class SpriteSheet:
    def __init__(self, filename: str):
        self.filename = filename
        self.sheet = pygame.image.load(self.filename).convert_alpha()

    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width, height))
        image.set_colorkey(color)
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))

        return image
