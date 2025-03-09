import tkinter as tk
from random import randint
from random import randrange


BATTLEFIELD_WIGTH = 800
BATTLEFIELD_HEIGHT = 600


def main() -> None:
    global canvas, target, gun, ball
    root = tk.Tk()
    root.title('Game: Guns')
    root.geometry(f'{BATTLEFIELD_WIGTH}x{BATTLEFIELD_HEIGHT}')
    canvas = tk.Canvas(bg='white', width=BATTLEFIELD_WIGTH, height=BATTLEFIELD_HEIGHT)
    canvas.pack(anchor=tk.CENTER, expand=1)
    
    target = Target()
    gun = Gun()
    ball = Ball()

    canvas.bind('<Button-1>', mouse_click)
    canvas.bind('<Button-3>', mouse_click2)
    root.mainloop()
    print('Goodbye!') #Say it in shell after close window

def tick():
    target.move()
    root.after(50, tick) #miliseconds





class Target:
    def __init__(self):
        x = self.x = randint(100, 200)
        y = self.y = randint(100, 200)
        r = self.r = randint(5, 50)
        self.color = 'green'
        self.id = canvas.create_oval(x, y, x + 2 * r, y + 2 * r, fill=self.color)

    def destroy_target(self):
        canvas.delete(self.id) 


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

def mouse_click(event):#TEST
    global target, canvas
    target.destroy_target()
    print('click', event)


def mouse_click2(event):#TEST
    global target, canvas, gun, ball
    gun.destroy_gun()
    ball.destroy_ball()
    print(gun.id, event)




if __name__ == '__main__':
    main()

