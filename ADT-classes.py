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
        self.queue = circular_queue(15)
        for i in range(15):
            self.storages.append(self.canvas.create_rectangle(
                (60+i*80, 140, 140+i*80, 180), width=1, fill='cadetblue2'))
            self.canvas.create_text(
                (100+i*80, 120), fill='black', font=('Arial', 10), text=str(i))
            self.controls.append(self.canvas.create_text(
                (100+i*80, 160), fill='black', font=('Arial, 10'), text=''))

        self.headptr_label = self.canvas.create_text((220, 40), text='Head-Ptr: {}'.format(
            self.queue.getPointers()["Head-ptr"]), font=('Arial', 10, 'normal'))
        self.tailptr_label = self.canvas.create_text((620, 40), text='Tail-Ptr: {}'.format(
            self.queue.getPointers()["Tail-ptr"]), font=('Arial', 10, 'normal'))
        self.returntext = self.canvas.create_text(
            (620, 280), text='', font=('Arial', 10, 'normal'))

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
