import pygame as pg
from pygame.math import Vector2
from time import time
from math import cos, sin, pi
from opensimplex.opensimplex import OpenSimplex
from random import random

from confing import *
from particle import Particle


class FlowField:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.fill(BG_COLOR)
        pg.display.set_caption("FLOWFIELD")

        self.paused = False

        self.noise = OpenSimplex()
        self.noise_seed = random() * 100
        self.time_passed = 0

        self.particles = [Particle() for _ in range(PARTICLE_AMOUNT)]

    def get_direction(self, x, y):
        angle = pi * self.get_noise_val(x, y)
        return Vector2(cos(angle), sin(angle))

    def get_noise_val(self, x, y):
        return self.noise.noise3d(x * NOISE_SCALE, y * NOISE_SCALE, self.time_passed * NOISE_SCALE * NOISE_SPEED_SCALE + self.noise_seed)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.paused = not self.paused

    def render(self):
        # self.screen.fill((0, 0, 0))

        transparent_surf = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pg.SRCALPHA)
        transparent_surf.set_alpha(10)
        for particle in self.particles:
            particle.draw(transparent_surf)
        self.screen.blit(transparent_surf, (0, 0))

        pg.display.update()

    def draw_noise(self):
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            for x in range(0, WINDOW_WIDTH, CELL_SIZE):
                rect = [
                    Vector2(x, y),
                    Vector2(CELL_SIZE, CELL_SIZE)
                ]
                k = self.get_noise_val(x, y)
                k = k if k > 0 else 0
                color = [int(255 * k) for _ in range(3)]
                pg.draw.rect(self.screen, color, rect)

    def draw_vectors(self):
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            for x in range(0, WINDOW_WIDTH, CELL_SIZE):
                start_pos = Vector2(x, y) + Vector2(CELL_SIZE, CELL_SIZE) / 2
                end_pos = start_pos + CELL_SIZE / 2 * self.get_direction(x, y)
                pg.draw.line(self.screen, (0, 255, 0), start_pos, end_pos, 2)

    def logic(self, time_delta):
        for particle in self.particles:
            k = abs(self.get_noise_val(particle.pos.x, particle.pos.y))
            particle.add_force(self.get_direction(particle.pos.x, particle.pos.y) * FLOW_FORCE * k)
            particle.update(time_delta)

    def mainloop(self):
        time_delta = 0
        while True:
            start = time()

            self.check_events()
            if not self.paused:
                self.logic(time_delta)
                self.render()

            time_delta = time() - start
            self.time_passed += time_delta


FlowField().mainloop()
