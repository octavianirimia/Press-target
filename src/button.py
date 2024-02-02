import pygame



class Button():
    def __init__(self, position: tuple, text: str, font: pygame.font.Font, color: str, hover_color: str):

        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.button_text = font.render(self.text, True, self.color)
        self.rect = self.button_text.get_rect(center = position)
    

    def input(self, mouse_position: tuple):

        if mouse_position[0] in range(self.rect.left, self.rect.right) and \
            mouse_position[1] in range(self.rect.top, self.rect.bottom):
            return True


    def hover(self, mouse_position: tuple):

        if mouse_position[0] in range(self.rect.left, self.rect.right) and \
            mouse_position[1] in range(self.rect.top, self.rect.bottom):
            self.button_text = self.font.render(self.text, True, self.hover_color)
        else:
            self.button_text = self.font.render(self.text, True, self.color)
    
    
    def draw(self, window: pygame.Surface):

        window.blit(self.button_text, self.rect)