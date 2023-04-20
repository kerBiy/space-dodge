import pygame
import random


class Asteroid(pygame.sprite.Sprite):
    # Constant
    SCALE = 150

    def __init__(self, x, y):
        super().__init__()
        # Image
        self.image = pygame.transform.scale(
            pygame.image.load("assets/img/asteroid.png"),
            (self.SCALE, self.SCALE),
        )

        # Variabiles
        self.rect = self.image.get_rect()
        self.rect.update(x, y, self.SCALE, self.SCALE)
        self.radius = 65
        self.mask = pygame.mask.from_surface(self.image)


class Asteroids:
    # Constants
    SCALE = 150
    SPEED = 600

    def __init__(self):
        # Variabiles
        self.asteroid_list = []
        self.spawn_time = 0.5
        self.time = 0

    def update(self, delta_time):
        self.time += delta_time

        # Spawn an asteroid
        if self.time > self.spawn_time:

            self.asteroid_list.append(
                Asteroid(random.randint(0, 1024 - self.SCALE), -300)
            )

            # Delete an asteroids when goes offscreen
            if self.asteroid_list[0].rect.y > 500:
                self.asteroid_list.pop(0)

            self.time = 0

        # Move asteroids
        for asteroid in self.asteroid_list:
            asteroid.rect.y += delta_time * self.SPEED

    def render(self, screen):
        # Draw asteroids
        for asteroid in self.asteroid_list:
            screen.blit(asteroid.image, asteroid.rect)

    def reset(self):
        # Clear asteroids from list
        self.time = 0
        self.asteroid_list.clear()