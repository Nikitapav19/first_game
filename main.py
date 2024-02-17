import pygame

from main_menu_buttons import ImageButton, play_music


def main_screen_draw():
    global first_play_button, tutorial_button, settings_button, about_the_creators_button, exit_the_game_button
    screen.fill(pygame.Color('black'))
    play_music()
    font = pygame.font.Font('./fonts/FontdinerSwanky-Regular.ttf', 80)
    logo = font.render('Tom & Jerry', True, 'red')
    text = font.render('Escape', True, 'red')
    text_x = width + text.get_width()
    text_y = 0 + logo.get_height()
    logo_x = 0 - logo.get_width()
    logo_y = height // 2 - logo.get_height() // 2 - (height // 3)
    first_play_button = ImageButton(width / 2 - (252 / 2), 320, 252, 74, "Играть", './images/red_button1.png',
                                    './images/red_button2.png', './sounds/perf_sound.mp3')
    tutorial_button = ImageButton(width / 2 - (252 / 2), 390, 252, 74, "Обучение", './images/yellow_button1.png',
                                  './images/yellow_button2.png', './sounds/perf_sound.mp3')
    settings_button = ImageButton(width / 2 - (252 / 2), 460, 252, 74, "Настройки", './images/green_button1.png',
                                  './images/green_button2.png', './sounds/perf_sound.mp3')
    about_the_creators_button = ImageButton(width / 2 - (252 / 2), 530, 252, 74, "О создателях",
                                            './images/blue_button1.png', './images/blue_button2.png',
                                            './sounds/perf_sound.mp3')
    exit_the_game_button = ImageButton(width / 2 - (252 / 2), 600, 252, 74, "Выход", './images/purple_button1.png',
                                       './images/purple_button2.png', './sounds/perf_sound.mp3')

    while logo_x <= width // 2 - logo.get_width() // 2:
        screen.fill(pygame.Color('black'))
        screen.blit(logo, (logo_x, logo_y))
        pygame.display.flip()
        pygame.time.delay(7)
        logo_x += 5

    screen.fill(pygame.Color('black'))
    screen.blit(logo, (logo_x, logo_y))
    screen.blit(text, (text_x, text_y))
    pygame.display.flip()


def main_menu_sign():
    screen.blit(background, (0, 0))
    font = pygame.font.Font('./fonts/FontdinerSwanky-Regular.ttf', 80)
    text = font.render('Escape', True, 'red')
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2 - (height // 3) + 90
    screen.blit(text, (text_x, text_y))
    logo = font.render('Tom & Jerry', True, 'red')
    logo_x = width // 2 - logo.get_width() // 2
    logo_y = height // 2 - logo.get_height() // 2 - (height // 3)
    screen.blit(logo, (logo_x, logo_y))


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Tom and Jerry: Escape')
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width = screen.get_width()
    height = screen.get_height()# pygame.display.set_icon(pygame.image.load('images/name.ico'))  Вместо name название картинки
    FPS = 60
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    background = pygame.image.load('images/background.jpg')
    running = True
    main_screen_draw()  # Изменить в случае анимаций
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
            screen.fill(pygame.Color('black'))
            main_menu_sign()
            if event.type == pygame.VIDEOEXPOSE:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_x += 1
                pygame.mouse.set_pos(mouse_x, mouse_y)
            first_play_button.handle_event(event, width, height)
            tutorial_button.handle_event(event, width, height)
            settings_button.handle_event(event, width, height)
            about_the_creators_button.handle_event(event, width, height)
            exit_the_game_button.handle_event(event, width, height)

        first_play_button.chek_hover(pygame.mouse.get_pos())
        first_play_button.draw(screen)
        tutorial_button.chek_hover(pygame.mouse.get_pos())
        tutorial_button.draw(screen)
        settings_button.chek_hover(pygame.mouse.get_pos())
        settings_button.draw(screen)
        about_the_creators_button.chek_hover(pygame.mouse.get_pos())
        about_the_creators_button.draw(screen)
        exit_the_game_button.chek_hover(pygame.mouse.get_pos())
        exit_the_game_button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
        pygame.display.update()
    pygame.quit()