from pygame import *

init()
clock = time.Clock()


# Музыка
music_damage = mixer.Sound("music/fun_damage.mp3")
music_am = mixer.Sound("music/fun_am.mp3")

# Шрифт
fonts = font.Font('font/ofont.ru_Zeitmax.ttf', 100)
font_point = font.Font('font/ofont.ru_Etude Noire.ttf', 35)

# Тексты
display.set_caption("Игра")
dead_label = fonts.render(f"Вы проиграли!", True, "black")
back_label = fonts.render("Заново", True, "red", "black")
menu_label = fonts.render("В меню", True, "red", "black")

start_label = fonts.render("Играть", True, "black")
quit_label = fonts.render("Выход", True, "black")


# Игра
screen = display.set_mode((1280, 720))
game_window = 'main'
kol_ghost = 0
heart = 3
running_display = True

left_move = [
    image.load("img/movement/left_1.png").convert_alpha(),
    image.load("img/movement/left_2.png").convert_alpha(),
    image.load("img/movement/left_3.png").convert_alpha(),
    image.load("img/movement/left_4.png").convert_alpha(),
]

right_move = [
    image.load("img/movement/right_1.png").convert_alpha(),
    image.load("img/movement/right_2.png").convert_alpha(),
    image.load("img/movement/right_3.png").convert_alpha(),
    image.load("img/movement/right_4.png").convert_alpha(),
]

# фон
bg = image.load("img/bg.jpg").convert_alpha()
bg_x1 = 0

# игрок
man_x = 300
man_y = 450
man_jump = 10
score = 0

heart_img = image.load("img/heart.png").convert_alpha()

# враги
ghost = image.load("img/ghost.png").convert_alpha()
hill = image.load("img/hill.png").convert_alpha()


# значение
value = 0
is_jump = False
frame_counter = 0

# объекты
list_ghost = []
list_hill = []
list_heart = []

# таймер
millis = 1500
times = USEREVENT + 1
time.set_timer(times, millis)


while running_display:
    keys = key.get_pressed()
    mouses = mouse.get_pos()
    # Анимация фона
    screen.blit(bg, (bg_x1, 0))
    screen.blit(bg, (bg_x1 + 1280, 0))
    clock.tick(80)

    if bg_x1 == -1280:
        bg_x1 = 0
    bg_x1 -= 5

    if game_window == 'main':
        screen.blit(start_label, (410, 250))
        screen.blit(quit_label, (430, 400))
        if start_label.get_rect(topleft=(410, 250)).collidepoint(mouses) and mouse.get_pressed()[0]:
            game_window = 'game'
        if quit_label.get_rect(topleft=(430, 400)).collidepoint(mouses) and mouse.get_pressed()[0]:
            game_window = 'quit'
        display.update()
    elif game_window == 'game':

        man_rect = right_move[0].get_rect(topleft=(man_x, man_y))
        screen.blit(font_point.render(f"Счёт: {score}", True, "black"), (0, 0))

        # HP
        heart_x = 0
        for _ in range(heart):
            screen.blit(heart_img, (heart_x, 620))
            heart_x += 100

        # создание ghost и прикосновение с ними
        if list_ghost:
            for el in list_ghost:
                screen.blit(ghost, el)
                el.x -= 10

                if man_rect.colliderect(el):
                    if heart == 1:
                        game_window = 'fail'
                    else:
                        heart -= 1
                        music_damage.play()
                        list_ghost.remove(el)

                if el.x < -100:
                    score += 100
                    list_ghost.remove(el)

        # создание hill и прикосновение с ними
        if list_hill:
            for el in list_hill:
                screen.blit(hill, el)
                el.x -= 10

                if man_rect.colliderect(el):
                    music_am.play()
                    if heart < 3:
                        heart += 1
                    list_hill.remove(el)

                if el.x < -100:
                    list_hill.remove(el)

        # стрелочки
        if keys[K_LEFT]:
            if man_x > 0:
                man_x -= 8
            screen.blit(left_move[value], (man_x, man_y))
        elif keys[K_RIGHT]:
            if man_x < 1000:
                man_x += 8
            screen.blit(right_move[value], (man_x, man_y))
        else:
            screen.blit(right_move[value], (man_x, man_y))

        # прыжок
        if not is_jump:
            if keys[K_UP]:
                is_jump = True
        else:
            if man_jump >= -10:
                if man_jump > 0:
                    man_y -= (man_jump ** 2) / 2
                else:
                    man_y += (man_jump ** 2) / 2
                man_jump -= 1
            else:
                is_jump = False
                man_jump = 10

        # изменение кадров
        frame_counter += 1
        if frame_counter == 10:  # сменяем кадр каждые 10 тиков
            value += 1
            if value == 4:
                value = 0
            frame_counter = 0

        display.update()
    elif game_window == 'fail':
        screen.fill("red")
        screen.blit(dead_label, (250, 50))
        screen.blit(fonts.render(f"Счёт: {score}", True, "white"), (420, 200))
        screen.blit(back_label, (420, 400))
        screen.blit(menu_label, (430, 550))
        display.update()
        if back_label.get_rect(topleft=(420, 400)).collidepoint(mouses) and mouse.get_pressed()[0]:
            list_ghost.clear()
            list_hill.clear()

            score = 0
            heart = 3
            kol_ghost = 0
            value = 0
            man_x = 300
            man_y = 450
            man_jump = 10
            is_jump = False
            frame_counter = 0
            game_window = 'game'

        if menu_label.get_rect(topleft=(430, 550)).collidepoint(mouses) and mouse.get_pressed()[0]:
            list_ghost.clear()
            list_hill.clear()

            score = 0
            heart = 3
            kol_ghost = 0
            value = 0
            man_x = 300
            man_y = 450
            man_jump = 10
            is_jump = False
            frame_counter = 0
            game_window = 'main'

    for e in event.get():
        if e.type == QUIT or game_window == 'quit':
            running_display = False
            quit()
        if e.type == times:

            kol_ghost += 1
            new_ghost = ghost.get_rect(topleft=(1280, 475))
            new_ghost.inflate_ip(-20, -20)  # уменьшение квадрата
            list_ghost.append(new_ghost)

            if kol_ghost == 5:
                new_hill = hill.get_rect(topleft=(2000, 475))
                new_hill.inflate_ip(-20, -20)
                list_hill.append(new_hill)
                kol_ghost = 0
