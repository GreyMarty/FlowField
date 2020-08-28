from pygame.math import Vector2
from pygame.draw import circle
from random import random, randint

from confing import WINDOW_WIDTH, WINDOW_HEIGHT, PARTICLE_MAX_VEL


PALETTE = (
    (255, 0, 0, 3),
    (0, 255, 0, 3),
    (0, 0, 255, 3)
)


class Particle:
    def __init__(self):
        self.pos = Vector2(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
        self.vel = Vector2(PARTICLE_MAX_VEL * random(), PARTICLE_MAX_VEL * random())
        self.max_vel = PARTICLE_MAX_VEL

        self.color = (0, 0, 0, 3)
        self.radius = 1

    def update(self, time_delta):
        self.pos += self.vel

        self.pos.x %= WINDOW_WIDTH
        self.pos.y %= WINDOW_HEIGHT

    def draw(self, surface):
        circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

    def add_force(self, force):
        self.vel += force

        if self.vel.magnitude() > self.max_vel:
            self.vel *= self.max_vel / self.vel.magnitude()
