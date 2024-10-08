from tkinter import Tk, Canvas


class window:
    def __init__(self):
        self.root = Tk()
        self.width = 1280
        self.height = 960
        self.root.resizable(True, True)
        self.canvas = Canvas(self.root, width=self.width,
                             height=self.height, bg='#F0F0F0')
        self.canvas.pack()
        self.root.after(1, self.sierpinskis_carpet, 50, 50, 5, 729)
        self.root.mainloop()

    def sierpinskis_carpet(self, x, y, n, l):
        if n == 0:
            self.canvas.create_rectangle(x, y, x+l, y+l)
            self.canvas.update()
        else:
            self.sierpinskis_carpet(x, y, n-1, l/3)
            self.sierpinskis_carpet(x+l/3, y, n-1, l/3)

            self.sierpinskis_carpet(x+2*l/3, y, n-1, l/3)
            self.sierpinskis_carpet(x+2*l/3, y+l/3, n-1, l/3)

            self.sierpinskis_carpet(x+2*l/3, y+2*l/3, n-1, l/3)
            self.sierpinskis_carpet(x+l/3, y+2*l/3, n-1, l/3)

            self.sierpinskis_carpet(x, y+2*l/3, n-1, l/3)
            self.sierpinskis_carpet(x, y+l/3, n-1, l/3)


main = window()
