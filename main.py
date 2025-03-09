import tkinter as tk
from random import randint
from random import randrange


BATTLEFIELD_WIGTH = 800
BATTLEFIELD_HEIGHT = 600


def main() -> None:
    global canvas, target, gun, ball, root
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
    root.mainloop()
    print('Goodbye!') #Say it in shell after close window

def tick():
    target.move()
    root.after(50, tick) #miliseconds




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
        root.after(50, target.move_target)


class Gun:
    def __init__(self):
        self.x = 20
        self.y = 400
        self.id = canvas.create_line(self.x, self.y, 50, 400, width=7)#FIX use constant

    def destroy_gun(self):
        canvas.delete(self.id)


class Ball:
    def __init__(self):
        self.x = 50
        self.y = 400
        self.dx = 2
        self.dy = 0
        self.r = 10
        self.color = 'red'
        self.id = canvas.create_oval(self.x - self.r, self.y - self.r, 
                                    self.x + self.r, self.y + self.r, fill=self.color)

    def destroy_ball(self):
        canvas.delete(self.id)

    def move_ball(self):
        canvas.move(self.id, 1, 0)
        root.after(50, self.move_ball)

def mouse_click(event):#TEST
    global target, canvas, ball, gun, root
    ball.move_ball()
    print('click', event)


def mouse_click2(event):#TEST
    global target, canvas, gun, ball, root
    gun.destroy_gun()
    ball.destroy_ball()
    print(gun.id, event)




if __name__ == '__main__':
    main()

