import pygame
from pygame.locals import *
import sys
import random

from assets.interface import Button
from assets.shapes import Polygon

pygame.font.init()
pygame.mixer.init()

FONT_1 = pygame.font.Font("assets/fonts/rexlia rg.otf", 50)  # 60 pts high
FONT_2 = pygame.font.Font("assets/fonts/rexlia rg.otf", 30)  # 36 pts high

MOUSE = pygame.image.load("assets/images/mouse.png")
MOUSE.set_colorkey((0, 0, 0))

CLICK_SOUND = pygame.mixer.Sound("assets/sounds/click.wav")
CLICK_SOUND.set_volume(0.25)

class Menu:
    def __init__(self):
        self.TITLE = FONT_1.render("ASTEROIDS", True, (255, 255, 255))
        self.PLAY_TEXT = FONT_2.render("PLAY", True, (255, 255, 255))
        self.QUIT_TEXT = FONT_2.render("QUIT", True, (255, 255, 255))

        self.PLAY_BUTTON = Button(self.PLAY_TEXT, self.PLAY_TEXT, (40, 110))
        self.QUIT_BUTTON = Button(self.QUIT_TEXT, self.QUIT_TEXT, (40, 166))

        self.menu = True

        self.ASTEROID_SHAPES = [
                [[23, 0],
                [72, 12],
                [79, 46],
                [64, 71],
                [25, 79],
                [0, 51],
                [0, 18]],

                [[25, 0],
                [79, 24],
                [79, 54],
                [46, 79],
                [2, 61],
                [0, 19]],

                [[25, 2],
                [66, 0],
                [79, 38],
                [67, 63],
                [38, 79],
                [14, 69],
                [0, 20]]
        ]

        self.asteroids = [Polygon(self.ASTEROID_SHAPES[0]).enlarge(2).move_to((624, 624)),
                        Polygon(self.ASTEROID_SHAPES[1]).enlarge(2).move_to((635, 490)),
                        Polygon(self.ASTEROID_SHAPES[1]).enlarge(2).move_to((475, 630)),
                        Polygon(self.ASTEROID_SHAPES[2]).enlarge(1).move_to((370, 637)),
                        Polygon(self.ASTEROID_SHAPES[2]).enlarge(1).move_to((642, 383)),
                        Polygon(self.ASTEROID_SHAPES[2]).enlarge(1).move_to((540, 550)),
                        Polygon(self.ASTEROID_SHAPES[0]).enlarge(0.75).move_to((641, 320)),
                        Polygon(self.ASTEROID_SHAPES[0]).enlarge(0.75).move_to((311, 634)),
                        Polygon(self.ASTEROID_SHAPES[0]).enlarge(0.4).move_to((562, 340)),
                        Polygon(self.ASTEROID_SHAPES[1]).enlarge(0.5).move_to((519, 456)),
                        Polygon(self.ASTEROID_SHAPES[2]).enlarge(0.6).move_to((380, 542)),
        ]

        self.particles = []
        self.DECAY = 0.8
        self.counters = [0, 0, 0]
        self.timers = [random.randint(90, 150), random.randint(90, 150), random.randint(90, 150)]

    def spawn_particles(self, coord):
        number = random.randint(4, 6)
        x_vels = []
        y_vels = []
        for i in range (number):
            x_vel = random.uniform(-1.5, 1.5)
            while (x_vel in x_vels) or -0.1 < x_vel < 0.1: 
                x_vel = random.uniform(-1.5, 1.5)
            x_vels.append(x_vel)
            
            y_vel = random.uniform(-1.5, 1.5)
            while (y_vel in y_vels) or -0.1 < y_vel < 0.1: 
                y_vel = random.uniform(-1.5, 1.5)
            y_vels.append(y_vels)
            
            timer = random.randint(45, 60)
            
            self.particles.append([coord[:], x_vel, y_vel, timer])

    def handle_particles(self):
        for index, particle in reversed(list(enumerate(self.particles))):
            particle[0][0] += particle[1]
            particle[0][1] += particle[2]
            particle[3] -= self.DECAY 
            if particle[3] <= 0: 
                self.particles.pop(index)

    def loop(self, surface):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if self.PLAY_BUTTON.execute():
                    CLICK_SOUND.play()
                    self.menu = False
                if self.QUIT_BUTTON.execute():
                    pygame.quit()
                    sys.exit()

        for i in range(len(self.counters)):
            self.counters[i] += 1
            if self.counters[i] >= self.timers[i]:
                self.spawn_particles([random.randint(350, 610), random.randint(350, 610)])
                self.counters[i] = 0
                self.timers[i] = random.randint(90, 150)

        self.handle_particles()

        surface.fill((0, 0, 0))
        surface.blit(self.TITLE, (40, 30))
        self.PLAY_BUTTON.draw(surface)
        self.QUIT_BUTTON.draw(surface)
        for asteroid in self.asteroids:
            asteroid.draw(surface, (255, 255, 255), 2)
        for particle in self.particles:
            pygame.draw.circle(surface, (255, 255, 255), particle[0], 2)
        surface.blit(MOUSE, pygame.mouse.get_pos())
        pygame.display.update()

class Game_over:
    def __init__(self, surface):
        self.GAME_OVER_TEXT = FONT_1.render("GAME  OVER", True, (255, 255, 255))
        self.RETRY_TEXT = FONT_2.render("RETRY", True, (255, 255, 255))
        self.MENU_TEXT = FONT_2.render("MENU", True, (255, 255, 255))
        self.QUIT_TEXT = FONT_2.render("QUIT", True, (255, 255, 255))

        self.RETRY_BUTTON = Button(self.RETRY_TEXT, self.RETRY_TEXT, (surface.get_width()//2-self.RETRY_TEXT.get_width()//2, surface.get_height()//2))
        self.MENU_BUTTON = Button(self.MENU_TEXT, self.MENU_TEXT, (surface.get_width()//2-self.MENU_TEXT.get_width()//2, surface.get_height()//2+55))
        self.QUIT_BUTTON = Button(self.QUIT_TEXT, self.QUIT_TEXT, (surface.get_width()//2-self.QUIT_TEXT.get_width()//2, surface.get_height()//2+110))

        self.game_over = False
        self.play = False
        self.GAME_OVER_SOUND = pygame.mixer.Sound("assets/sounds/game over.wav")

    def loop(self, surface, score, menu):
        if not self.play:
            self.play = True
            self.GAME_OVER_SOUND.play()
        reset = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if self.RETRY_BUTTON.execute():
                    CLICK_SOUND.play()
                    reset = True
                    self.game_over = False
                    self.play = False
                if self.QUIT_BUTTON.execute():
                    pygame.quit()
                    sys.exit()
                if self.MENU_BUTTON.execute():
                    CLICK_SOUND.play()
                    menu.menu = True
                    reset = True
                    self.game_over = False
                    self.play = False

        score_text = FONT_2.render(f"SCORE: {score}", True, (255, 255, 255))

        surface.fill((0, 0, 0))
        surface.blit(self.GAME_OVER_TEXT, (surface.get_width()//2-self.GAME_OVER_TEXT.get_width()//2, surface.get_height()//4))
        surface.blit(score_text, (surface.get_width()//2-score_text.get_width()//2, surface.get_height()//2-55))
        self.RETRY_BUTTON.draw(surface)
        self.MENU_BUTTON.draw(surface)
        self.QUIT_BUTTON.draw(surface)
        surface.blit(MOUSE, pygame.mouse.get_pos())
        pygame.display.update()

        return reset

class Pause:
    def __init__(self, surface):
        self.PAUSED_TEXT = FONT_1.render("PAUSED", True, (255, 255, 255))
        self.PLAY_TEXT = FONT_2.render("PLAY", True, (255, 255, 255))
        self.EXIT_TEXT = FONT_2.render("EXIT", True, (255, 255, 255))

        self.PLAY_BUTTON = Button(self.PLAY_TEXT, self.PLAY_TEXT, (surface.get_width()//2-self.PLAY_TEXT.get_width()//2, surface.get_height()//2-55))
        self.EXIT_BUTTON = Button(self.EXIT_TEXT, self.EXIT_TEXT, (surface.get_width()//2-self.EXIT_TEXT.get_width()//2, surface.get_height()//2))

    def loop(self, window, surface, menu, clock, fps):
        reset = False
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        CLICK_SOUND.play()
                        return reset
                if event.type == MOUSEBUTTONDOWN:
                    if self.PLAY_BUTTON.execute():
                        CLICK_SOUND.play()
                        return
                    if self.EXIT_BUTTON.execute():
                        CLICK_SOUND.play()
                        menu.menu = True
                        reset = True
                        return reset

            window.blit(surface, (0, 0))
            window.blit(self.PAUSED_TEXT, (surface.get_width()//2-self.PAUSED_TEXT.get_width()//2, window.get_height()//4))
            self.PLAY_BUTTON.draw(window)
            self.EXIT_BUTTON.draw(window)
            window.blit(MOUSE, pygame.mouse.get_pos())
            pygame.display.update()

            clock.tick(fps)