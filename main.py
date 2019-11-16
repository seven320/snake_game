# encoding:utf-8

import sys
import numpy as np
import time
# import queue
import pygame
from pygame.locals import *
import copy


X = 20
Y = 20
cell_size = 20
display_w,display_h = X*cell_size, Y*cell_size

class Snake():
    def __init__(self,pos = [5,5],l = 7,auto = False):
        self.pos = [pos]
        x,y = pos
        for i in range(1,l):
            y += 1
            self.pos.append([x,y])
        self.l = l
        self.auto = auto
        self.move_direction = 1
        self.yellow_snake_pos = []

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

        for pos in self.pos+self.yellow_snake_pos: # hit head
            if np.all(pos == n_head):
                gameover = True
                break
        else:
            gameover = False

        #eat egg
        if np.all(n_head == self.egg_pos):
            self.pos = [n_head] + self.pos
            self.l += 1
            self.setting_egg()
        else:
            self.pos.insert(0,n_head)
            self.pos = self.pos[:(self.l)]
        return gameover

    def draw_snake(self,screen,snake_pos):
        if self.auto: color = (255,224,32)
        else: color = (0,32,255)
        for i,pos in enumerate(snake_pos): # draw snake
            x,y = pos
            if i != 0:
                pygame.draw.rect(screen,color,(x*cell_size,y*cell_size,cell_size,cell_size))
            else:
                x_head,y_head = x,y
        # head
        pygame.draw.rect(screen,color,(x_head*cell_size,y_head*cell_size,cell_size,cell_size))
        if self.move_direction == 0 or self.move_direction == 1: eye = [0,-3]
        elif self.move_direction == 2 or self.move_direction == 3: eye = [-3,0]
        pygame.draw.circle(screen,(255,255,255),(x_head*cell_size+cell_size//2+eye[0],y_head*cell_size+cell_size//2+eye[1]),3)
        return screen

class Snake_game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((display_w,display_h))
        pygame.display.set_caption(u"snake game!")
        self.init_game()
        move = 1
        while True:
            self.update()
            self.draw(self.screen)

    def update(self):
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
                if event.key == K_SPACE and self.game_state == "START": self.game_state = "PLAY" # game start
                if event.key == K_SPACE and self.game_state == "GAMEOVER": self.init_game() # game start
                if self.game_state == "PLAY":
                    if event.key == K_h and not(self.move == 1): self.move = 0
                    if event.key == K_j and not(self.move == 2): self.move = 3
                    if event.key == K_k and not(self.move==3): self.move = 2
                    if event.key == K_l and not(self.move == 0): self.move = 1
                    if event.key == K_RIGHT and not(self.move == 0): self.move = 1
                    if event.key == K_LEFT and not(self.move == 1): self.move = 0
                    if event.key == K_UP and not(self.move==3): self.move = 2
                    if event.key == K_DOWN and not(self.move == 2): self.move = 3

        self.snake.yellow_snake_pos = self.yellow_snake.pos
        gameover = self.snake.move(self.move)
        if gameover:
            self.game_state = "GAMEOVER"
        self.yellow_snake.egg_pos = self.snake.egg_pos
        self.yellow_snake.move()
        time.sleep(self.sleep_time)

    def text_objects(self,text, font):
        textSurface = font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect()

    def draw(self,screen):
        self.screen.fill((255,255,255))
        title_font = pygame.font.Font("freesansbold.ttf",30)
        sub_title_font = pygame.font.Font("freesansbold.ttf",20)
        sub_sub_title_font = pygame.font.Font("freesansbold.ttf",10)
        if self.game_state == "START":
            python_img = pygame.image.load("python.png")
            self.screen.blit(python_img,(display_h/8,display_w/8))
            TextSurf,TextRect = self.text_objects("Python SNAKE GAME", title_font)
            TextRect.center = ((display_w/2),(display_h*0.15))
            self.screen.blit(TextSurf,TextRect)
            TextSurf,TextRect = self.text_objects("START", sub_title_font)
            TextRect.center = ((display_w/2,display_h*0.9))
            # self.screen.blit(TextSurf,TextRect)
            TextSurf,TextRect = self.text_objects("push space button to start", sub_title_font)
            TextRect.center = ((display_w/2),(display_h*0.9))
            self.screen.blit(TextSurf,TextRect)

        elif self.game_state == "PLAY":
            self.screen = self.snake.draw_snake(self.screen,self.snake.pos)
            self.screen = self.yellow_snake.draw_snake(self.screen,self.yellow_snake.pos)
            # draw egg
            pygame.draw.rect(self.screen,(255,0,0),(self.snake.egg_pos[0]*cell_size,self.snake.egg_pos[1]*cell_size,cell_size,cell_size))

        elif self.game_state == "GAMEOVER": # GAME OVERを描画
            self.screen = self.snake.draw_snake(self.screen,self.snake.pos)
            self.screen = self.yellow_snake.draw_snake(self.screen,self.yellow_snake.pos)
            # draw egg
            pygame.draw.rect(self.screen,(255,0,0),(self.snake.egg_pos[0]*cell_size,self.snake.egg_pos[1]*cell_size,cell_size,cell_size))
            TextSurf,TextRect = self.text_objects("GAME OVER", sub_title_font)
            TextRect.center = ((display_w/2),(display_h/2))
            self.screen.blit(TextSurf,TextRect)
            TextSurf,TextRect = self.text_objects("push space button to restart", sub_title_font)
            TextRect.center = ((display_w/2),(display_h*0.6))
            self.screen.blit(TextSurf,TextRect)

        pygame.display.update()

    def init_game(self):
        self.snake = Snake()
        self.yellow_snake = Snake(pos = [10,10],l = 5,auto = True)
        self.move = 1
        self.snake.setting_egg()
        self.yellow_snake.egg_pos = self.snake.egg_pos
        self.yellow_snake_pos = []
        self.game_state = "START"
        self.sleep_time = 0.1

def main():
    game = Snake_game()
    return 0

if __name__ == "__main__":
    main()
