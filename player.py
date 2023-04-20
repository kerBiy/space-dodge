import pygame
from sprite_sheet import SpriteSheet


class Player(pygame.sprite.Sprite):
    # Constants
    WIDTH = 85
    HEIGHT = 135

    def __init__(self):
        super().__init__()
        # Variabiles
        self.rect = pygame.Rect(512 - self.WIDTH / 2, 424, self.WIDTH, self.HEIGHT)
        self.radius = 35
        self.direction = 0
        self.speed = 400

        # SpriteSheets
        self.left_sprite_sheet = SpriteSheet("assets/img/left.png")
        self.right_sprite_sheet = SpriteSheet("assets/img/right.png")

        self.left_animations = []
        self.right_animations = []

        self.image = pygame.image.load("assets/img/icon.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.WIDTH / 2, self.HEIGHT / 2)
        )

        # Animation variabiles
        self.animation_steps = 3
        self.animation_direction = 0
        self.animation_cooldown = 150
        self.frame = 0
        self.freeze = False
        self.last_update = pygame.time.get_ticks()

        # Spritesheets setup
        BLACK = (0, 0, 0)
        for i in range(self.animation_steps):
            self.left_animations.append(
                self.left_sprite_sheet.get_image(i, 17, 27, 5, BLACK)
            )

            self.right_animations.append(
                self.right_sprite_sheet.get_image(i, 17, 27, 5, BLACK)
            )

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time):
        # Set animation direction
        if self.direction != 0:
            self.animation_direction = self.direction

        self.direction = 0

        # Get input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction = -1
        elif keys[pygame.K_d]:
            self.direction = 1

        # Move the player
        if not (self.rect.x < 0 and self.direction == -1) and not (
            self.rect.x + Player.WIDTH > 1024 and self.direction == 1
        ):
            self.rect.x += self.direction * self.speed * delta_time

        # If player not moving
        if self.direction == 0:
            self.frame = 0
            self.freeze = True
        else:
            self.freeze = False

    def render(self, screen):
        # Update animation
        current_time = pygame.time.get_ticks()
        if (
            current_time - self.last_update >= self.animation_cooldown
            and not self.freeze
        ):
            self.frame += 1
            self.last_update = current_time
            if self.frame >= self.animation_steps:
                self.frame = 0

        # Render animation
        if self.animation_direction == -1:
            screen.blit(self.left_animations[self.frame], self.rect)
        else:
            screen.blit(self.right_animations[self.frame], self.rect)

    def reset(self):
        # Reset the player
        self.rect.update(512 - self.WIDTH / 2, 424, self.WIDTH, self.HEIGHT)
        self.frame = 0
        self.animation_direction = 0
        self.freeze = True
