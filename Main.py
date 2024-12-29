from pygame import *

init()
clock = time.Clock()
kol_ghost = 0
heart = 3

music_damage = mixer.Sound("music/fun_damage.mp3")
music_am = mixer.Sound("music/fun_am.mp3")

screen = display.set_mode((1280, 720))
display.set_caption("Игра")
running_display = True
fonts = font.Font('font/ofont.ru_Zeitmax.ttf', 100)
font_point = font.Font('font/ofont.ru_Etude Noire.ttf', 35)
dead_label = fonts.render(f"Вы проиграли!", True, "black")
back_label = fonts.render("Заново", True, "white")
game_window = True

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
times = USEREVENT + 1
time.set_timer(times, 1700)


while running_display:
    keys = key.get_pressed()
    mouses = mouse.get_pos()
    # Анимация фона
    screen.blit(bg, (bg_x1, 0))
    screen.blit(bg, (bg_x1 + 1280, 0))

    if bg_x1 == -1280:
        bg_x1 = 0
    bg_x1 -= 5
    if game_window:
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
                        game_window = False
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
        clock.tick(80)
    else:
        screen.fill("red")
        back_rect = back_label.get_rect(topleft=(430, 600))
        screen.blit(dead_label, (250, 200))
        screen.blit(fonts.render(f"Счёт: {score}", True, "white"), (420, 400))
        screen.blit(back_label, (430, 600))
        display.update()
        if back_rect.collidepoint(mouses) and mouse.get_pressed()[0]:
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
            game_window = True

    for e in event.get():
        if e.type == QUIT:
            running_display = False
            quit()
        if e.type == times:

            kol_ghost += 1
            new_ghost = ghost.get_rect(topleft=(1280, 475))
            new_ghost.inflate_ip(-20, -20)
            list_ghost.append(new_ghost)

            if kol_ghost == 5:
                new_hill = hill.get_rect(topleft=(2000, 475))
                new_hill.inflate_ip(-20, -20)
                list_hill.append(new_hill)
                kol_ghost = 0
