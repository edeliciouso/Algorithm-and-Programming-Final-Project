import pygame
from settings import *

pygame.font.init() # Initialize the font


class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE)) # Set a tile with the dimensions of 128 x 128
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()
        if self.text != "empty":
            self.font = pygame.font.SysFont("Consolas", 50) # Set the font and its size
            font_surface = self.font.render(self.text, True, YELLOW_BROWN) # Set a new surface with yellow brown color text
            self.image.fill(LIGHTBROWN) # Fill image with light brown color
            self.font_size = self.font.size(self.text) # Set font size to size of the text
            # Calculate the center of the tile. self.font_size[0] being the width and [1] being the height
            draw_x = (TILESIZE / 2) - self.font_size[0] / 2
            draw_y = (TILESIZE / 2) - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x, draw_y)) # Put text in the middle of the tile
        else:
            self.image.fill(BGCOLOUR) # If text empty, fill with background color

    def update(self): # Give exact coordinates on the grid in pixels
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def click(self, mouse_x, mouse_y): # Check if tile is clicked
        # Check if mouse is inside of the tile
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom

    # Check the right, left, top, and bottom side of each tile
    def right(self):
        return self.rect.x + TILESIZE < GAME_SIZE * TILESIZE

    def left(self):
        return self.rect.x - TILESIZE >= 0

    def up(self):
        return self.rect.y - TILESIZE >= 0

    def down(self):
        return self.rect.y + TILESIZE < GAME_SIZE * TILESIZE


class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen): # Draw text on screen
        font = pygame.font.SysFont("Consolas", 30)
        text = font.render(self.text, True, LIGHTBROWN)
        screen.blit(text, (self.x, self.y))


class Button: # For the shuffle and reset button
    def __init__(self, x, y, width, height, text, colour, text_colour):
        self.colour, self.text_colour = colour, text_colour
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen): # Draw the button on the screen
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Consolas", 30)
        text = font.render(self.text, True, self.text_colour)
        self.font_size = font.size(self.text)
        # Put text in the middle of button
        draw_x = self.x + (self.width / 2) - self.font_size[0] / 2
        draw_y = self.y + (self.height / 2) - self.font_size[1] / 2
        screen.blit(text, (draw_x, draw_y))

    def click(self, mouse_x, mouse_y): # Check if mouse is in button
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height
