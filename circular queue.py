from math import cos, pi, sin
from tkinter import Button, Canvas, Entry, Menu, StringVar, Tk
from tkinter.messagebox import showinfo


class circular_queue:
    def __init__(self, size):
        self.head = 0
        self.tail = -1
        self.numElements = 0
        self.size = size
        self.store = [0] * self.size

    def resetStore(self):
        self.__init__(self.size)
        return True

    def addItem(self, newItem):
        successs = False
        if self.numElements < self.size:
            self.tail = (self.tail + 1) % self.size
            self.store[self.tail] = newItem
            self.numElements += 1
            successs = True
        else:
            return "Add failed: queue is full"
        return successs

    def removeItem(self):
        value = None
        success = False
        if self.numElements != 0:
            value = self.store[self.head]
            self.head = (self.head + 1) % self.size
            self.numElements -= 1
            success = True
        else:
            return "Remove failed: queue is empty"
        return success, value

    def getStore(self):
        return self.store

    def getPointers(self):
        return {"Head-ptr": self.head, "Tail-ptr": self.tail}

    def getQueueIndexes(self):
        if self.numElements != 0:
            if self.head > self.tail:
                return list(range(self.head, self.size)) + list(range(0, self.tail+1))
            else:
                return list(range(self.head, self.tail+1))
        else:
            return []

    def getQueueData(self):
        return [self.store[i] for i in self.getQueueIndexes()]


def part_of_part_of_circle(centrex, centrey, radiusa, radiusb, start, extent):
    list = []
    for i in range(start, extent+1):
        list.append([centrex+radiusa*cos(i/180*pi),
                    centrey+radiusa*sin(i/180*pi)])
    for i in range(extent, start-1, -1):
        list.append([centrex+radiusb*cos(i/180*pi),
                    centrey+radiusb*sin(i/180*pi)])
    return list


class window:
    def __init__(self):
        self.title = "Circular queue visualizer"
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

        width = 1280
        height = 840
        self.root.resizable(True, True)
        self.canvas = Canvas(self.root, width=width,
                             height=height, bg='#F0F0F0')
        self.canvas.pack()

        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_command(label="About", command=self.popupShowinfo)
        self.root.config(menu=menubar)

        self.controls = []
        self.storages = []

        # method 1
        # self.queue = circular_queue(28)
        # self.storages.append(self.canvas.create_arc((60, 140, 220, 240), width = 1, fill = 'cadetblue2', style=CHORD, start=90, extent=180))
        # self.canvas.create_text((100, 120), fill='black', font=('Arial', 10), text=str(0))
        # self.controls.append(self.canvas.create_text((100, 190), fill='black', font=('Arial, 10'), text=''))
        # for i in range(1,14):
        #     self.storages.append(self.canvas.create_rectangle((60+i*80, 140, 140+i*80, 180), width = 1, fill = 'cadetblue2'))
        #     self.canvas.create_text((100+i*80, 120), fill='black', font=('Arial', 10), text=str(i))
        #     self.controls.append(self.canvas.create_text((100+i*80, 160), fill='black', font=('Arial, 10'), text=''))
        # self.storages.append(self.canvas.create_arc((1100, 140, 1260, 240), width = 1, fill = 'cadetblue2', style=CHORD, start=90, extent=-180))
        # self.canvas.create_text((1220, 120), fill='black', font=('Arial', 10), text=str(14))
        # self.controls.append(self.canvas.create_text((1220, 190), fill='black', font=('Arial, 10'), text=''))
        # for i in range(13):
        #     self.storages.append(self.canvas.create_rectangle((1180-i*80, 200, 1100-i*80, 240), width = 1, fill = 'cadetblue2'))
        #     self.canvas.create_text((1140-i*80, 260), fill='black', font=('Arial', 10), text=str(15+i))
        #     self.controls.append(self.canvas.create_text((1140-i*80, 220), fill='black', font=('Arial, 10'), text=''))

        # method 2
        self.queue = circular_queue(60)
        for i in range(60):
            self.storages.append(self.canvas.create_polygon(part_of_part_of_circle(
                810, 440, 350, 300, i*6, 6+i*6), width=1, outline='black', fill="cadetblue2"))
            self.canvas.create_text((810+370*cos((3+i*6)/180*pi), 440+370*sin(
                (3+i*6)/180*pi)), fill='black', font=('Arial', 10), text=str(i))
            self.controls.append(self.canvas.create_text(
                (810+325*cos((3+i*6)/180*pi), 440+325*sin((3+i*6)/180*pi)), fill='black', font=('Arial, 10'), text=''))

        self.headptr_label = self.canvas.create_text((220, 40), text='Head-Ptr: {}'.format(
            self.queue.getPointers()["Head-ptr"]), font=('Arial', 10, 'normal'))
        self.tailptr_label = self.canvas.create_text((620, 40), text='Tail-Ptr: {}'.format(
            self.queue.getPointers()["Tail-ptr"]), font=('Arial', 10, 'normal'))
        self.returntext = self.canvas.create_text(
            (810, 440), text='', font=('Arial', 10, 'normal'))

        s_newItem = StringVar()
        newItem_entry = Entry(self.root, textvariable=s_newItem,
                              width=30, font=('Arial', 10, 'normal'))
        newItem_entry.place(x=60, y=280)

        addItem_btn = Button(self.root, text="Add", width=6,
                             height=1, command=lambda: self.addItem(s_newItem.get()))
        addItem_btn.place(x=60, y=320)
        removeItem_btn = Button(
            self.root, text="Remove", width=6, height=1, command=lambda: self.removeItem())
        removeItem_btn.place(x=60, y=360)
        resetItem_btn = Button(
            self.root, text="Reset", width=6, height=1, command=lambda: self.resetItem())
        resetItem_btn.place(x=60, y=400)

        self.update_item()
        self.root.mainloop()

    def popupShowinfo(self):
        showinfo("About " + self.title, "Version: " + self.ver
                 + " September 2022\n\nAuthor: Jeffrey Cheung\n\n"
                 + self.licenceStr)

    def update_item(self, returntext=''):
        for i in range(len(self.queue.getStore())):
            self.canvas.itemconfig(
                self.controls[i], text=str(self.queue.getStore()[i]))
            if i in self.queue.getQueueIndexes():
                self.canvas.itemconfig(self.storages[i], fill='green')
            else:
                self.canvas.itemconfig(self.storages[i], fill='cadetblue2')
        self.canvas.itemconfig(
            self.headptr_label, text='Head-Ptr: {}'.format(self.queue.getPointers()["Head-ptr"]))
        self.canvas.itemconfig(
            self.tailptr_label, text='Tail-Ptr: {}'.format(self.queue.getPointers()["Tail-ptr"]))
        self.canvas.itemconfig(self.returntext, text=returntext)

    def addItem(self, newItem):
        result = self.queue.addItem(newItem)
        if result is True:
            returntext = "Successful!"
        else:
            returntext = result
        self.update_item(returntext=returntext)

    def removeItem(self):
        result = self.queue.removeItem()
        if type(result) == str:
            returntext = result
        else:
            returntext = "Successful! The value removed is {}".format(
                result[1])
        self.update_item(returntext=str(returntext))

    def resetItem(self):
        result = self.queue.resetStore()
        if result is True:
            returntext = "Successful!"
        else:
            returntext = result
        self.update_item(returntext=returntext)


def main():
    root = window()


main()
