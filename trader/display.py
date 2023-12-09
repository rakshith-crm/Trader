import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from enum import Enum

FONT_STYLE = 'freesansbold.ttf'
FONT_SIZE = 24
MIN_COLUMN_SIZE = 600
MIN_ROW_SIZE = 0


class RGB(Enum):
    WHITE = (255, 255, 255)
    GREEN = (6, 69, 1)
    BLUE = (0, 0, 128)


class DisplayWindow:
    def __init__(self, title, window_dims=(MIN_COLUMN_SIZE, MIN_ROW_SIZE)):
        pygame.init()
        pygame.display.set_caption(title)
        self.window_dims = window_dims
        self.display_surface = pygame.display.set_mode(window_dims)
        self.font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        self.data = {}
        self.ROW_SIZE = 40
        self.TOP_MARGIN = 10
        self.LEFT_MARGIN = 20
        self.RIGHT_MARGIN = 20

    def update(self, data: dict):
        if self.data == data:
            return
        self.data = data
        self.update_window_dims()
        content = []
        for i, (key, value) in enumerate(data.items()):
            key = str(key) + ' : '
            text_key, text_rect_key = self.get_blit(key, i, color=RGB.GREEN, alignment='left')
            text_value, text_rect_value = self.get_blit(value, i, color=RGB.BLUE, alignment='right')
            content.append((text_key, text_rect_key))
            content.append((text_value, text_rect_value))
        self.display_surface.fill(RGB.WHITE.value)
        self.display_surface.blits(content)
        pygame.display.update()

    def get_blit(self, text_value, index, color, alignment='left'):
        text = self.font.render(str(text_value), True, color.value, RGB.WHITE.value)
        text_rect = text.get_rect()
        text_rect.top = index * self.ROW_SIZE + self.TOP_MARGIN
        if alignment == 'left':
            text_rect.left = self.LEFT_MARGIN
        else:
            text_rect.right = self.window_dims[0] - self.RIGHT_MARGIN
        return text, text_rect

    def update_window_dims(self):
        required_size = (MIN_COLUMN_SIZE, len(self.data) * self.ROW_SIZE + self.TOP_MARGIN)
        if self.window_dims != required_size:
            self.display_surface = pygame.display.set_mode(required_size)
            self.display_surface.fill(RGB.WHITE.value)
            self.window_dims = required_size
