import sqlite3

import pygame

from tutorial import tutorial

maps_dir = {'first_level': [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 1],
                            [1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1],
                            [1, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 3, 0, 7, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1],
                            [1, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]],
            'second_level': [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 0, 0, 2, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 2, 0, 0, 1],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 0, 0, 0, 0, 0, 7, 1, 10, 0, 0, 0, 0, 9, 1, 7, 0, 0, 0, 0, 7, 1],
                             [1, 0, 0, 2, 2, 0, 0, 2, 2, 1, 2, 2, 0, 0, 2, 2, 1, 2, 2, 0, 0, 2, 2, 1],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 0, 0, 7, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 0, 0, 2, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 2, 0, 0, 1],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 0, 0, 0, 7, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 4, 0, 1],
                             [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]],
            'third_level': [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 10, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1],
                            [1, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 7, 2, 2, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 7, 0, 0, 0, 2, 2, 0, 3, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 7, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 2, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 2, 2, 0, 0, 7, 0, 0, 0, 0, 1],
                            [1, 0, 0, 7, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 2, 2, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 1],
                            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]],
            'fourth_level': [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                             [1, 0, 7, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 7, 4, 0, 0, 0, 1],
                             [1, 0, 2, 0, 0, 0, 1, 0, 2, 2, 0, 0, 2, 2, 0, 1, 0, 0, 2, 2, 2, 0, 0, 1],
                             [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 7, 0, 0, 1, 0, 0, 0, 7, 7, 0, 0, 0, 1, 0, 7, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 2, 0, 0, 1, 0, 0, 0, 2, 2, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                             [1, 0, 0, 0, 3, 0, 1, 0, 3, 0, 9, 10, 0, 4, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                             [1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1]]}


class ImageButton:
    def __init__(self, x, y, width, height, text, image_path, hover_image_path, sound_path):
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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


def levels_menu():
    pygame.init()
    # background = pygame.image.load("./")
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # screen.blit(background, (0, 0))
    width = screen.get_width()
    height = screen.get_height()
    button_lvl_1 = ImageButton(200, 310, 200, 200, "", './images/first_level.png',
                               './images/first_level2.png', './sounds/perf_sound.mp3')
    button_lvl_2 = ImageButton(500, 310, 200, 200, "", './images/second_level.png',
                               './images/second_level2.png', './sounds/perf_sound.mp3')
    button_lvl_3 = ImageButton(800, 310, 200, 200, "", './images/third_level1.png',
                               './images/third_level2.png', './sounds/perf_sound.mp3')
    button_lvl_4 = ImageButton(1100, 310, 200, 200, "", './images/fourth_level1.png',
                               './images/fourth_level2.png', './sounds/perf_sound.mp3')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                first_level_x, first_level_y = 200, 310
                second_level_x, second_level_y = 500, 310
                third_level_x, third_level_y = 800, 310
                fourth_level_x, fourth_level_y = 1100, 310
                if (first_level_x <= mouse_x <= first_level_x + 200 and
                        first_level_y <= mouse_y <= first_level_y + 200):
                    tutorial(maps_dir['first_level'], 1, None)
                elif (second_level_x <= mouse_x <= second_level_x + 200 and
                      second_level_y <= mouse_y <= second_level_y + 200):
                    tutorial(maps_dir['second_level'], 2, None)
                elif (third_level_x <= mouse_x <= third_level_x + 200 and
                      third_level_y <= mouse_y <= third_level_y + 200):
                    tutorial(maps_dir['third_level'], 3, None)
                elif (fourth_level_x <= mouse_x <= third_level_x + 200 and
                      fourth_level_y <= mouse_y <= fourth_level_y + 200):
                    tutorial(maps_dir['fourth_level'], 4, None)
            button_lvl_1.handle_event(event, width, height)
            button_lvl_2.handle_event(event, width, height)
            button_lvl_3.handle_event(event, width, height)
            button_lvl_4.handle_event(event, width, height)
            # button.handle_event(event, width, height)
        font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 20)
        button_lvl_1.chek_hover(pygame.mouse.get_pos())
        button_lvl_1.draw(screen)
        button_lvl_2.chek_hover(pygame.mouse.get_pos())
        button_lvl_2.draw(screen)
        button_lvl_3.chek_hover(pygame.mouse.get_pos())
        button_lvl_3.draw(screen)
        button_lvl_4.chek_hover(pygame.mouse.get_pos())
        button_lvl_4.draw(screen)
        screen.blit(font.render('Уровень I', True, 'white'), (200, 550))
        screen.blit(font.render('Уровень II', True, 'white'), (500, 550))
        screen.blit(font.render('Уровень III', True, 'white'), (800, 550))
        screen.blit(font.render('Уровень IV', True, 'white'), (1100, 550))

        con = sqlite3.connect('./database/database.db')
        cur = con.cursor()
        first_level_score = cur.execute('SELECT first_level_amount FROM coins').fetchall()[0][0]
        second_level_score = cur.execute('SELECT second_level_amount FROM coins').fetchall()[0][0]
        third_level_score = cur.execute('SELECT third_level_amount FROM coins').fetchall()[0][0]
        fourth_level_score = cur.execute('SELECT fourth_level_amount FROM coins').fetchall()[0][0]

        font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 50)

        text_surface = font.render(str(first_level_score), True, 'white')
        text_rect = (280, 630)
        screen.blit(text_surface, text_rect)
        text_surface = font.render(str(second_level_score), True, 'white')
        text_rect = (580, 630)
        screen.blit(text_surface, text_rect)
        text_surface = font.render(str(third_level_score), True, 'white')
        text_rect = (880, 630)
        screen.blit(text_surface, text_rect)
        text_surface = font.render(str(fourth_level_score), True, 'white')
        text_rect = (1180, 630)
        screen.blit(text_surface, text_rect)

        pygame.display.flip()
