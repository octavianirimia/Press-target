import math
import pygame
import random



class Target(pygame.sprite.Sprite):

    def __init__(self, window_dimensions: tuple, group: pygame.sprite.Group) -> None:
        pygame.sprite.Sprite.__init__(self, group)

        self.radius: int = 1
        self.maximum_radius: int = 30
        self.position: tuple = (random.randint(self.maximum_radius, window_dimensions[0] - self.maximum_radius),
                                random.randint(100 + self.maximum_radius, window_dimensions[1] - self.maximum_radius))
        self.speed: int = 25

        self.maximum_radius_reached: bool = False
    

    def click_collision(self, mouse_position: tuple) -> None:

        # Se calculează dinstanța dintre cursor și centrul țintei cu ajutorul dinstanței euclidiene
        distance: float = math.sqrt((mouse_position[0] - self.position[0]) ** 2 + (mouse_position[1] - self.position[1]) ** 2)

        if distance <= self.radius:
            return True

        return False
    

    def update(self, dt: float) -> None:

        if not self.maximum_radius_reached:
            self.radius += dt * self.speed

            if self.radius >= self.maximum_radius:
                self.maximum_radius_reached = True

        else:
            self.radius -= dt * self.speed

            if self.radius < 1:
                self.kill()


    def draw(self, window: pygame.Surface) -> None:

        pygame.draw.circle(window, "RED", self.position, self.radius)
        pygame.draw.circle(window, "WHITE", self.position, self.radius - 5)
        pygame.draw.circle(window, "RED", self.position, self.radius - 10)
        pygame.draw.circle(window, "WHITE", self.position, self.radius - 15)
        pygame.draw.circle(window, "RED", self.position, self.radius - 20)
        pygame.draw.circle(window, "WHITE", self.position, self.radius - 25)