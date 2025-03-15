import tkinter as tk
from random import randint
from random import randrange
from math import sqrt


BATTLEFIELD_WIGTH = 800
BATTLEFIELD_HEIGHT = 600
TIME_DELAY = 20 #miliseconods


def main() -> None:
    global event, canvas, target, gun, ball, root
    root = tk.Tk()
    root.title('Game: Guns')
    root.geometry(f'{BATTLEFIELD_WIGTH}x{BATTLEFIELD_HEIGHT}')
    canvas = tk.Canvas(bg='white', width=BATTLEFIELD_WIGTH, height=BATTLEFIELD_HEIGHT)
    canvas.pack(anchor=tk.CENTER, expand=1)
    
    target = Target()
    gun = Gun()
    gun.gun_move()
    target.move_target()

    canvas.bind('<Button-1>', mouse_click)
    print(canvas.coords(gun.id), type(canvas.coords(gun.id)))
    root.mainloop()
    print('Goodbye!') #Say it in shell after close window


def mouse_click(event):#TEST
    global target, canvas, ball, root
    ball = Ball()
    ball.shot_ball()
    gun.gun_move()
    print('click', event)


class NewGame:
    def __init__(self):
        pass

    def create_target(self):
        pass

    def create_ball(self):
        pass

    def create_gun(self):
        pass

class Target:
    FIRST_VELOCITY_X = -1
    FIRST_VELOCITY_Y = 5

    def __init__(self):
        self.x = randint(650, 750)
        self.y = randint(50, 550)
        self.r = randint(5, 50)
        self.dx = self.FIRST_VELOCITY_X
        self.dy = self.FIRST_VELOCITY_Y
        self.color = 'green'
        self.id = canvas.create_oval(self.x - self.r, self.y - self.r,
                                     self.x + self.r, self.y + self.r, fill=self.color)

    def destroy_target(self):
        canvas.delete(self.id) 

    def move_target(self):
        canvas.move(self.id, self.dx, self.dy)
        self.x += self.dx
        self.y += self.dy
        if self.y >= BATTLEFIELD_HEIGHT - self.r or self.y <= self.r:
            self.dy = -self.dy
        root.after(TIME_DELAY, self.move_target)


class Gun:
    FIRST_POINT_X = 20
    FIRST_POINT_Y = 400
    WIDTH = 6
    GUN_LENGTH = 50

    def __init__(self):
        self.second_point_x = self.FIRST_POINT_X + self.GUN_LENGTH
        self.second_point_y = self.FIRST_POINT_Y
        self.id = canvas.create_line(self.FIRST_POINT_X, self.FIRST_POINT_Y, 
                                     self.second_point_x, self.second_point_y, 
                                     width=self.WIDTH)

    def destroy_gun(self):
        canvas.delete(self.id)

    def gun_move(self):
        x_mouse = canvas.winfo_pointerx() - canvas.winfo_rootx() # coordinates of mouse on canvas
        y_mouse = canvas.winfo_pointery() - canvas.winfo_rooty()
        x_vector_mouse = x_mouse - self.FIRST_POINT_X # mouse coordinates relative to FIRST_POINT of gun
        y_vector_mouse = y_mouse - self.FIRST_POINT_Y
        hypotenuse = sqrt((x_vector_mouse)**2 + (y_vector_mouse)**2)
        x_ratio = x_vector_mouse / hypotenuse
        y_ratio = y_vector_mouse / hypotenuse
        self.second_point_x = self.FIRST_POINT_X + x_ratio * self.GUN_LENGTH
        self.second_point_y = self.FIRST_POINT_Y + y_ratio * self.GUN_LENGTH
        canvas.coords(gun.id, self.FIRST_POINT_X, self.FIRST_POINT_Y, self.second_point_x, self.second_point_y)
        root.after(TIME_DELAY, gun.gun_move)
        return (x_ratio, y_ratio)


class Ball:
    RADIUS_BALL = 10
    FIRST_IMPULSE = 20
    COLOR = 'red'

    def __init__(self):
        self.first_impulse = self.FIRST_IMPULSE
        self.x = gun.second_point_x
        self.y = gun.second_point_y
        self.dx = self.first_impulse * gun.gun_move()[0]
        self.dy = self.first_impulse * gun.gun_move()[1]
        self.r = self.RADIUS_BALL
        self.id = canvas.create_oval(self.x - self.r, self.y - self.r,
                                     self.x + self.r, self.y + self.r, fill=self.COLOR)

    def destroy_ball(self):
        canvas.delete(self.id)

    def shot_ball(self):
        canvas.move(self.id, self.dx, self.dy)
        self.x += self.dx
        self.y += self.dy
        print(self.y, self.dy)
        if (self.y >= BATTLEFIELD_HEIGHT - self.r - 1) and self.dy <= 1: # fix bug, ball fall under low border
            self.dy = 0
        elif (self.y >= BATTLEFIELD_HEIGHT - self.r - self.dy) or self.y <= self.r:
            self.dy -= 1 # ball jump lower and lower
            self.dy = -self.dy
        else:
            self.dy += 1 # It's give effect gravitation
        self.hit_test()
        if self.x < 0 or self.x > BATTLEFIELD_WIGTH: # need added " - self.r" for destroy ball abroad border
            self.destroy_ball()
        root.after(TIME_DELAY, self.shot_ball)

    def hit_test(self):
        if int(sqrt((target.x - self.x)**2 + (target.y - self.y)**2)) <= target.r + self.r:
            target.destroy_target()





if __name__ == '__main__':
    main()

