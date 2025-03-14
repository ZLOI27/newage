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
    canvas.bind('<Button-3>', mouse_click2)
    print(canvas.coords(gun.id), type(canvas.coords(gun.id)))
    root.mainloop()
    print('Goodbye!') #Say it in shell after close window



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
    def __init__(self):
        self.x = randint(650, 750)
        self.y = randint(50, 550)
        self.r = randint(5, 50)
        self.dx = 0
        self.dy = 5
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


class Ball:
    RADIUS_BALL = 10

    def __init__(self):
        self.x = gun.second_point_x
        self.y = gun.second_point_y
        self.dx = 4
        self.dy = 0
        self.r = self.RADIUS_BALL
        self.color = 'red'
        self.id = canvas.create_oval(self.x - self.r, self.y - self.r,
                                     self.x + self.r, self.y + self.r, fill=self.color)

    def destroy_ball(self):
        canvas.delete(self.id)

    def shot_ball(self):
        canvas.move(self.id, self.dx, self.dy)
        self.x += self.dx
        self.y += self.dy
        if self.y >= BATTLEFIELD_HEIGHT - self.r - self.dy or self.y <= self.r:
            self.dy = -self.dy
        self.dy += 1
        self.hit_test()
        root.after(TIME_DELAY, self.shot_ball)

    def hit_test(self):
        if int(sqrt((target.x - self.x)**2 + (target.y - self.y)**2)) <= target.r + self.r:
            target.destroy_target()


def mouse_click(event):#TEST
    global target, canvas, ball, gun, root
    ball = Ball()
    ball.shot_ball()
    gun.gun_move()
    print('click', event)


def mouse_click2(event):#TEST
    global target, canvas, gun, ball, root
    gun.destroy_gun()
    ball.destroy_ball()
    print(gun.id, event)




if __name__ == '__main__':
    main()

