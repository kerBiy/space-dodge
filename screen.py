import pygame
import math
import sys

from player import Player
from asteroid import Asteroids


class Screen:
    # Constants
    global WIDTH, HEIGHT, GRASS, BLACK, WHITE
    WIDTH = 1024
    HEIGHT = 640
    GRASS = 128
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self):
        # Screen
        global screen
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_icon(pygame.image.load("assets/img/icon.png"))
        pygame.display.set_caption("Space Dodge")

        # Images
        global background_tex, mountains_tex, grass_tex
        background_tex = pygame.transform.scale(
            pygame.image.load("assets/img/background.png"), (WIDTH, HEIGHT)
        )
        mountains_tex = pygame.transform.scale(
            pygame.image.load("assets/img/mountain.png"), (WIDTH, 262)
        )
        grass_tex = pygame.transform.scale(
            pygame.image.load("assets/img/grass.png"), (GRASS, GRASS)
        )

        # Fonts
        global font_150, font_69
        font_150 = pygame.font.Font("assets/font/font.otf", 150)
        font_69 = pygame.font.Font("assets/font/font.otf", 69)

        # Sounds
        global launch_sfx, lose_sfx, start_sfx, intro_sfx, gameover_sfx
        launch_sfx = pygame.mixer.Sound("assets/sound/launch.wav")
        lose_sfx = pygame.mixer.Sound("assets/sound/lose.wav")
        gameover_sfx = pygame.mixer.Sound("assets/sound/gameover.mp3")
        start_sfx = pygame.mixer.Sound("assets/sound/win.wav")
        intro_sfx = pygame.mixer.Sound("assets/sound/intro.mp3")
        pygame.mixer.music.load("assets/sound/background2.mp3")
        pygame.mixer.music.set_volume(0.05)

        # Objects
        self.start_screen = StartScreen()
        self.play_screen = PlayScreen()
        self.gameover_screen = GameOverScreen()

        # Enum :))
        global START_SCREEN, PLAY_SCREEN, GAMEOVER_SCREEN
        START_SCREEN, PLAY_SCREEN, GAMEOVER_SCREEN = 0, 1, 2

        # Variabiles
        global current_screen
        current_screen = START_SCREEN

    def update(self, delta_time):
        # Check the type of screen and updates it
        if current_screen == START_SCREEN:
            self.start_screen.update(delta_time)
        elif current_screen == PLAY_SCREEN:
            self.play_screen.update(delta_time)
        elif current_screen == GAMEOVER_SCREEN:
            self.gameover_screen.update()

    def render(self):
        # Check the type of screen and draws it
        if current_screen == START_SCREEN:
            self.start_screen.render()
        elif current_screen == PLAY_SCREEN:
            self.play_screen.render()
        elif current_screen == GAMEOVER_SCREEN:
            self.gameover_screen.render()

        pygame.display.flip()


class PlayScreen:
    def __init__(self):
        # Objects
        global player, asteroids
        player = Player()
        asteroids = Asteroids()

        self.seconds = 0
        self.minutes = 0
        self.score = 0

    def check_collision(self):
        for ast in asteroids.asteroid_list:
            if pygame.sprite.collide_circle(player, ast):
                global current_screen
                current_screen = GAMEOVER_SCREEN
                self.seconds = 0
                self.score = 0
                self.minutes = 0
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(lose_sfx)
                pygame.mixer.Sound.play(gameover_sfx)

    def update_score(self, delta_time):
        self.score += delta_time
        if self.score >= 1:
            self.seconds += 1
            self.score = 0

        if self.seconds == 60:
            self.seconds = 0
            self.minutes += 1

    def render_score(self):
        if self.seconds < 10:
            self.zero = "0"
        else:
            self.zero = ""

        self.score_white = font_69.render(
            f"SCORE: {str(self.minutes)}:{self.zero}{str(self.seconds)}", True, WHITE
        )
        self.score_black = font_69.render(
            f"SCORE: {str(self.minutes)}:{self.zero}{str(self.seconds)}", True, BLACK
        )

        screen.blit(self.score_black, (10, 5))
        screen.blit(self.score_white, (5, 0))

    def update(self, delta_time):
        self.update_score(delta_time)

        # Updates player and asteroid
        player.update(delta_time)
        asteroids.update(delta_time)

        self.check_collision()

    def render(self):
        # Render backgraound
        screen.blit(background_tex, (0, 0))
        screen.blit(mountains_tex, (0, 284))

        asteroids.render(screen)

        # Render grass
        for i in range(8):
            screen.blit(grass_tex, (i * 128, 524))

        player.render(screen)

        self.render_score()


class GameOverScreen:
    def __init__(self):
        # Strings of text
        self.gameover_white = font_150.render("GAME OVER", True, WHITE)
        self.gameover_black = font_150.render("GAME OVER", True, BLACK)

        self.press_enter_white = font_69.render("Press Enter", True, WHITE)
        self.press_enter_black = font_69.render("Press Enter", True, BLACK)

    def update(self):
        keys = pygame.key.get_pressed()
        # Resets the game and returns to the Play Screen
        if keys[pygame.K_RETURN]:
            asteroids.reset()
            player.reset()
            global current_screen
            current_screen = PLAY_SCREEN
            pygame.mixer.music.play(-1)

        # If you press esc it quits the game
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    def render(self):
        # Drawing the strings of text
        screen.blit(self.gameover_black, (210, 135))
        screen.blit(self.gameover_white, (200, 125))

        screen.blit(self.press_enter_black, (365, 305))
        screen.blit(self.press_enter_white, (360, 300))


class StartScreen:
    def __init__(self):
        # string of texts
        self.space_white = font_150.render("Space", True, WHITE)
        self.space_black = font_150.render("Space", True, BLACK)
        self.dodge_white = font_150.render("Dodge", True, WHITE)
        self.dodge_black = font_150.render("Dodge", True, BLACK)

        self.startMessage_black = font_69.render("Press enter to play", True, BLACK)
        self.startMessage_white = font_69.render("Press enter to play", True, WHITE)

        self.splashMessage_white = font_69.render("CREATED BY BALTA ALEX", True, WHITE)
        self.splashMessage_black = font_69.render("CREATED BY BALTA ALEX", True, BLACK)

        # Variables
        self.splash_timer = 0
        self.splash_sound = False
        self.entry_sound = False

    def update(self, delta_time):
        # Splash Screen animation
        if self.splash_timer < 2:
            self.splash_timer += delta_time
            if self.splash_sound == False:
                pygame.mixer.Sound.play(start_sfx)
                self.splash_sound = True

        else:
            # Play launch sound
            if self.entry_sound == False:
                pygame.mixer.music.play(-1)
                # pygame.mixer.Sound.play(launch_sfx)
                self.entry_sound = True

            keys = pygame.key.get_pressed()
            # Starts the game and goes to the Play Screen
            if keys[pygame.K_RETURN]:
                global current_screen
                current_screen = 1
                pygame.mixer.Sound.play(launch_sfx)

            # If you press esc it quits the game
            elif keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

    def render(self):
        # Render Splash Screen
        if self.splash_timer < 2:
            self.splash_screen()

        # Render Start Screen
        else:
            screen.fill(WHITE)

            screen.blit(background_tex, (0, 0))
            screen.blit(mountains_tex, (0, 284))

            for i in range(8):
                screen.blit(grass_tex, (i * 128, 524))

            self.floating_text(self.space_black, -140, 10)
            self.floating_text(self.space_white, -150)

            self.floating_text(self.dodge_black, -10, 10)
            self.floating_text(self.dodge_white, -20)

            self.plain_text(self.startMessage_black, 150, 6)
            self.plain_text(self.startMessage_white, 153)

    def splash_screen(self):
        screen.fill(WHITE)
        screen.blit(background_tex, (0, 0))

        self.plain_text(self.splashMessage_black, 0, 6)
        self.plain_text(self.splashMessage_white)

    def floating_text(self, text, height=0, amount=0):
        screen.blit(
            text,
            (
                WIDTH / 2 - text.get_width() / 2 + amount,
                HEIGHT / 2
                - text.get_height() / 2
                + math.sin(pygame.time.get_ticks() * 0.005) * 10
                + height,
            ),
        )

    def plain_text(self, text, height=0, amount=0):
        screen.blit(
            text,
            (
                WIDTH / 2 - text.get_width() / 2 + amount,
                HEIGHT / 2 + height - text.get_height() / 2 + amount,
            ),
        )
