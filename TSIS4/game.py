import pygame
import random

class Snake:
    def __init__(self, color):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = (20, 0)
        self.color = color

    def move(self):
        head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        self.body.insert(0, head)
        return head

class Food:
    def __init__(self, color, weight):
        self.color = color
        self.weight = weight
        self.pos = (0, 0)

    def spawn(self, obstacles, snake_body):
        while True:
            self.pos = (random.randint(0, 29) * 20, random.randint(0, 29) * 20)
            if self.pos not in obstacles and self.pos not in snake_body:
                break