#!/usr/bin/env python3

import tkinter as tk
from random import randint, choice
from random import randrange
from time import sleep
from math import sqrt


BATTLEFIELD_WIGTH = 800
BATTLEFIELD_HEIGHT = 600
TIME_DELAY = 20 # Miliseconods


from tkinter import font
 
def main() -> None:
    global canvas

    root = tk.Tk()
    root.title('Game: Guns')
    root.geometry(f'{BATTLEFIELD_WIGTH}x{BATTLEFIELD_HEIGHT}')

    canvas = tk.Canvas(bg='white', width=BATTLEFIELD_WIGTH, height=BATTLEFIELD_HEIGHT)
    canvas.pack(anchor=tk.CENTER, expand=1)

    game = Game(Target, Gun, Ball, root)

    main_menu = tk.Menu()

    game_menu = tk.Menu()
    game_menu.add_command(label='Exit', command=exit)

    main_menu.add_cascade(label='Game menu', menu=game_menu)
    root.config(menu=main_menu)

    canvas.bind('<ButtonPress-1>', game.mouse_click)
    canvas.bind('<ButtonRelease-1>', game.mouse_unclick)

    root.mainloop()



class Game:
    GAME_OVER_SLEEP = 5
    PROBABILITY_SPAWN_TARGET = 100 # Than number more, that probability less
    INIT_SCORE = 20 
    SCORE_LOSS = 1
    SCORE_GAIN = 2
    Y_TEXT_SCORE = 30
    FONT_SCORE = "Arial 40"

    def __init__(self, Target, Gun, Ball, root):
        """In targets[] and balls[] addresses of class objects are stored"""
        self.root = root
        self.targets = []
        self.balls = []
        self.gun = Gun()
        self.mouse_btn_keep = False
        self.score = self.INIT_SCORE
        self.time_handler(root)
        self.id_score = canvas.create_text((BATTLEFIELD_WIGTH / 2), self.Y_TEXT_SCORE,
                                           font=self.FONT_SCORE, text=f'Score: {self.score}')

    def time_handler(self, root):
        if randint(1, self.PROBABILITY_SPAWN_TARGET) == 1: self.targets.append(Target())
        self.gun.move_gun()
        if self.score == 0:
            self.game_over()
            return
        for target in self.targets: 
            score = target.move_target(self.targets, target, self.score)
        for ball in self.balls: ball.move_ball(self.balls, ball)
        for target in self.targets: 
            for ball in self.balls:
                if self.hit_test(target, ball):
                    self.score += self.SCORE_GAIN
                    self.refresh_score()
        root.after(TIME_DELAY, lambda a=root: self.time_handler(a))

    def mouse_unclick(self, event):
        self.mouse_btn_keep = False
        self.balls.append(Ball(self.gun))
        self.score -= self.SCORE_LOSS
        self.refresh_score()
        print('click', event) # TEST

    def mouse_click(self, event):
        self.mouse_btn_keep = True
        self.mouse_keep()

    def mouse_keep(self):
        if self.mouse_btn_keep:
            if self.gun.power < self.gun.MAX_POWER:
                self.gun.power += 1
            print(self.gun.power) # TEST
            canvas.after(TIME_DELAY, self.mouse_keep)

    def hit_test(self, target, ball):
        if int(sqrt((target.x - ball.x)**2 + (target.y - ball.y)**2)) <= target.r + ball.r:
            target.destroy_target(self.targets, target)
            ball.destroy_ball(self.balls, ball)
            return 1
        return 0

    def refresh_score(self):
        canvas.itemconfig(self.id_score, text=f'Score: {self.score}')

    def game_over(self):
        canvas.create_text((BATTLEFIELD_WIGTH / 2), (BATTLEFIELD_HEIGHT / 2),
                           font=self.FONT_SCORE, text=f'GAME OVER')


class Target:
    FIRST_VELOCITY_X = -1
    FIRST_VELOCITY_Y = 5
    COLORS_TARGET = ['green', 'red', 'blue', 'yellow']
    PENALTY_LOSS_TARGET = 3
    LEFT_BORDER_SPAWN = 650
    RIGHT_BORDER_SPAWN = 750
    UP_BORDER_SPAWN = 50
    LOW_BORDER_SPAWN = 550
    MAX_RADIUS = 50
    MIN_RADIUS = 10

    def __init__(self):
        self.x = randint(self.LEFT_BORDER_SPAWN, self.RIGHT_BORDER_SPAWN)
        self.y = randint(self.UP_BORDER_SPAWN, self.LOW_BORDER_SPAWN)
        self.r = randint(self.MIN_RADIUS, self.MAX_RADIUS)
        self.dx = self.FIRST_VELOCITY_X
        self.dy = self.FIRST_VELOCITY_Y
        self.color = choice(self.COLORS_TARGET)
        self.id = canvas.create_oval(self.x - self.r, self.y - self.r,
                                     self.x + self.r, self.y + self.r, fill=self.color)

    def destroy_target(self, targets, target):
        canvas.delete(self.id) 
        targets.remove(target)

    def move_target(self, targets, target, score):
        canvas.move(self.id, self.dx, self.dy)
        self.x += self.dx
        self.y += self.dy
        if self.y >= BATTLEFIELD_HEIGHT - self.r or self.y <= self.r:
            self.dy = -self.dy
        if self.x <= 0 or self.x >= BATTLEFIELD_WIGTH:
            self.destroy_target(targets, target)
            return (score - self.PENALTY_LOSS_TARGET)
        return score


class Gun:
    FIRST_POINT_X = 20
    FIRST_POINT_Y = 400
    GUN_WIDTH = 5
    GUN_LENGTH = 50
    FIRST_POWER = 0
    MAX_POWER = 50

    def __init__(self):
        self.second_point_x = self.FIRST_POINT_X + self.GUN_LENGTH
        self.second_point_y = self.FIRST_POINT_Y
        self.x_ratio = 1
        self.y_ratio = 0
        self.power = self.FIRST_POWER 
        self.id = canvas.create_line(self.FIRST_POINT_X, self.FIRST_POINT_Y, 
                                     self.second_point_x, self.second_point_y, 
                                     width=self.GUN_WIDTH)

    def destroy_gun(self, gun):
        canvas.delete(self.id)
        del gun

    def move_gun(self):
        x_mouse = canvas.winfo_pointerx() - canvas.winfo_rootx() # Coordinates of mouse on canvas
        y_mouse = canvas.winfo_pointery() - canvas.winfo_rooty()
        x_vector_mouse = x_mouse - self.FIRST_POINT_X # Mouse coordinates relative to FIRST_POINT of gun
        y_vector_mouse = y_mouse - self.FIRST_POINT_Y
        hypotenuse = sqrt((x_vector_mouse)**2 + (y_vector_mouse)**2)
        self.x_ratio = x_vector_mouse / hypotenuse
        self.y_ratio = y_vector_mouse / hypotenuse
        self.second_point_x = self.FIRST_POINT_X + self.x_ratio * (self.GUN_LENGTH + self.power)
        self.second_point_y = self.FIRST_POINT_Y + self.y_ratio * (self.GUN_LENGTH + self.power)
        canvas.coords(self.id, self.FIRST_POINT_X, self.FIRST_POINT_Y, self.second_point_x, self.second_point_y)


class Ball:
    RADIUS_BALL = 10
    FIRST_IMPULSE = 10
    COLOR = 'red'
    LOSS_IMPULSE = 1
    GRAVITATION = 1

    def __init__(self, gun):
        self.first_impulse = self.FIRST_IMPULSE + gun.power
        gun.power = gun.FIRST_POWER
        self.x = gun.second_point_x
        self.y = gun.second_point_y
        self.dx = self.first_impulse * gun.x_ratio
        self.dy = self.first_impulse * gun.y_ratio
        self.r = self.RADIUS_BALL
        self.id = canvas.create_oval(self.x - self.r, self.y - self.r,
                                     self.x + self.r, self.y + self.r, fill=self.COLOR)

    def destroy_ball(self, balls, ball):
        canvas.delete(self.id)
        balls.remove(ball)

    def move_ball(self, balls, ball):
        canvas.move(self.id, self.dx, self.dy)
        self.x += self.dx
        self.y += self.dy
        if (self.y >= BATTLEFIELD_HEIGHT - self.r - 1) and self.dy <= 1: # This fix bug, when ball fall under border
            self.dy = 0
        elif (self.y >= BATTLEFIELD_HEIGHT - self.r - self.dy) or self.y <= self.r:
            self.dy -= self.LOSS_IMPULSE 
            self.dy = -self.dy
        else:
            self.dy += self.GRAVITATION
        if self.x < 0 or self.x > BATTLEFIELD_WIGTH: # Need added " - self.r" for destroy ball abroad border
            self.destroy_ball(balls, ball)
            return


if __name__ == '__main__':
    main()

