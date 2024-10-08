from time import sleep
from tkinter import Button, Canvas, Entry, Menu, StringVar, Tk
from tkinter.messagebox import showinfo
from math import e


class node:
    def __init__(self, data, lnode: int = -1, rnode: int = -1) -> None:
        self.data = data
        self.lnode: int = lnode
        self.rnode: int = rnode


class relative_locations:
    def __init__(self, width, height):
        self.screenwidth = width
        self.screenheight = height
        self.relative_coordinates = []
        self.screen_coordinates = []
        self.screen_coordinates_store = []

    def __getitem__(self, i):
        return self.screen_coordinates[i]

    def append(self, coordinate):
        self.relative_coordinates.append(coordinate)

    def update(self):
        [self.screen_coordinates.append(i)
         for i in self.screen_coordinates_store]
        self.screen_coordinates_store = []

    def predict(self, pos):
        future_relative_coordinates = self.relative_coordinates.copy()
        future_relative_coordinates.append(pos)
        minx = min([i[0] for i in future_relative_coordinates])
        miny = min([i[1] for i in future_relative_coordinates])
        width_difference = max([i[0] for i in future_relative_coordinates]) - \
            min([i[0] for i in future_relative_coordinates])
        height_difference = max([i[1] for i in future_relative_coordinates]) - \
            min([i[1] for i in future_relative_coordinates])
        usablewidth = self.screenwidth - \
            (e ** (-0.1 *
             (len(set([i[0] for i in future_relative_coordinates]))-1))) * self.screenwidth
        usableheight = self.screenheight - \
            (e ** (-0.2 *
             (len(set([i[1] for i in future_relative_coordinates]))-1))) * self.screenheight
        if width_difference == 0:
            ratiox = 0
        else:
            ratiox = usablewidth / width_difference
        if height_difference == 0:
            ratioy = 0
        else:
            ratioy = usableheight / height_difference
        originx = (self.screenwidth - usablewidth) / 2
        originy = (self.screenheight - usableheight) / 2
        self.new_coordinates = [
            [(i[0]-minx)*ratiox+originx, (i[1]-miny)*ratioy+originy] for i in future_relative_coordinates]
        self.screen_coordinates_store.append(self.new_coordinates[-1])
        return self.new_coordinates[:-1]


class window:
    def __init__(self):
        self.title = "Binary Search Tree visualizer"
        self.ver = '1.0'
        self.licenceStr = \
            "GNU General Public License\n\n" \
            + "This program is free software; you can redistribute it and/or modify it under the terms of the " \
            + "GNU General Public License as published by the Free Software Foundation; " \
            + "either version 2 of the License, or (at your option) any later version.\n\n" \
            + "This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; " \
            + "without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  " \
            + "See the GNU General Public License for more details.\n\n" \
            + "You should have received a copy of the GNU General Public License along with this program; if not, " \
            + "write to the Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA."
        self.root = Tk()
        self.root.title(self.title)

        self.width = 1280
        self.height = 960
        self.root.resizable(True, True)
        self.canvas = Canvas(self.root, width=self.width,
                             height=self.height, bg='#F0F0F0')
        self.canvas.pack()

        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        self.operations = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.root.destroy)
        self.operations.add_command(label="Start demo", command=self.demo)
        self.operations.add_command(
            label="In order", command=self.inorder, state="disabled")
        self.operations.add_command(
            label="Pre order", command=self.preorder, state="disabled")
        self.operations.add_command(
            label="Post order", command=self.postorder, state="disabled")
        self.operations.add_command(label="Reset", command=self.reset)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Operations", menu=self.operations)
        menubar.add_command(label="About", command=self.popupShowinfo)
        self.root.config(menu=menubar)

        s_insert = StringVar()
        insertentry = Entry(self.root, textvariable=s_insert,
                            width=30, font=('Arial', 10, 'normal'))
        insertentry.bind(
            "<Return>", lambda event: self.insertitem(s_insert.get()))
        insertentry.place(x=10, y=10)
        insert_btn = Button(self.root, text="Insert", width=6,
                            height=1, command=lambda: self.insertitem(s_insert.get()))
        insert_btn.place(x=250, y=10)

        self.returntext: str = ""
        self.returntext_control = self.canvas.create_text(
            (810, 640), text='', font=('Arial', 10, 'normal'))

        self.store: list[node] = []
        self.store.append(node(None))
        self.freestore = 0

        self.nodes = []
        self.node_data = []

        self.pos = relative_locations(self.width, self.height)
        self.lines = []
        self.links = []
        self.redraw()
        self.root.mainloop()

    def demo(self):
        [self.insertitem(i)
         for i in ['F', 'B', 'G', 'I', 'A', 'D', 'H', 'C', 'E']]
        self.operations.entryconfig("In order", state="normal")
        self.operations.entryconfig("Pre order", state="normal")
        self.operations.entryconfig("Post order", state="normal")

    def popupShowinfo(self):
        showinfo("About " + self.title, "Version: " + self.ver
                 + " September 2022\n\nAuthor: Jeffrey Cheung\n\n"
                 + self.licenceStr)

    def insertitem(self, item, ptr: int = 0, path=None, dir=None):
        if path is None:
            path = []
        if dir is None:
            dir = []
        self.delay()
        if self.store[ptr].data is None:
            self.calculate_layout(path, dir)
            self.store[ptr].data = item
            self.create_node()
            self.canvas.itemconfig(self.node_data[ptr], text=item)
            self.fillnode(ptr)
            self.delay()
            self.reset_nodes()
            self.freestore += 1
            self.store.append(node(None))
        else:
            self.fillnode(ptr)
        if item < self.store[ptr].data:
            path.append(ptr)
            dir.append(-1)
            if self.store[ptr].lnode == -1:
                self.store[ptr].lnode = self.freestore
            self.insertitem(item, self.store[ptr].lnode, path, dir)
        elif item > self.store[ptr].data:
            path.append(ptr)
            dir.append(1)
            if self.store[ptr].rnode == -1:
                self.store[ptr].rnode = self.freestore
            self.insertitem(item, self.store[ptr].rnode, path, dir)
        self.redraw()

    def finditem(self, item) -> int:
        itempointer = -1
        while self.store[itempointer].data != item and itempointer != -1:
            if self.store[itempointer].data > item:
                itempointer = self.store[itempointer].lnode
            else:
                itempointer = self.store[itempointer].rnode
        return itempointer

    def inorder(self, ptr: int = 0):
        if len(self.store) == 0:
            return
        if not ptr:
            self.reset_returntext()
        self.delay()
        self.fillnode(ptr)
        if self.store[ptr].lnode != -1:
            self.inorder(self.store[ptr].lnode)
        self.delay()
        self.fillnode(ptr)
        self.add_returntext(self.store[ptr].data)
        if self.store[ptr].rnode != -1:
            self.inorder(self.store[ptr].rnode)
        self.delay()
        self.fillnode(ptr)
        if not ptr:
            self.delay()
            self.reset_nodes()

    def preorder(self, ptr: int = 0):
        if len(self.store) == 0:
            return
        if not ptr:
            self.reset_returntext()
        self.delay()
        self.fillnode(ptr)
        self.add_returntext(self.store[ptr].data)
        if self.store[ptr].lnode != -1:
            self.preorder(self.store[ptr].lnode)
        self.delay()
        self.fillnode(ptr)
        if self.store[ptr].rnode != -1:
            self.preorder(self.store[ptr].rnode)
        self.delay()
        self.fillnode(ptr)
        if not ptr:
            self.delay()
            self.reset_nodes()

    def postorder(self, ptr: int = 0):
        if len(self.store) == 0:
            return
        if not ptr:
            self.reset_returntext()
        self.delay()
        self.fillnode(ptr)
        if self.store[ptr].lnode != -1:
            self.postorder(self.store[ptr].lnode)
        self.delay()
        self.fillnode(ptr)
        if self.store[ptr].rnode != -1:
            self.postorder(self.store[ptr].rnode)
        self.delay()
        self.fillnode(ptr)
        self.add_returntext(self.store[ptr].data)
        if not ptr:
            self.delay()
            self.reset_nodes()

    def get_links(self, ptr: int = 0):
        links = []
        if self.store[ptr].lnode != -1:
            links.append([ptr, self.store[ptr].lnode])
            links += self.get_links(self.store[ptr].lnode)
        if self.store[ptr].rnode != -1:
            links.append([ptr, self.store[ptr].rnode])
            links += self.get_links(self.store[ptr].rnode)
        return links

    def calculate_layout(self, path, dir):
        if len(dir) == 0:
            x = 0
        else:
            x = sum([dir[i]*600/2**i for i in range(len(dir))])
        y = len(path) * 100
        new_coordinates = self.pos.predict([x, y])
        args = []
        for i in range(len(new_coordinates)):
            args += [i, new_coordinates[i][0]-self.pos[i]
                     [0], new_coordinates[i][1]-self.pos[i][1]]
        self.move_object(args)
        self.pos.append([x, y])
        self.links = self.get_links()
        self.pos.update()

    def create_node(self):
        self.nodes.append(self.canvas.create_oval(
            self.pos[len(self.store)-1][0] -
            30, self.pos[len(self.store)-1][1]-30,
            self.pos[len(self.store)-1][0]+30, self.pos[len(self.store)-1][1]+30, width=1, fill='cadetblue2'))
        self.node_data.append(self.canvas.create_text(
            self.pos[len(self.store)-1], fill='black', font=('Arial', 10), text=self.store[-1].data))

    def reset_nodes(self):
        for i in self.nodes:
            self.canvas.itemconfig(i, fill='cadetblue2')
        self.root.update()

    def fillnode(self, ptr):
        for i in self.nodes:
            self.canvas.itemconfig(i, fill='cadetblue2')
        self.canvas.itemconfig(self.nodes[ptr], fill="green")
        self.root.update()

    def redraw(self):
        self.canvas.delete("all")
        self.lines = []
        self.nodes = []
        self.node_data = []
        for i in self.links:
            self.canvas.create_line(self.pos[i[0]], self.pos[i[1]])
        for i in range(len(self.store)-1):
            self.nodes.append(self.canvas.create_oval(
                self.pos[i][0]-30, self.pos[i][1]-30, self.pos[i][0]+30, self.pos[i][1]+30, width=1, fill='cadetblue2'))
            self.node_data.append(self.canvas.create_text(
                self.pos[i], fill='black', font=('Arial', 10), text=self.store[i].data))
        self.returntext_control = self.canvas.create_text(
            (810, 640), text='', font=('Arial', 10, 'normal'))
        self.root.update()

    def move_object(self, args):
        if len(args) % 3 != 0:
            raise IndexError
        objects, dx, dy = [], [], []
        for i in range(len(args)//3):
            objects.append(args[i * 3])
            dx.append(args[i*3 + 1]/30)
            dy.append(args[i*3 + 2]/30)
        for i in range(30):
            for o in range(len(objects)):
                self.pos[objects[o]][0] += dx[o]
                self.pos[objects[o]][1] += dy[o]
            self.redraw()
            sleep(1/30)

    def add_returntext(self, add):
        self.returntext += add
        self.canvas.itemconfig(self.returntext_control, text=self.returntext)

    def reset_returntext(self):
        self.returntext = ""
        self.canvas.itemconfig(self.returntext_control, text=self.returntext)

    def reset(self):
        self.store: list[node] = []
        self.store.append(node(None))
        self.freestore = 0

        self.nodes = []
        self.node_data = []

        self.pos = relative_locations(self.width, self.height)
        self.links = []
        self.redraw()

    @staticmethod
    def delay():
        sleep(2/15)


main = window() 