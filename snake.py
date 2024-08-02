import pygame
import time
import random
from datetime import datetime
import os


# Очищаем консоль
os.system('cls')

# Инициализация Pygame
pygame.init()


# Определение цветов
yellow = (255, 255, 102)           # Желтый цвет
color_snake = (0, 255, 0)          # Цвет змейки
red = (213, 50, 80)                # Красный цвет
color_apple = (255, 69, 0)         # Цвет яблока
color_back = (0, 0, 0)             # Цвет фона
color_info_panel = (169, 169, 169) # Цвет информационной панели
color_grid = (40, 40, 40)          # Цвет сетки


# Размеры доски и панели
board_width = 800
board_height = 600
info_panel_width = 400


# Размеры окна игры
game_width = board_width + info_panel_width
game_height = board_height


# Создание окна игры
game_wn = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption('AutoSnake by ROVA')


# Настройки игры
clock = pygame.time.Clock()
snake_block = 10  # Размер блока змеи
snake_speed = 100  # Скорость змеи
moving_now = 'None'
snake_steps = {}


# Шрифты для отображения текста
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
stats_font = pygame.font.SysFont("comicsansms", 20)


# Отображение сообщения на экране
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    game_wn.blit(mesg, [board_width / 6, board_height / 3])


# Отображение текущего счёта
def show_score(score):
    value = score_font.render("Score: " + str(score), True, yellow)
    game_wn.blit(value, [board_width + 20, 10])


# Отображение текущего времени
def show_time(start_time):
    elapsed_time = int(time.time() - start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    time_text = score_font.render("Time: {:02d}:{:02d}".format(minutes, seconds), True, yellow)
    game_wn.blit(time_text, [board_width + 20, 50])

    return "Time: {:02d}:{:02d}".format(minutes, seconds)


# Функция для сохранения скриншота
def save_screenshot():
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f')
    filename = f'./screenshots/screenshot_v3.0_{timestamp}.png'
    try:
        pygame.image.save(game_wn, filename)
        print(f"Screenshot saved successfully as {filename}")
    except pygame.error as e:
        print(f"Failed to save screenshot: {e}")


# Отображение информации о змее
def show_snake_info(cords, apple):
    if cords != None:
        percent_D = cords[0]
        percent_A = cords[1]
        percent_W = cords[2] 
        percent_S = cords[3]
        
        dir_A = stats_font.render(f'A:   {percent_A}', True, color_back)
        game_wn.blit(dir_A, [board_width + 30, 150])

        dir_D = stats_font.render(f'D:   {percent_D}', True, color_back)
        game_wn.blit(dir_D, [board_width + 30, 170])   
 
        dir_W = stats_font.render(f'W:  {percent_W}', True, color_back)
        game_wn.blit(dir_W, [board_width + 30, 190]) 

        dir_S = stats_font.render(f'S:   {percent_S}', True, color_back)
        game_wn.blit(dir_S, [board_width + 30, 210]) 

    moving_info = stats_font.render(f'Moving now: {moving_now}', True, color_back)
    game_wn.blit(moving_info, [board_width + 30, 250])


# Отображение сетки на игровом поле
def draw_grid():
    for x in range(0, game_width, snake_block):
        pygame.draw.line(game_wn, color_grid, (x, 0), (x, game_height))
    for y in range(0, game_height, snake_block):
        pygame.draw.line(game_wn, color_grid, (0, y), (game_width, y))


# Отрисовка головы и тело змеи
def our_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        if i == len(snake_list) - 1:
            pygame.draw.rect(game_wn, yellow, [x[0], x[1], snake_block, snake_block])  # Snake head color
        else:
            pygame.draw.rect(game_wn, color_snake, [x[0], x[1], snake_block, snake_block])  # Snake body color


# Отрисовка ориентировочной пути для змеи
def moving_path(snake_block, path):
    for x in path[:-1]:
        pygame.draw.rect(game_wn, color_grid, [x[0], x[1], snake_block, snake_block])      
    

# Генерация еды
def generate_food(snake_list):
    
    while True:
        foodx = round(random.randrange(0, board_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, board_height - snake_block) / 10.0) * 10.0
        
        if [foodx, foody] not in snake_list:
            break
            
    return (foodx, foody)

 
'''
Шпаргалка

return (0, -snake_block) --> w
return (0,  snake_block) --> s
return (-snake_block, 0) --> a
return ( snake_block, 0) --> d
'''

# Изменение координат для движения в заданную сторону
def controling(direction ):
    global moving_now
    if direction == 'w' : 
        # print('# w')
        moving_now = '# w'
        return (0, -snake_block)
    elif direction == 'a':
        # print('# a')
        moving_now = '# a'       
        return (-snake_block, 0)
    elif direction == 's': 
        # print('# s')
        moving_now = '# s'
        return (0, snake_block)
    elif direction == 'd': 
        # print('# d')
        moving_now = '# d'
        return (snake_block, 0)


# Функция радар : Возвращает дистанцию в процентах
def radar(snake_list):
    if len(snake_list) > 1:
        head = snake_list[-1]

        dir_D_cords = []
        dir_A_cords = []
        dir_W_cords = []
        dir_S_cords = []

        # (D)
        for x in range(snake_block, snake_block * 11, snake_block):
            new_cord_D = [head[0] + x, head[1]]
            if new_cord_D[0] < board_width and new_cord_D not in snake_list:
                dir_D_cords.append(new_cord_D)
            else:
                break

        # (A)
        for x in range(snake_block, snake_block * 11, snake_block):
            new_cord_A = [head[0] - x, head[1]]
            if new_cord_A[0] >= 0 and new_cord_A not in snake_list:
                dir_A_cords.append(new_cord_A)
            else:
                break

        # (W)
        for x in range(snake_block, snake_block * 11, snake_block):
            new_cord_W = [head[0], head[1] - x]
            if new_cord_W[1] >= 0 and new_cord_W not in snake_list:
                dir_W_cords.append(new_cord_W)
            else:
                break

        # (S)
        for x in range(snake_block, snake_block * 11, snake_block):
            new_cord_S = [head[0], head[1] + x]
            if new_cord_S[1] < board_height and new_cord_S not in snake_list:
                dir_S_cords.append(new_cord_S)
            else:
                break
        
        percent_S = len(dir_S_cords) /10
        percent_W = len(dir_W_cords) /10
        percent_D = len(dir_D_cords) /10
        percent_A = len(dir_A_cords) /10
        
        return percent_D, percent_A, percent_W, percent_S


# Логистика змеи
def snake_logistic(apple, snake_list):

    directions = {}
    if len(snake_list) > 1:
        head = snake_list[-1]

        percents = radar(snake_list)
        percent_D = percents[0]
        percent_A = percents[1]
        percent_W = percents[2] 
        percent_S = percents[3]

        if percent_D != 0:
            next_step_D = [head[0] + snake_block, head[1]]
            delta_D_x = apple[0] - next_step_D[0]
            delta_D_y = apple[1] - next_step_D[1]
            delta_D = abs(delta_D_x) + abs(delta_D_y)
            total_D = delta_D * percent_D
            directions['d'] = delta_D
            # print('D', delta_D)

        if percent_A != 0:
            next_step_A = [head[0] - snake_block, head[1]]
            delta_A_x = apple[0] - next_step_A[0]
            delta_A_y = apple[1] - next_step_A[1]
            delta_A = abs(delta_A_x) + abs(delta_A_y)
            total_A = delta_A * percent_A
            directions['a'] = delta_A
            # print('A', delta_A)

        if percent_W != 0:
            next_step_W = [head[0], head[1] - snake_block]
            delta_W_x = apple[0] - next_step_W[0]
            delta_W_y = apple[1] - next_step_W[1]
            delta_W = abs(delta_W_x) + abs(delta_W_y)
            total_W = delta_W * percent_W
            directions['w'] = delta_W
            # print('W', delta_W)

        if percent_S != 0:
            next_step_S = [head[0], head[1] + snake_block]
            delta_S_x = apple[0] - next_step_S[0]
            delta_S_y = apple[1] - next_step_S[1]
            delta_S = abs(delta_S_x) + abs(delta_S_y)
            total_S = delta_S * percent_S
            directions['s'] = delta_S
            # print('S', delta_S)

        if directions:
            min_value = min(directions.values())
            min_keys = [key for key, value in directions.items() if value == min_value]

            if len(min_keys) == 1:
                # print('min_keys', min_keys)
                # print()
                changes = controling(min_keys[0])
            else:
                # print('min_keys', min_keys)
                # print()
                big_percent = {}
                for i in min_keys:
                    if i == 'w':
                        big_percent['w'] = percent_W
                    elif i == 'a':
                        big_percent['a'] = percent_A
                    elif i == 's':
                        big_percent['s'] = percent_S
                    elif i == 'd':
                        big_percent['d'] = percent_D
                
                max_value = max(big_percent.values())
                max_keys = [key for key, value in big_percent.items() if value == max_value]

                changes = controling(max_keys[0])

            return changes


# Путь к яблоку
def road_to_apple(snake_steps, snake_list, apple):
    
    if len(snake_list) > 1:
        
        head = snake_list[-1]

        delta_x = apple[0] - head[0]
        delta_y = apple[1] - head[1]

        delta = (delta_x, delta_y)

        road = []
        snake_work_list = snake_list.copy()
        while True:
            if not road:
                head_n = head
            else:
                head_n = road[-1]
            
            if head_n[0] == apple[0] and head_n[1] == apple[1]:
                return road
            
            else:
                changes = snake_logistic(apple, snake_work_list)
                if changes:
                    x1_change, y1_change = changes

                new_head = []
                new_head.append(head_n[0] + x1_change)
                new_head.append(head_n[1] + y1_change)
                road.append(new_head)
                snake_work_list.append(new_head)


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Основная функция игры
def gameLoop():
    game_over = False
    game_close = False
    paused = False
    view_mode = True

    # Появление змеи по центру
    x1 = board_width / 2 - snake_block 
    y1 = board_height / 2 - snake_block

    x1_change = snake_block # первым шагом ходить в право, чтобы хвост тоже мог появится
    y1_change = 0

    # Координаты всех частей змеи на карте
    snake_list = []
    length_of_snake = 2

    score = 0
    start_time = time.time()

    apple = generate_food(snake_list)

    snake_steps[apple] = {}
    snake_steps[apple]['steps'] = []


    # Основной процесс
    while not game_over:
                    
        if game_close:
            # При завершении игры сохранение screenshot и добавить результат в статистику
            save_screenshot()
            with open('statistic#3.txt', 'a') as stats:
                stats = stats.write(f'Score:{score} | Speed:{snake_speed} | {show_time(start_time)}\n')
            exit()
        
        while game_close:
            game_wn.fill(color_back)
            message("Вы проиграли! R -> повтор | Esc -> выход", red)
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_d and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_w and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_s and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_v:
                    if view_mode == True:
                        view_mode = False
                    else:
                        view_mode = True

        if paused:
            message("Пауза. Нажмите Space для продолжения", yellow)
            pygame.display.update()
            continue
        
        # Изменение для следующего шага змеи
        changes = snake_logistic(apple, snake_list)
        if changes:
            x1_change, y1_change = changes

        x1 += x1_change
        y1 += y1_change

        # При столкновении со стеной -> смерт
        if x1 >= board_width or x1 < 0 or y1 >= board_height or y1 < 0:
            game_close = True

        game_wn.fill(color_back)
        if view_mode:
            draw_grid()
        pygame.draw.rect(game_wn, color_apple, [apple[0], apple[1], snake_block, snake_block])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_list)

        pygame.draw.rect(game_wn, color_info_panel, [board_width, 0, info_panel_width, board_height])
        show_score(score)
        show_time(start_time)
        if view_mode:
            show_snake_info(radar(snake_list), apple)
            if len(snake_list) > 1:
                moving_path(snake_block, path = road_to_apple(snake_steps, snake_list, apple))

        pygame.display.update()

        if x1 == apple[0] and y1 == apple[1]:
            del  snake_steps[apple]

            apple = generate_food(snake_list)

            snake_steps[apple] = {}
            snake_steps[apple]['steps'] = []

            length_of_snake += 1
            score += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
