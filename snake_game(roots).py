import pygame
import time
import random

# تنظیمات اولیه pygame
pygame.init()

# رنگ‌ها
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# ابعاد صفحه
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# تنظیمات بازی
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

# فونت‌ها
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# وضعیت تمام‌صفحه
is_fullscreen = False

# تابع نمایش امتیاز
def show_score(score):
    score_text = score_font.render(f"Score: {score}", True, black)
    dis.blit(score_text, [dis_width - 150, 0])

# تابع نمایش تایمر
def show_timer(timer):
    timer_text = font_style.render(f"Time: {timer:.1f} s", True, black)
    dis.blit(timer_text, [10, 10])

# تابع نمایش مار
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

# تابع پیام
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

# تابع تغییر حالت تمام‌صفحه
def toggle_fullscreen():
    global is_fullscreen, dis
    if is_fullscreen:
        dis = pygame.display.set_mode((dis_width, dis_height))
        is_fullscreen = False
    else:
        dis = pygame.display.set_mode((dis_width, dis_height), pygame.FULLSCREEN)
        is_fullscreen = True

# صفحه اصلی (Home)
def home_screen():
    home = True
    while home:
        dis.fill(blue)
        message("Welcome to Snake Game! Press S to Start, F for Fullscreen, Q to Quit", white)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    home = False  # شروع بازی
                elif event.key == pygame.K_f:
                    toggle_fullscreen()  # تمام‌صفحه
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# حلقه اصلی بازی
def gameLoop():
    game_over = False
    game_close = False

    # موقعیت اولیه مار
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    score = 0

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # تایمر غذا
    food_timer = 10
    start_time = time.time()
    game_start_time = time.time()  # زمان شروع بازی

    while not game_over:
        while game_close:
            dis.fill(blue)
            message("You Lost! Press C to Play Again or Q to Quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_f:  # کلید 'F' برای تغییر حالت تمام‌صفحه
                    toggle_fullscreen()

        # برخورد با لبه‌ها
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # برخورد مار با خودش
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)

        # مدیریت تایمر غذا
        current_time = time.time()
        elapsed_time = current_time - start_time
        if x1_change != 0 or y1_change != 0:  # زمانی که مار در حال حرکت است
            remaining_time = max(food_timer - elapsed_time, 0)
        else:  # زمانی که مار در حال حرکت نیست
            remaining_time = max(food_timer - (current_time - game_start_time), 0)

        # نمایش تایمر
        show_timer(remaining_time)
        show_score(score)

        pygame.display.update()

        if remaining_time <= 0:
            game_close = True

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score += 10
            start_time = time.time()  # ریست تایمر غذا
            game_start_time = time.time()  # زمان شروع بازی جدید

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# شروع برنامه
home_screen()
gameLoop()