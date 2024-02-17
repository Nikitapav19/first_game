import sqlite3

import pygame


background = pygame.image.load('images/background.jpg')


def about_devs():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width = screen.get_width()
    height = screen.get_height()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
            screen.blit(background, (0, 0))
            font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 60)
            text = font.render('Создатели:', True, 'red')
            text_x = width // 2 - text.get_width() // 2
            text_y = height // 2 - text.get_height() // 2 - (height // 3) + 90
            screen.blit(text, (text_x, text_y))
            text_about_devs1 = font.render('Акылбекова Самира', True, 'black')
            text_x = width // 2 - text_about_devs1.get_width() // 2
            text_y = height // 2 - text_about_devs1.get_height()
            screen.blit(text_about_devs1, (text_x, text_y))
            text_about_devs2 = font.render('Павленко Никита', True, 'black')
            text_x = width // 2 - text_about_devs2.get_width() // 2
            text_y = height // 1.55 - text_about_devs2.get_height()
            screen.blit(text_about_devs2, (text_x, text_y))
            text_about_devs3 = font.render('Шарун Эрна', True, 'black')
            text_x = width // 2 - text_about_devs3.get_width() // 2
            text_y = height // 1.25 - text_about_devs3.get_height()
            screen.blit(text_about_devs3, (text_x, text_y))

            pygame.display.flip()


def settings():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width = screen.get_width()
    height = screen.get_height()
    eq_width = 200
    eq_height = 10
    eq_x = width / 2 - eq_width - 120
    eq_y = height / 2 - eq_height
    con = sqlite3.connect('database/database.db')
    cur = con.cursor()
    volume = cur.execute('SELECT music FROM volume').fetchall()[0][0]
    pygame.mixer.music.set_volume(volume)

    dragging = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    con = sqlite3.connect('database/database.db')
                    cur = con.cursor()
                    cur.execute('UPDATE volume SET music = ?', (volume,)).fetchall()
                    con.commit()
                    con.close()
                    pygame.mixer.music.set_volume(volume)
                    if volume >= 0:
                        return volume
                    else:
                        return 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if eq_x <= mouse_x <= eq_x + eq_width and eq_y <= mouse_y <= eq_y + eq_height:
                        dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    volume = (mouse_x - eq_x) / eq_width
                    if volume <= 0:
                        volume = 0
                    elif volume >= 1:
                        volume = 1
                    pygame.mixer.music.set_volume(volume)

        screen.fill(pygame.Color('black'))
        con = sqlite3.connect('database/database.db')
        cur = con.cursor()
        cur.execute('UPDATE volume SET music = ?', (volume,)).fetchall()
        con.commit()
        con.close()

        screen.blit(background, (0, 0))
        font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 80)
        text = font.render('Настройки:', True, 'red')
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2 - (height // 3) + 90
        screen.blit(text, (text_x, text_y))
        font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 40)
        text_about_volume = font.render('громкость', True, 'black')
        text_x = width // 2 - text_about_volume.get_width() // 2 - 250
        text_y = height // 2 - text_about_volume.get_height() - 50
        screen.blit(text_about_volume, (text_x, text_y))
        font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 25)
        con = sqlite3.connect('database/database.db')
        cur = con.cursor()
        current_volume = cur.execute('SELECT music FROM volume').fetchall()[0][0]
        current_volume *= 100
        current_volume = round(current_volume)
        number_text = font.render(str(current_volume), True, 'black')
        text_x = width // 2 - text_about_volume.get_width() // 2 - 230
        text_y = height // 2 - text_about_volume.get_height() + 22
        screen.blit(number_text, (text_x, text_y))
        font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 10)
        exit_text = font.render('Чтобы принять настройки нажмите esc', True, 'grey')
        text_x = width - exit_text.get_width()
        text_y = height - exit_text.get_height()
        screen.blit(exit_text, (text_x, text_y))

        pygame.draw.rect(screen, 'black', (eq_x, eq_y, eq_width, eq_height))
        pygame.draw.circle(screen, 'red',
                           (eq_x + int(eq_width * pygame.mixer.music.get_volume()), eq_y + eq_height / 2), 10)
        pygame.display.update()
        pygame.display.flip()