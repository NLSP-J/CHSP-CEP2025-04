import pygame as pg
import random, time
pg.init()
clock = pg.time.Clock()
import asyncio

black = (0, 0, 0)

win_width = 800
win_height = 600
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Falling Debris')

font = pg.font.Font(None, 30)
speed = 10
score = 0
running = True

player_size = 40
player_pos = [win_width / 2, win_height - player_size]  # 400, 600-40
player_image = pg.image.load('./assets/images/mario.png')
player_image = pg.transform.scale(player_image, (player_size, player_size))  # 40,40

obj_size = 60
obj_data = []     # List to store object positions and their images
obj = pg.image.load('./assets/images/C_rock-RRR.png')
obj = pg.transform.scale(obj, (obj_size, obj_size))

bg_image = pg.image.load('./assets/images/cave123.jpg')
bg_image = pg.transform.scale(bg_image, (win_width, win_height))

def myscript():
        bg_image = pg.image.load('./assets/images/dizzymario.jpg')
        bg_image = pg.transform.scale(bg_image, (win_width, win_height))
        screen.blit(bg_image, (0, 0))
        pg.display.flip()

def create_object(obj_data):
    if len(obj_data) < 10 and random.random() < 0.1:            
        x = random.randint(0, win_width - obj_size)
        y = 0                                         
        obj_data.append([x, y, obj])


def update_objects(obj_data):
    global score

    for object in obj_data:
        x, y, image_data = object
        if y < win_height:
            y += speed
            object[1] = y
            screen.blit(image_data, (x, y))
        else:
            obj_data.remove(object)
            score += 1


def collision_check(obj_data, player_pos):
    global running
    for object in obj_data:
        x, y, image_data = object
        player_x, player_y = player_pos[0], player_pos[1]
        obj_rect = pg.Rect(x, y, obj_size, obj_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(obj_rect):
            time.sleep(0.1)
            myscript()
            time.sleep(2)
            running = False
            break

async def main():
    global running, player_pos
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= 7
        if keys_pressed[pg.K_RIGHT] and player_pos[0] < win_width - player_size:
            player_pos[0] += 7

        screen.blit(bg_image, (0, 0))
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        text = f'Score: {score}'
        text = font.render(text, 10, black)
        screen.blit(text, (win_width - 200, win_height - 40))

        create_object(obj_data)
        update_objects(obj_data)
        collision_check(obj_data, player_pos)

        clock.tick(30)
        pg.display.flip()

        await asyncio.sleep(0)

asyncio.run(main())