import pygame

pygame.font.init()

class Label:
    def __init__(self, font=pygame.font.SysFont("comicsansms", 15), text="", position: tuple=(0, 0), color=(0, 0, 0)):
        self.text = font.render(text, True, color)
        self.position = position
    def draw(self, surface: pygame.Surface):
        surface.blit(self.text, self.position)

class Button:
    def __init__(self, icon_false: pygame.Surface, icon_true: pygame.Surface, icon_position: tuple):
        self.icon_false = icon_false
        self.icon_true = icon_true
        self.position = icon_position
        self.rect = self.icon_false.get_rect()
        self.rect.x += self.position[0]
        self.rect.y += self.position[1]

    def draw(self, surface: pygame.Surface):
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            surface.blit(self.icon_true, self.position)
        else:
            surface.blit(self.icon_false, self.position)
    def execute(self, event: int=None):
        mouse_position = pygame.mouse.get_pos()
        if isinstance(event, int): 
            if self.rect.collidepoint(mouse_position):
                pygame.event.post(event)
        else:
            if self.rect.collidepoint(mouse_position):
                return True
            else:
                return False