#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 21:49:29 2024

@author: 67degrees
"""

import pygame
from random import randrange
from time import sleep

pygame.init()

frame = 0  # 当前帧
map_width = 284
map_height = 512
FPS = 60  # 屏幕刷新率 60帧每秒
pipes = [[150, 4]]  # 管道坐标， 管道开口位置
bird = [40, map_height // 2 - 50]
gravity = 1.5
velocity = 0
score = 0  # Score variable

# Set up the screen
gameScreen = pygame.display.set_mode((map_width, map_height))
clock = pygame.time.Clock()  # 时间函数

# Load images
bird_wing_up = pygame.image.load("image/bird2.png")  # 小鸟翅膀图片
bird_wing_down = pygame.image.load("image/bird1.png")  # 小鸟翅膀放下来图片
background = pygame.image.load("image/background.png")
pipe_body = pygame.image.load("image/pipe_body.png")
pipe_end = pygame.image.load("image/pipe_end.png")

# Set up font for score
font = pygame.font.Font(None, 36)

def draw_pipes():
    global pipes
    for n in range(len(pipes)):
        for m in range(pipes[n][1]):  # 从第0个管道的开口画到第0个管道的开口
            gameScreen.blit(pipe_body, (pipes[n][0], m * 32))
        for m in range(pipes[n][1] + 6, 16):  # 从开口的末尾画到管道的末尾
            gameScreen.blit(pipe_body, (pipes[n][0], m * 32))

        gameScreen.blit(pipe_end, (pipes[n][0], (pipes[n][1]) * 32))  # 添加管道的末端
        gameScreen.blit(pipe_end, (pipes[n][0], (pipes[n][1] + 5) * 32))
        pipes[n][0] -= 1

def draw_bird(x, y):  # 小鸟动画
    global frame  # 全局变量
    if 0 <= frame <= 30:
        gameScreen.blit(bird_wing_up, (x, y))
        frame += 1
    elif 30 <= frame <= 60:
        gameScreen.blit(bird_wing_down, (x, y))
        frame += 1
        if frame == 60:
            frame = 0

def safe():
    if bird[1] > map_height - 35:  # 小鸟坐标在屏幕之内
        print("hit floor")
        return False
    if bird[1] < 0:  # 达到顶端
        print("hit ceiling")
        return False
    if pipes[0][0] - 30 < bird[0] < pipes[0][0] + 79:
        if bird[1] < (pipes[0][1] + 1) * 32 or bird[1] > (pipes[0][1] + 4) * 32:
            print("hit pipe")
            return False
    return True

# 新增变量
score = 0  # 当前分数
highest_score = 0  # 最高分

def startScreen():
    global highest_score
    font = pygame.font.SysFont(None, 48)  # 设置字体
    title_text = font.render("Flappy Bird", True, (255, 255, 255))
    highest_score_text = font.render(f"Highest Score: {highest_score}", True, (255, 255, 255))
    instruction_text = pygame.font.SysFont(None, 36).render(
        "Press any key to start", True, (255, 255, 255)
    )
    
    while True:
        gameScreen.blit(background, (0, 0))  # 显示背景
        gameScreen.blit(title_text, (map_width // 2 - title_text.get_width() // 2, 100))
        gameScreen.blit(highest_score_text, (map_width // 2 - highest_score_text.get_width() // 2, 200))
        gameScreen.blit(instruction_text, (map_width // 2 - instruction_text.get_width() // 2, 300))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # 按下任意键开始游戏
                return
            if event.type == pygame.QUIT:  # 退出游戏
                pygame.quit()
                return

def reset():
    global frame, map_width, map_height, FPS, pipes, bird, gravity, velocity, score
    global highest_score

    if score > highest_score:  # 更新最高分
        highest_score = score

    frame = 0
    map_width = 284
    map_height = 512
    FPS = 60
    pipes.clear()
    bird.clear()
    pipes = [[180, 4]]
    bird = [40, map_height // 2 - 50]
    gravity = 1.5
    velocity = 0
    score = 0  # 重置分数

    # 回到起始页面
    startScreen()


def gameLoop():
    global score, highest_score, passed_pipe

    passed_pipe = False  # 当前管道通过标志

    startScreen()  # 显示开始页面

    while True:
        if len(pipes) < 4:
            x = pipes[-1][0] + 200
            open_pos = randrange(1, 9)
            pipes.append([x, open_pos])
        if pipes[0][0] < -100:
            pipes.pop(0)
            passed_pipe = False  # 重置当前管道通过标志

        # 检查鸟是否通过当前管道
        if not passed_pipe and pipes[0][0] + 79 < bird[0]:  # 鸟完全超过管道
            score += 1  # 增加分数
            passed_pipe = True  # 标记当前管道已计分

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                bird[1] -= 40
                velocity = 0

            if event.type == pygame.QUIT:
                pygame.quit()
                return

        velocity = 0
        velocity += gravity

        bird[1] += velocity
        gameScreen.blit(background, (0, 0))
        draw_pipes()
        draw_bird(bird[0], bird[1])

        # 绘制分数和最高分
        font = pygame.font.SysFont(None, 36)  # 定义字体
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        highest_score_text = font.render(f"Highest Score: {highest_score}", True, (255, 255, 255))
        gameScreen.blit(score_text, (10, 10))
        gameScreen.blit(highest_score_text, (10, 50))

        pygame.display.update()

        if not safe():
            sleep(3)
            reset()  # 重置游戏，并返回到起始页面

        clock.tick(FPS)


# 主程序
if __name__ == "__main__":
    gameLoop()
