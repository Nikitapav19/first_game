import sqlite3
import sys
from random import randint

import pygame


def tutorial(world_map, level_number, text_for_tutorial=False):
    tile_size = 50
    pygame.init()
    global number_of_players, black_cat_sound, dog_sound
    number_of_players = 2
    background_image = pygame.image.load('./images/sky.png')
    restart_button_image = pygame.image.load('./images/restart_button.png')
    dog_img = pygame.image.load('./images/enemy_dog.png')
    black_cat_img = pygame.image.load('./images/enemy_cat.png')
    screen_width = 1200
    screen_height = 800
    game_over = 0
    score = 0
    clock = pygame.time.Clock()
    FPS = 60
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Platformer')

    class Player_Tom:
        def __init__(self, x, y):
            image = pygame.image.load('./images/Tom.png')
            self.image = pygame.transform.scale(image, (60, 80))
            self.images_right = []
            self.images_left = []
            self.index = 0
            self.counter = 0
            self.direction = 0
            dead_image = pygame.image.load('./images/dead_tom.png')
            self.dead_image = pygame.transform.scale(dead_image, (60, 80))
            for num in range(1, 5):
                img_right = pygame.image.load(f'./images/tom{num}.png')
                img_right = pygame.transform.scale(img_right, (60, 80))
                img_left = pygame.transform.flip(img_right, True, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
            self.image = self.images_right[self.index]
            self.rect = self.image.get_rect()
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.rect.x = x
            self.rect.y = y
            self.vel_y = 0
            self.jumped = True
            self.in_air = False

        def update(self, game_over):
            dx = 0
            dy = 0
            walk_cooldown = 6

            if game_over != 1 and game_over != -1:
                key = pygame.key.get_pressed()
                if key[pygame.K_UP] and self.jumped == False and self.in_air == False:
                    self.vel_y = -20
                    self.jumped = True
                if key[pygame.K_UP] == False:
                    self.jumped = False
                if key[pygame.K_LEFT]:
                    dx -= 2
                    self.counter += 1
                    self.direction = -1
                if key[pygame.K_RIGHT]:
                    dx += 2
                    self.counter += 1
                    self.direction = 1
                if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                    self.counter = 0
                    self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]

                if self.counter > walk_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images_right):
                        self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]

                self.vel_y += 1
                if self.vel_y > 10:
                    self.vel_y = 10
                dy += self.vel_y

                self.in_air = True
            
                for tile in world.tile_list:
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        if self.vel_y < 0:
                            dy = tile[1].bottom - self.rect.top
                            self.vel_y = 0
                        elif self.vel_y >= 0:
                            dy = tile[1].top - self.rect.bottom
                            self.vel_y = 0
                            self.in_air = False

                if pygame.sprite.spritecollide(self, exit_group, False):
                    game_over += 0.6

                if self.rect.bottom > screen_height:
                    self.rect.bottom = screen_height
                    dy = 0

                if pygame.sprite.spritecollide(self, dog_group, False):
                    game_over = -1

                self.rect.x += dx
                self.rect.y += dy

            if game_over == 0.6:
                self.rect.y = -100
                self.rect.x = -100

            elif game_over == -1:
                self.image = self.dead_image
                self.image = pygame.transform.scale(self.image, (100, 80))

            elif game_over == 1:
                self.rect.y = -100
                self.rect.x = -100

            screen.blit(self.image, self.rect)
            return game_over

        def restart(self, x, y):  # Можно убрать в принципе
            self.images_right = []
            self.images_left = []
            self.index = 0
            self.counter = 0
            for num in range(1, 5):
                img_right = pygame.image.load(f'images/tom{num}.png')
                img_right = pygame.transform.scale(img_right, (60, 80))
                img_left = pygame.transform.flip(img_right, True, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
            self.dead_image = pygame.image.load('images/dead_tom.png')
            self.image = self.images_right[self.index]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.vel_y = 0
            self.jumped = False
            self.direction = 0
            self.in_air = True

    class Player_Jerry:
        def __init__(self, x, y):
            self.images_right = []
            self.images_left = []
            self.index = 0
            self.counter = 0
            self.direction = 0
            dead_image = pygame.image.load('./images/dead_jerry.png')
            self.dead_image = pygame.transform.scale(dead_image, (60, 80))
            for num in range(1, 5):
                img_right = pygame.image.load(f'./images/jerry{num}.png')
                img_right = pygame.transform.scale(img_right, (40, 50))
                img_left = pygame.transform.flip(img_right, True, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
            self.image = self.images_right[self.index]
            self.rect = self.image.get_rect()
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.rect.x = x
            self.rect.y = y
            self.vel_y = 0
            self.jumped = True
            self.in_air = False

        def update(self, game_over):
            dx = 0
            dy = 0
            walk_cooldown = 6

            if game_over != 1 and game_over != -1:
                key = pygame.key.get_pressed()
                if key[pygame.K_w] and not self.jumped and not self.in_air:
                    self.vel_y = -20
                    self.jumped = True
                if not key[pygame.K_w]:
                    self.jumped = False
                if key[pygame.K_a]:
                    dx -= 2
                    self.counter += 1
                    self.direction = -1
                if key[pygame.K_d]:
                    dx += 2
                    self.counter += 1
                    self.direction = 1
                if not key[pygame.K_a] and not key[pygame.K_d]:
                    self.counter = 0
                    self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]

                if self.counter > walk_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images_right):
                        self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]

                self.vel_y += 1
                if self.vel_y > 10:
                    self.vel_y = 10
                dy += self.vel_y

                self.in_air = True

                for tile in world.tile_list:
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        if self.vel_y < 0:
                            dy = tile[1].bottom - self.rect.top
                            self.vel_y = 0
                        elif self.vel_y >= 0:
                            dy = tile[1].top - self.rect.bottom
                            self.vel_y = 0
                            self.in_air = False

                if pygame.sprite.spritecollide(self, exit_group2, False):
                    game_over += 0.4

                if self.rect.bottom > screen_height:
                    self.rect.bottom = screen_height
                    dy = 0

                if pygame.sprite.spritecollide(self, black_cat_group, False):
                    game_over = -1

                self.rect.x += dx
                self.rect.y += dy

            if game_over == 0.4:
                self.rect.y = -100
                self.rect.x = -100

            elif game_over == -1:
                self.image = self.dead_image
                self.image = pygame.transform.scale(self.image, (100, 80))

            elif game_over == 1:
                self.rect.y = -100
                self.rect.x = -100

            screen.blit(self.image, self.rect)
            return game_over

        def restart(self, x, y):
            self.images_right = []
            self.images_left = []
            self.index = 0
            self.counter = 0
            for num in range(1, 5):
                img_right = pygame.image.load(f'images/jerry{num}.png')
                img_right = pygame.transform.scale(img_right, (40, 50))
                img_left = pygame.transform.flip(img_right, True, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
            self.dead_image = pygame.image.load('images/dead_jerry.png')
            self.image = self.images_right[self.index]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.vel_y = 0
            self.jumped = False
            self.direction = 0
            self.in_air = True

    class World:
        def __init__(self, data):
            self.tile_list = []

            dirt_img = pygame.image.load('./images/dirt.png')
            grass_img = pygame.image.load('./images/grass.png')
            exit_door_image = pygame.image.load('./images/exit_door.png')

            tile_size = 50

            row_count = 0
            for row in data:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 2:
                        img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 3:
                        dog = Enemy(col_count * tile_size, row_count * tile_size, dog_img)
                        dog_group.add(dog)
                    if tile == 4:
                        black_cat = Enemy(col_count * tile_size, row_count * tile_size, black_cat_img)
                        black_cat_group.add(black_cat)
                    if tile == 7:
                        coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                        coin_group.add(coin)
                    if tile == 9:
                        exit1 = Exit_for_Tom(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                        exit_group.add(exit1)
                    if tile == 10:
                        exit2 = Exit_for_Jerry(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                        exit_group2.add(exit2)
                    
                    col_count += 1
                row_count += 1

        def draw(self):
            for tile in self.tile_list:
                screen.blit(tile[0], tile[1])

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y, image_enemy):
            pygame.sprite.Sprite.__init__(self)
            self.image_enemy = image_enemy
            self.image = pygame.transform.scale(self.image_enemy, (40, 75))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y - 25
            self.move_direction = 1
            self.move_counter = 0

        def update(self):
            self.rect.x += self.move_direction
            self.move_counter += 1
            if abs(self.move_counter) > 50:
                self.move_direction *= -1
                self.move_counter *= -1

    class Exit_for_Tom(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('./images/exit_door_jerry.png')
            self.image = pygame.transform.scale(img, (50, int(50 * 1.5)))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class Exit_for_Jerry(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('./images/exit_door.png')
            self.image = pygame.transform.scale(img, (50, int(50 * 1.5)))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class Coin(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('./images/coin.png')
            self.image = pygame.transform.scale(img,  (50, 50))
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

    class Button:
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.clicked = False

        def draw(self):
            action = False

            pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    action = True
                    self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            screen.blit(self.image, self.rect)

            return action

    world_data = world_map

    player_Tom = Player_Tom(100, screen_height - 130)
    player_Jerry = Player_Jerry(800, screen_height - 130)
    restart_button = Button(screen_width // 2 - 100, screen_height // 3 - 100, restart_button_image)
    dog_group = pygame.sprite.Group()
    black_cat_group = pygame.sprite.Group()
    exit_group2 = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    world = World(world_data)
    score_coin = Coin(tile_size, tile_size // 2)
    coin_group.add(score_coin)

    running = True
    while running:
        
        screen.blit(background_image, (0, 0))

        world.draw()
        dog_group.draw(screen)
        black_cat_group.draw(screen)
        exit_group.draw(screen)
        exit_group2.draw(screen)
        coin_group.draw(screen)
        dog_group.update()
        black_cat_group.update()
        game_over = player_Tom.update(game_over)
        game_over = player_Jerry.update(game_over)

        if text_for_tutorial:
            font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 15)
            tut_text1 = 'Управление Томом - стрелки, управление Джерри - WASD;'
            tut_text2 = 'Для Тома опасен бульдог Спайк, а враг Джерри - чёрный кот Бутч;'
            tut_text3 = 'Тому необходимо добраться до синей двери, Джерри - до коричневой.'
            text1 = font.render(tut_text1, True, 'black')
            text2 = font.render(tut_text2, True, 'black')
            text3 = font.render(tut_text3, True, 'black')
            screen.blit(text1, (100, 100))
            screen.blit(text2, (100, 150))
            screen.blit(text3, (100, 200))

        if pygame.sprite.spritecollide(player_Tom, coin_group, True):
            score += 1
            print(score)
        if pygame.sprite.spritecollide(player_Jerry, coin_group, True):
            score += 1
            print(score)

        if game_over == -1:
            if restart_button.draw():
                score = 0
                pygame.quit()
                tutorial(world_map, level_number, None)

                game_over = 0

        if game_over == 0.6:
            pass

        if game_over == 0.4:
            pass

        if game_over == 1:
            font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 80)
            text = font.render('Вы победили!', True, 'red')
            text_x = 150
            text_y = 200
            screen.blit(text, (text_x, text_y))

            con = sqlite3.connect('database/database.db')
            cur = con.cursor()

            if level_number == 1:
                cur.execute(
                    'UPDATE coins SET first_level_amount = CASE WHEN'
                    ' :score > first_level_amount THEN :score ELSE first_level_amount END',
                    (score, ))

            if level_number == 2:
                cur.execute('UPDATE coins SET second_level_amount = CASE WHEN'
                            ' :score > second_level_amount THEN :score ELSE second_level_amount END',
                            (score, ))

            if level_number == 3:
                cur.execute('UPDATE coins SET third_level_amount = CASE WHEN'
                            ' :score > third_level_amount THEN :score ELSE third_level_amount END', (score, ))

            if level_number == 4:
                cur.execute('UPDATE coins SET fourth_level_amount = CASE WHEN'
                            ' :score > fourth_level_amount THEN :score ELSE fourth_level_amount END', (score, ))
            con.commit()
            con.close()

            ending = pygame.image.load(f'./images/cat_ending_{randint(1, 3)}.png')
            ending = pygame.transform.scale(ending, (screen_width, screen_height))
            screen.blit(ending, (0, 0))

            pygame.display.update()
            pygame.time.delay(3000)
            pygame.quit()
            tutorial(world_map, level_number, None)

        font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 30)
        text_surface = font.render(str(score), True, 'white')
        text_x, text_y = 4, 12
        screen.blit(text_surface, (text_x, text_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        clock.tick(FPS)

        pygame.display.update()

    pygame.quit()
