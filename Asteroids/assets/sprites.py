from numpy import angle
import pygame
from pygame.locals import *

from math import cos, sin, radians
import random

from assets.shapes import *

pygame.mixer.init()

class Player:
    def __init__(self, width, height):
        self.width, self.height = width, height

        self.center = list(coords_to_rect([[width/2, height/2-50], [width/2-25, height/2+20], [width/2+25, height/2+20]]).center)
        self.body = [
            Line([[width/2, height/2-50], [width/2-25, height/2+20]]).enlarge(0.6, self.center),  # Left line
            Line([[width/2, height/2-50], [width/2+25, height/2+20]]).enlarge(0.6, self.center),  # Right line
            Line([[width/2-20, height/2+4], [width/2+20, height/2+4]]).enlarge(0.6, self.center)  # Center line
        ]
        self.top = enlarge_coord([width/2, height/2-50], 0.6, self.center)

        self.angle = 0
        self.ROTATION = 4

        self.VEL = 5
        self.vector = [0, 0]
        self.max_vel = [0, 0]
        self.direction = [1, 1]

        self.safe = False
        self.timer = 0
        self.visible = True

        self.health = 3
        self.HEALTH_IMG = pygame.image.load("assets/images/health bar.png")
        self.HEALTH_IMG.set_colorkey((0, 0, 0))
        self.dead = False
        self.death_timer = 180
        self.movements = [[-0.5, -0.5], [0.5, -0.5], [0, 0.5]]

    def death(self):
        if self.death_timer == 180:
            self.angles = [random.choice([-3, 3]), random.choice([-3, 3]), random.choice([-3, 3])]
        for i, line in enumerate(self.body):
            line.move(self.movements[i][0], self.movements[i][1])
            line.rotate(self.angles[i])
        self.death_timer -= 1
        if not self.death_timer:
            self.dead = False
            self.death_timer = 180
            return self.health, True
        return self.health, False
    
    def move(self, move):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.angle -= self.ROTATION
            if self.angle < 0:
                self.angle += 360
            for line in self.body: line.rotate(-self.ROTATION, self.center)
            self.top = rotate_coord(self.top, -self.ROTATION, self.center)
        if keys[K_RIGHT]:
            self.angle += self.ROTATION
            if self.angle >= 360:
                self.angle -= 360
            for line in self.body: line.rotate(self.ROTATION, self.center)
            self.top = rotate_coord(self.top, self.ROTATION, self.center)
        
        self.max_vel = [self.VEL*sin(radians(self.angle)), -self.VEL*cos(radians(self.angle))]
        self.direction[0] = 1 if (0 < self.angle < 180) else -1
        self.direction[1] = 1 if (90 < self.angle < 270) else -1
        
        if move:
            self.vector[0] += self.max_vel[0]*0.02
            self.vector[1] += self.max_vel[1]*0.02
            if (self.vector[0] > self.max_vel[0] and self.direction[0] > 0) or (self.vector[0] < self.max_vel[0] and self.direction[0] < 0):
                self.vector[0] = self.max_vel[0]
            if (self.vector[1] > self.max_vel[1] and self.direction[1] > 0) or (self.vector[1] < self.max_vel[1] and self.direction[1] < 0):
                self.vector[1] = self.max_vel[1]
        else:
            self.vector[0] -= self.max_vel[0]*0.005
            self.vector[1] -= self.max_vel[1]*0.005
            if (self.vector[0] < 0 and self.direction[0] > 0) or (self.vector[0] > 0 and self.direction[0] < 0):
                self.vector[0] = 0
            if (self.vector[1] < 0 and self.direction[1] > 0) or (self.vector[1] > 0 and self.direction[1] < 0):
                self.vector[1] = 0
        
        for line in self.body:
            line.move(self.vector[0], self.vector[1])
        self.top = [self.top[0]+self.vector[0], self.top[1]+self.vector[1]]
        self.center = [self.center[0]+self.vector[0], self.center[1]+self.vector[1]]

        center = self.center[:]
        if self.center[0] > self.width + 31:
            self.center[0] = -31
        elif self.center[0] < -31:
            self.center[0] = self.width+31

        if self.center[1] > self.height+43:
            self.center[1] = -43
        elif self.center[1] < -43:
            self.center[1] = self.height+43

        vector = [self.center[0]-center[0], self.center[1]-center[1]]
        for line in self.body:
            line.move(vector[0], vector[1])
        self.top = [self.top[0]+vector[0], self.top[1]+vector[1]]
        
        if self.safe:
            self.timer -= 1
            self.safe = bool(self.timer)

    def draw(self, surface):
        if self.safe and not self.dead and not self.timer%25:
            self.visible = not(self.visible)
        if self.visible:
            for line in self.body:
                line.aadraw(surface, (255, 255, 255))

        for i in range(self.health):
            surface.blit(self.HEALTH_IMG, (30 + 35*(i), 50))

class Bullets:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.bullets = []
        self.VEL = 11
        self.key_pressed = False
        self.FIRE_SOUND = pygame.mixer.Sound("assets/sounds/fire.wav")
        self.FIRE_SOUND.set_volume(0.25)

    def bullet_handler(self, player, fire):
        for index, bullet in reversed(list(enumerate(self.bullets))):
            bullet[0].x += bullet[1]
            bullet[0].y += bullet[2]
            if not (0 < bullet[0].x < self.width) or not (0 < bullet[0].y < self.height):
                self.bullets.pop(index)

        if fire and not self.key_pressed and not player.dead:
            self.FIRE_SOUND.play()
            self.bullets.append([Circle(player.top, 2.5), self.VEL*sin(radians(player.angle)), -self.VEL*cos(radians(player.angle))])
            self.key_pressed = True
        elif not fire:
            self.key_pressed = False

    def draw(self, surface):
        for bullet in self.bullets:
            bullet[0].draw(surface, (255, 255, 255))


class Asteroids:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.asteroids = []
        self.spawn_range = [
            [0, width//3, 0, height//3], 
            [width//3, int(width*(2/3)), 0, height//3], 
            [int(width*(2/3)), width, 0, height//3], 
            [0, width//3, height//3, int(height*(2/3))], 
            [int(width*(2/3)), width, height//3, int(height*(2/3))], 
            [0, width//3, int(height*(2/3)), height], 
            [width//2, int(width*(2/3)), int(height*(2/3)), height], 
            [int(width*(2/3)), width, int(height*(2/3)), height]
        ]

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

        self.asteroid_no = 4
        self.SCALE_FACTORS = [1, 0.625, 0.325]
        self.VELS = [1, 2, 1.75]
        self.SIZES = ["L", "M", "S"]
        self.SCORES = [20, 50, 100]

        # [pos, x_vel, y_vel, timer]
        self.particles = []
        self.DECAY = 1.2

        self.score_count = 1
        self.DEATH_SOUND = pygame.mixer.Sound("assets/sounds/dead.wav")
        self.DEATH_SOUND.set_volume(0.25)
        self.ASTEROID_SOUND = pygame.mixer.Sound("assets/sounds/asteroid hit.wav")
        self.ASTEROID_SOUND.set_volume(0.1)

    def spawn_particles(self, coord):
        number = random.randint(3, 5)
        x_vels = []
        y_vels = []
        for i in range (number):
            x_vel, y_vel, x_vels, y_vels = self.velocity_randomizer(1.5, x_vels, y_vels)
            x_vels.append(x_vel)
            y_vels.append(y_vel)
            timer = random.randint(45, 60)
            self.particles.append([coord[:], x_vel, y_vel, timer])

    def handle_particles(self):
        for index, particle in reversed(list(enumerate(self.particles))):
            particle[0][0] += particle[1]
            particle[0][1] += particle[2]
            particle[3] -= self.DECAY 
            if particle[3] <= 0: 
                self.particles.pop(index)

    def velocity_randomizer(self, size, x_vels, y_vels):
        x_vel = random.uniform(-size, size)
        while (x_vel in x_vels) or -0.1 < x_vel < 0.1: 
            x_vel = random.uniform(-size, size)
        y_vel = random.uniform(-size, size)
        while (y_vel in y_vels) or -0.1 < y_vel < 0.1:
            y_vel = random.uniform(-size, size)
        
        return x_vel, y_vel, x_vels, y_vels

    def next_round(self):
        """
        Start the next round
        """
        x_vels = []
        y_vels = []
        for i in range(self.asteroid_no):
            x_vel, y_vel, x_vels, y_vels = self.velocity_randomizer(self.VELS[0], x_vels, y_vels)
            x_vels.append(x_vel)
            y_vels.append(y_vel)
            asteroid = Polygon(random.choice(self.ASTEROID_SHAPES))
            spawn = random.choice(self.spawn_range)
            asteroid.center = [random.randrange(spawn[0], spawn[1]), random.randrange(spawn[2], spawn[3])]
            self.asteroids.append([asteroid, x_vel, y_vel, "L", 1, 1])

        return self

    def spawn_new(self, asteroid):
        asteroids = []
        x_vels = []
        y_vels = []
        if asteroid[3] != "S":
            for i in range(2):
                x_vel, y_vel, x_vels, y_vels = self.velocity_randomizer(self.VELS[self.SIZES.index(asteroid[3])+1], x_vels, y_vels)
                new_asteroid = Polygon(random.choice(self.ASTEROID_SHAPES)).enlarge(self.SCALE_FACTORS[self.SIZES.index(asteroid[3])+1])
                new_asteroid.center = asteroid[0].center
                asteroids.append([new_asteroid, x_vel, y_vel, self.SIZES[self.SIZES.index(asteroid[3])+1], 1, 1])

                x_vels.append(x_vel)
                y_vels.append(y_vel)
        
        return asteroids

    def move(self, player, bullets, score, game_over, shake):
        new_asteroids = []
        for index, asteroid in reversed(list(enumerate(self.asteroids))):
            asteroid[0].move(asteroid[1], asteroid[2])

            # Check if the asteroid has moved out of the screen and move it to the other side
            if asteroid[0].center[0] > self.width + asteroid[0].rect.width//2:
                asteroid[0].center = [-asteroid[0].rect.width//2, asteroid[0].center[1]]
            elif asteroid[0].center[0] < -asteroid[0].rect.width//2:
                asteroid[0].center = [self.width + asteroid[0].rect.width//2, asteroid[0].center[1]]

            if asteroid[0].center[1] > self.width + asteroid[0].rect.height//2:
                asteroid[0].center = [asteroid[0].center[0], -asteroid[0].rect.height//2]
            elif asteroid[0].center[1] < -asteroid[0].rect.height//2:
                asteroid[0].center = [asteroid[0].center[0], self.height + asteroid[0].rect.height//2]

            collision = False
            # Check for bullet-asteroid collisions
            for j, bullet in reversed(list(enumerate(bullets))):
                if asteroid[0].collidecircle(bullet[0]):
                    score += self.SCORES[self.SIZES.index(asteroid[3])]
                    new_asteroids += self.spawn_new(asteroid)
                    self.spawn_particles(asteroid[0].center)
                    self.ASTEROID_SOUND.play()
                    self.asteroids.pop(index)
                    bullets.pop(j)
                    shake = True
                    collision = True
                    break

            if collision:
                continue

            if score >= 10000*self.score_count:
                player.health += 1
                if player.health > 5:
                    player.health = 5
                self.score_count += 1

            # Check if the player has collided with the asteroid
            if not player.dead:
                for line in player.body:
                    if line.collidepolygon(asteroid[0]) and not player.safe:
                        self.DEATH_SOUND.play()
                        self.ASTEROID_SOUND.play()
                        player.health -= 1
                        player.dead = True
                        game_over.game_over = not player.health
                        score += self.SCORES[self.SIZES.index(asteroid[3])]
                        new_asteroids += self.spawn_new(asteroid)
                        self.spawn_particles(asteroid[0].center)
                        self.asteroids.pop(index)
                        shake = True
                        break
                
        self.asteroids += new_asteroids
        self.handle_particles()
        return score, shake

    def draw(self, surface):
        for asteroid in self.asteroids:
            asteroid[0].draw(surface, (255, 255, 255), 2)

        for particle in self.particles:
            pygame.draw.circle(surface, (255, 255, 255), particle[0], 2)