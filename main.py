from tkinter import *

def main() -> None:
    root = Tk()
    root.title('Game')
    root.geometry('800x600')
    label = Label(text='Guns')
    label.pack()
    root.mainloop()
    print('Goodbye!') #Say it in shell after close window

if __name__ == '__main__':
    main()

