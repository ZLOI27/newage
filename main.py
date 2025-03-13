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
    ball = Ball()
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
        x = self.x = randint(650, 750)
        y = self.y = randint(50, 550)
        r = self.r = randint(5, 50)
        self.dx = 0
        self.dy = 5
        self.color = 'green'
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, fill=self.color)

    def destroy_target(self):
        canvas.delete(self.id) 

    def move_target(self):
        canvas.move(self.id, self.dx, self.dy)
        self.x += self.dx
        self.y += self.dy
        if self.y >= BATTLEFIELD_HEIGHT - self.r or self.y <= self.r:
            self.dy = -self.dy
        root.after(TIME_DELAY, target.move_target)


class Gun:
    FIRST_POINT_X = 20
    FIRST_POINT_Y = 400
    SECOND_POINT_X = 50
    SECOND_POINT_Y = 400
    WIDTH = 7
    #x = self.x = event.x
    #y = self.y = event.y

    def __init__(self):
        self.id = canvas.create_line(self.FIRST_POINT_X, self.FIRST_POINT_Y, 
                                     self.SECOND_POINT_X, self.SECOND_POINT_Y, 
                                     width=self.WIDTH)

    def destroy_gun(self):
        canvas.delete(self.id)

    def gun_move(self):
        canvas.coords(gun.id, self.FIRST_POINT_X, self.FIRST_POINT_Y, 
                      canvas.winfo_pointerx() - canvas.winfo_rootx(), 
                      canvas.winfo_pointery() - canvas.winfo_rooty())
        root.after(TIME_DELAY, gun.gun_move)


class Ball:
    def __init__(self):
        x = self.x = 50
        y = self.y = 400
        dx = self.dx = 4
        dy = self.dy = 0
        r = self.r = 10
        self.color = 'red'
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, fill=self.color)

    def destroy_ball(self):
        canvas.delete(self.id)

    def move_ball(self):
        canvas.move(self.id, self.dx, self.dy)
        self.x += self.dx
        self.y += self.dy
        if self.y >= BATTLEFIELD_HEIGHT - self.r - self.dy or self.y <= self.r:
            self.dy = -self.dy
        self.dy += 1
        self.hit_test()
        root.after(TIME_DELAY, self.move_ball)

    def hit_test(self):
        if int(sqrt((target.x - ball.x) ** 2 + (target.y - ball.y) ** 2)) <= target.r + ball.r:
            target.destroy_target()


def mouse_click(event):#TEST
    global target, canvas, ball, gun, root
    ball.move_ball()
    gun.gun_move()
    print('click', event)


def mouse_click2(event):#TEST
    global target, canvas, gun, ball, root
    gun.destroy_gun()
    ball.destroy_ball()
    print(gun.id, event)




if __name__ == '__main__':
    main()

