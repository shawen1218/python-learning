import pygame
import random
import sys

# 1. 初始化游戏引擎
pygame.init()

# 2. 定义精美的彩色皮肤（RGB颜色）
COLOR_BG = (25, 25, 35)       # 深邃夜空黑（背景）
COLOR_SNAKE = (46, 204, 113)   # 翡翠绿（蛇身）
COLOR_FOOD = (231, 76, 60)     # 珊瑚红（食物）
COLOR_TEXT = (236, 240, 241)   # 纯净白（文字）
COLOR_GAME_OVER = (241, 196, 15) # 亮金黄（结束提示）

# 3. 游戏窗口尺寸与配置
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
BLOCK_SIZE = 20  # 蛇身和食物的尺寸（20x20像素网格）
GAME_SPEED = 5  # 蛇的移动速度（数字越大越快）

# 创建独立弹窗
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("莎温的独立游戏首秀：经典贪吃蛇")
clock = pygame.time.Clock()

# 4. 辅助渲染函数
def draw_snake(block_size, snake_list):
    """画出整条蛇"""
    for block in snake_list:
        pygame.draw.rect(screen, COLOR_SNAKE, [block[0], block[1], block_size, block_size], border_radius=4)

def show_info(score):
    """在左上角实时显示分数"""
    font = pygame.font.SysFont(None, 25)
    score_text = font.render(f"Score: {score}", True, COLOR_TEXT)
    screen.blit(score_text, [10, 10])

def show_message(msg, color):
    """居中弹窗文字"""
    font = pygame.font.SysFont("arial", 24, bold=True)
    text_surface = font.render(msg, True, color)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    screen.blit(text_surface, text_rect)

# 5. 核心游戏主循环
def game_loop():
    game_over = False
    game_close = False

    # 蛇的初始核心坐标（屏幕正中央）
    x = WINDOW_WIDTH / 2
    y = WINDOW_HEIGHT / 2

    # 移动速度变量
    x_change = 0
    y_change = 0

    # 蛇身结构
    snake_list = []
    snake_length = 1

    # 随机生成第一个食物，并对齐20像素网格
    food_x = round(random.randrange(0, WINDOW_WIDTH - BLOCK_SIZE) / 20.0) * 20.0
    food_y = round(random.randrange(0, WINDOW_HEIGHT - BLOCK_SIZE) / 20.0) * 20.0

    while not game_over:

        # 【死亡挂起状态】当撞墙或撞到自己时进入此循环
        while game_close:
            screen.fill(COLOR_BG)
            show_message("Game Over! Press 'C' to Play Again or 'Q' to Quit", COLOR_GAME_OVER)
            show_info(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # ✨ 新增：如果玩家点击了红叉，直接彻底退出
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # 按 Q 彻底退出
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:  # 按 C 重新开始
                        game_loop()
        # 【正常游戏状态】监听键盘上下左右控制
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = BLOCK_SIZE
                    x_change = 0

        # 边界碰撞检测（撞墙死）
        if x >= WINDOW_WIDTH or x < 0 or y >= WINDOW_HEIGHT or y < 0:
            game_close = True

        # 更新蛇头坐标
        x += x_change
        y += y_change
        
        # 渲染背景和食物
        screen.fill(COLOR_BG)
        pygame.draw.rect(screen, COLOR_FOOD, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE], border_radius=10)
        
        # 蛇身移动逻辑
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # 自身碰撞检测（咬到自己死）
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        # 绘制蛇身和分数
        draw_snake(BLOCK_SIZE, snake_list)
        show_info(snake_length - 1)
        
        # 刷新屏幕
        pygame.display.update()

        # 吃食物检测
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WINDOW_WIDTH - BLOCK_SIZE) / 20.0) * 20.0
            food_y = round(random.randrange(0, WINDOW_HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
            snake_length += 1  # 吃到食物，蛇身变长

        # 控制游戏帧率
        clock.tick(GAME_SPEED)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()