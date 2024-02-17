import sys

import pygame
import sqlite3
from buttons_functionality import about_devs, settings
from levels import levels_menu
from tutorial import tutorial


def play_music():
    global sound_for_menu_music
    sound_for_menu_music = pygame.mixer.Sound('./sounds/main_music.mp3')
    sound_for_menu_music.play(-1)
    con = sqlite3.connect('database/database.db')
    cur = con.cursor()
    volume = cur.execute('SELECT music FROM volume').fetchall()
    if volume:
        sound_for_menu_music.set_volume(volume[0][0])
    else:
        sound_for_menu_music.set_volume(1)
    con.close()


class ImageButton:
    def __init__(self, x, y, width, height, text, image_path, hover_image_path=None, sound_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = self.image
        if hover_image_path:
            self.hover_image = pygame.image.load(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)
        self.is_hovered = False

    def draw(self, screen):
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 20)
        text_surface = font.render(self.text, True, 'white')
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def chek_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event, monitor_width, monitor_height):
        tutorial_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        ]
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_width = 252
            button_height = 74
            exit_button_x, exit_button_y = monitor_width / 2 - (252 / 2), 600
            about_devs_button_x, about_devs_button_y = monitor_width / 2 - (252 / 2), 530
            settings_button_x, settings_button_y = monitor_width / 2 - (252 / 2), 460
            tutorial_button_x, tutorial_button_y = monitor_width / 2 - (252 / 2), 390
            if exit_button_x <= mouse_x <= button_width + exit_button_x \
                    and exit_button_y <= mouse_y <= exit_button_y + button_height:
                pygame.quit()
                sys.exit()
            elif about_devs_button_x <= mouse_x <= button_width + about_devs_button_x \
                    and about_devs_button_y <= mouse_y <= about_devs_button_y + button_height:
                about_devs()
            elif settings_button_x <= mouse_x <= button_width + settings_button_x \
                    and settings_button_y <= mouse_y <= settings_button_y + button_height:
                sound_for_menu_music.set_volume(settings())  # Настройки громкости
            elif tutorial_button_x <= mouse_x <= button_width + tutorial_button_x \
                    and tutorial_button_y <= mouse_y <= tutorial_button_y + button_height:
                tutorial(tutorial_map, level_number=5, text_for_tutorial='text')
            else:
                levels_menu()
