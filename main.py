import pygame
import sys

from screen import Screen

# Constants
FPS = 60


def main():
    # Objects
    pygame.init()
    screen = Screen()

    # Variabiles
    clock = pygame.time.Clock()
    previous_time = pygame.time.get_ticks()

    # Main Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Set Delta Time
        present_time = pygame.time.get_ticks()
        delta_time = (present_time - previous_time) / 1000
        previous_time = present_time

        # Update and Render the Screen
        screen.update(delta_time)
        screen.render()

        # Get constant FPS
        clock.tick(FPS)


if __name__ == "__main__":
    main()
