# encoding:utf-8

import sys
import numpy as np
import time
# import queue
import pygame
from pygame.locals import *


X = 30
Y = 30
cell_size = 16


class Snake():
    def __init__(self,pos = [5,5],l = 5,auto = False):
        self.pos = [pos]
        x,y = pos
        for i in range(1,l):
            y += 1
            self.pos.append([x,y])
        self.l = l
        self.auto = auto
        self.move_direction = 1

    def setting_egg(self):
        while True:
            x = np.random.choice(X)
            y = np.random.choice(Y)
            for pos in self.pos:
                if np.all(pos==np.array([x,y])):
                    break
            else:
                self.egg_pos = np.array([x,y])
                break

    def move(self,next_move = 0):
        if self.auto:
            moves = [0,1,2,3]
            if self.move_direction == 0: moves.remove(1)
            elif self.move_direction == 1: moves.remove(0)
            elif self.move_direction == 2: moves.remove(3)
            else: moves.remove(2)
            next_move = np.random.choice(moves)
            self.move_direction = next_move
        game_continue = True
        x = np.array([-1,1])
        y = np.array([-1,1])
        mov = np.array([[-1,0],[1,0],[0,-1],[0,1]]) # 0:upper 1:down 2:left 3:right
        head = self.pos[0]
        x,y = head
        n_head = head + mov[next_move]
        self.move_direction = next_move

        if n_head[0] == X:
            n_head[0] = 0
        if n_head[0] == -1:
            n_head[0] = X-1
        if n_head[1] == Y:
            n_head[1] = 0
        if n_head[1] == -1:
            n_head[1] = Y-1

        for pos in self.pos: # hit head
            if np.all(pos == n_head):
                game_continue = False
                break

        #eat egg
        if np.all(n_head == self.egg_pos):
            self.pos = [n_head] + self.pos
            self.l += 1
            self.setting_egg()
        else:
            self.pos.insert(0,n_head)
            self.pos = self.pos[:(self.l)]
        return game_continue, self.pos

    def draw_snake(self,screen,snake_pos):
        if self.auto: color = (255,224,32)
        else: color = (0,32,255)
        for i,pos in enumerate(snake_pos): # draw snake
            x,y = pos
            if i == 0:
                 # head
                pygame.draw.rect(screen,color,(x*cell_size,y*cell_size,cell_size,cell_size))
                if self.move_direction == 0 or self.move_direction == 1: eye = [0,-3]
                elif self.move_direction == 2 or self.move_direction == 3: eye = [-3,0]
                pygame.draw.circle(screen,(255,255,255),(x*cell_size+cell_size//2+eye[0],y*cell_size+cell_size//2+eye[1]),3)
            else:
                pygame.draw.rect(screen,color,(x*cell_size,y*cell_size,cell_size,cell_size))
        return screen

def main():
    snake = Snake()
    yellow_snake = Snake(pos = [20,20],l = 10,auto = True)
    game_continue = True
    pygame.init()
    screen = pygame.display.set_mode((X*cell_size,Y*cell_size))
    pygame.display.set_caption("snake game")
    move = 1
    snake.setting_egg()
    yellow_snake.egg_pos = snake.egg_pos
    for i in range(10000):
        stage = [[0 for y in range(Y)]for x in range(X)]
        screen.fill((255,255,255))
        #イベント処理
        for event in pygame.event.get():
            #終了用イベント
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #キー入力時
            if event.type == pygame.KEYDOWN:
                #終了機能
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_RIGHT and not(move == 0): move = 1
                if event.key == K_LEFT and not(move == 1): move = 0
                if event.key == K_UP and not(move==3): move = 2
                if event.key == K_DOWN and not(move == 2): move = 3

        game_continue,snake_pos = snake.move(move)
        yellow_snake.egg_pos = snake.egg_pos
        _,yellow_snake_pos = yellow_snake.move()

        screen = snake.draw_snake(screen,snake_pos)
        screen = yellow_snake.draw_snake(screen,yellow_snake_pos)

        # draw egg
        pygame.draw.rect(screen,(255,0,0),(snake.egg_pos[0]*cell_size,snake.egg_pos[1]*cell_size,cell_size,cell_size))
        pygame.display.update()
        time.sleep(0.1)
        if game_continue == False:
            print("GAME OVER")
            break

if __name__ == "__main__":
    main()
