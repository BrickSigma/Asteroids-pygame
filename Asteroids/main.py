import pygame
import sys
import random
from pygame.locals import *

from assets.shapes import *
from assets.sprites import *
from assets.scenes import *

pygame.font.init()

# Colors
BLACK = (0, 0, 0)

class Asteroids_Game:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 650, 650
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Asteroids")
        pygame.mouse.set_visible(False)
        pygame.display.set_icon(pygame.image.load("assets/images/icon.png"))

        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.canvas = pygame.Surface((self.WIDTH, self.HEIGHT))

        self.player = Player(self.WIDTH, self.HEIGHT)
        self.bullets = Bullets(self.WIDTH, self.HEIGHT)
        self.asteroids = Asteroids(self.WIDTH, self.HEIGHT).next_round()
        self.menu = Menu()
        self.game_over = Game_over(self.canvas)
        self.pause = Pause(self.canvas)

        self.fire = False
        self.move = False
        self.score = 0

        self.shake = False
        self.shake_timer = 0

    def reset_game(self):
        self.player = Player(self.WIDTH, self.HEIGHT)
        self.bullets = Bullets(self.WIDTH, self.HEIGHT)
        self.asteroids = Asteroids(self.WIDTH, self.HEIGHT).next_round()
        self.fire = False
        self.score = 0

    def draw(self):
        roll = [0, 0]
        if self.shake:
            self.shake_timer = 15
        if self.shake_timer:
            self.shake_timer -= 1
            roll = [random.randint(-2, 2), random.randint(-2, 2)]

        self.canvas.fill(BLACK)
        self.player.draw(self.canvas)
        self.bullets.draw(self.canvas)
        self.asteroids.draw(self.canvas)

        text = FONT_2.render(str(self.score), True, (255, 255, 255))
        self.canvas.blit(text, (78-(text.get_rect().width//2), 10))

        self.WIN.blit(self.canvas, (roll[0], roll[1]))
        pygame.display.update()

    def main(self):        
        run = True
        while run:
            if self.menu.menu:
                self.menu.loop(self.WIN)
            elif self.game_over.game_over and not self.player.dead:
                reset = self.game_over.loop(self.WIN, self.score, self.menu)
                if reset:
                    self.reset_game()
            else:
                if not len(self.asteroids.asteroids):
                    self.asteroids.asteroid_no += 1
                    if self.asteroids.asteroid_no > 6: 
                        self.asteroids.asteroid_no = 6
                    self.asteroids.next_round()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.move = True
                        if event.key == pygame.K_SPACE:
                            self.fire = True
                        if event.key == K_p: 
                            CLICK_SOUND.play()
                            reset = self.pause.loop(self.WIN, self.canvas, self.menu, self.clock, self.FPS)
                            if reset:
                                self.reset_game()
                    if event.type == KEYUP:
                        if event.key == K_SPACE: self.fire = False
                        if event.key == K_UP: self.move = False

                self.shake = False
                if self.player.dead: 
                    health, end = self.player.death()
                    if end:
                        self.player = Player(self.WIDTH, self.HEIGHT)
                        self.player.health = health
                        self.player.safe = True
                        self.player.timer = 300
                else: self.player.move(self.move)
                self.score, self.shake = self.asteroids.move(self.player, self.bullets.bullets, self.score, self.game_over, self.shake)
                self.bullets.bullet_handler(self.player, self.fire)
                self.draw()

            self.clock.tick(self.FPS)

    

if __name__ == '__main__':
    Asteroids_Game().main()