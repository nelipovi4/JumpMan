from pygame import *

init()

clock = time.Clock()

screen = display.set_mode((807, 403))
display.set_caption("Игра")

running_display = True

left_move = [
	image.load("img/movement/left_1.png"),
	image.load("img/movement/left_2.png"),
	image.load("img/movement/left_3.png"),
	image.load("img/movement/left_4.png"),
]

right_move = [
	image.load("img/movement/right_1.png"),
	image.load("img/movement/right_2.png"),
	image.load("img/movement/right_3.png"),
	image.load("img/movement/right_4.png"),
]

bg = image.load("img/bg.jpg")
bg_x1 = 0
bg_x2 = bg.get_width()
value = 0
left = False
right = False
frame_count = 0

while running_display:
	keys = key.get_pressed()

	# Очистка экрана
	screen.fill((0, 0, 0))

	# Отрисовка фона
	screen.blit(bg, (bg_x1, 0))
	screen.blit(bg, (bg_x2, 0))

	bg_x1 -= 5
	bg_x2 -= 5

	# Перемещение фона
	if bg_x1 <= -bg.get_width():
		bg_x1 = bg.get_width()
	if bg_x2 <= -bg.get_width():
		bg_x2 = bg.get_width()

	if keys[K_LEFT]:
		left = True
		right = False
		frame_count += 1
	elif keys[K_RIGHT]:
		right = True
		left = False
		frame_count += 1
	else:
		left = False
		right = False
		frame_count = 0

	if left:
		screen.blit(left_move[value], (300, 200))
	elif right:
		screen.blit(right_move[value], (300, 200))
	else:
		screen.blit(image.load("img/movement/face.png"), (300, 200))

	if frame_count >= 5:
		value += 1
		if value == 4:
			value = 0
		frame_count = 0

	display.update()
	clock.tick(30)
	for e in event.get():
		if e.type == QUIT:
			running_display = False
			quit()
