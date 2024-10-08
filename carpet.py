from tkinter import Tk, Canvas


X = [1, 0, -1, 0]
Y = [0, 1, 0, -1]


class window:
    def __init__(self):
        self.root = Tk()
        self.width = 960
        self.height = 960
        self.root.resizable(True, True)
        self.canvas = Canvas(self.root, width=self.width,
                             height=self.height, bg='#F0F0F0')
        self.canvas.pack()

        self.dir = dir()

        self.root.after(50, self.sierpinskis_carpet, 4, 891, [50, 50])
        self.root.mainloop()

    def sierpinskis_carpet(self, n, l, o):
        if n == 0:
            self.canvas.create_rectangle(
                o[0], o[1], o[0]+l/3, o[1]+l/3)
            self.root.update()
        else:
            self.canvas.create_rectangle(
                o[0], o[1], o[0]+l, o[1]+l)
            self.root.update()
            for d in range(4):
                for _ in range(2):
                    self.sierpinskis_carpet(n-1, l/3, o)
                    o[0] += l/3*X[d]
                    o[1] += l/3*Y[d]


main = window()
