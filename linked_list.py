from tkinter import Button, Canvas, Entry, Menu, StringVar, Tk
from tkinter.messagebox import showinfo


class node():
    def __init__(self, data: str, ptr: int) -> None:
        self.data = data
        self.ptr = ptr
        return


NULLPOINTER = -1


class linked_list():
    def __init__(self, size):
        self.startptr: int = NULLPOINTER
        self.freelistptr: int = 0
        self.list: list[node] = []
        for i in range(size-1):
            self.list.append(node("", i+1))
        self.list.append(node("", NULLPOINTER))

    def insert_node(self, new_item) -> str:
        if self.freelistptr != NULLPOINTER:
            newnodeptr = self.freelistptr
            self.list[newnodeptr].data = new_item
            self.freelistptr = self.list[self.freelistptr].ptr
            previousnodeptr = NULLPOINTER
            thisnodeptr = self.startptr
            while thisnodeptr != NULLPOINTER and self.list[thisnodeptr].data < new_item:
                previousnodeptr = thisnodeptr
                thisnodeptr = self.list[thisnodeptr].ptr
            if self.startptr == NULLPOINTER or previousnodeptr == NULLPOINTER:
                self.list[newnodeptr].ptr = self.startptr
                self.startptr = newnodeptr
            else:
                self.list[newnodeptr].ptr = self.list[previousnodeptr].ptr
                self.list[previousnodeptr].ptr = newnodeptr
            return "Successfully added " + new_item + " at index " + str(newnodeptr)
        else:
            return "Failed to add. List is full"

    def find_node(self, dataitem) -> int:
        currentnodeptr = self.startptr
        while currentnodeptr != NULLPOINTER and self.list[currentnodeptr].data != dataitem:
            currentnodeptr = self.list[currentnodeptr].ptr
        return currentnodeptr

    def delete_node(self, dataitem) -> str:
        thisnodeptr = self.startptr
        previousnodeptr = NULLPOINTER
        while thisnodeptr != NULLPOINTER and self.list[thisnodeptr].data != dataitem:
            previousnodeptr = thisnodeptr
            thisnodeptr = self.list[thisnodeptr].ptr
        if thisnodeptr != NULLPOINTER:
            if thisnodeptr == self.startptr:
                self.startptr = self.list[self.startptr].ptr
            else:
                self.list[previousnodeptr].ptr = self.list[thisnodeptr].ptr
            self.list[thisnodeptr].ptr = self.freelistptr
            self.freelistptr = thisnodeptr
            return "Successfully removed " + dataitem + " from index " + str(thisnodeptr)
        else:
            return "Item '" + dataitem + "' not found"

    def output_all_nodes(self) -> str:
        currentnodeptr = self.startptr
        text = ''
        while currentnodeptr != NULLPOINTER:
            text += self.list[currentnodeptr].data + '\n'
            currentnodeptr = self.list[currentnodeptr].ptr
        return text


def test_linked_list():
    a = linked_list(8)
    a.insert_node('b')
    a.insert_node('i')
    a.insert_node('l')
    a.insert_node('i')
    a.insert_node('b')
    a.insert_node('a')
    a.insert_node('l')
    a.insert_node('a')
    a.insert_node('c')
    print(a.output_all_nodes())
    print('bu')
    for i in a.list:
        print(i.data)


class window:
    def __init__(self):
        self.title = "Linked list visualiser"
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
        self.ver = "1.0"

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

        self.linked_list = linked_list(10)
        self.store = []
        self.store2 = []
        self.control = []
        self.control2 = []
        for i in range(10):  # support up to only list size 10
            self.store.append(self.canvas.create_rectangle(
                (200, 180+i*40, 400, 220+i*40), width=1, fill="cadetblue2"))
            self.store2.append(self.canvas.create_rectangle(
                (400, 180+i*40, 500, 220+i*40), width=1, fill="cadetblue2"))
            self.canvas.create_text(
                (180, 200+i*40), fill='black', font=('Arial', 10), text=str(i))
            self.control.append(self.canvas.create_text(
                (300, 200+i*40), fill='black', font=('Arial', 10), text=""))
            self.control2.append(self.canvas.create_text(
                (450, 200+i*40), fill='black', font=('Arial', 10), text=""))

        self.startptr_label = self.canvas.create_text(
            (220, 40), text='Start-Ptr: {}'.format(self.linked_list.startptr), font=('Arial', 10, 'normal'))
        self.freelistptr_label = self.canvas.create_text(
            (620, 40), text='Free-Ptr: {}'.format(self.linked_list.freelistptr), font=('Arial', 10, 'normal'))
        self.large_word = self.canvas.create_text(
            (660, 540), fill='black', font=('Courier', 12), text='', anchor='nw')

        s_newItem = StringVar()
        newItem_entry = Entry(self.root, textvariable=s_newItem,
                              width=30, font=('Arial', 10, 'normal'))
        newItem_entry.place(x=660, y=180)
        s_removeItem = StringVar()
        removeItem_entry = Entry(
            self.root, textvariable=s_removeItem, width=30, font=('Arial', 10, 'normal'))
        removeItem_entry.place(x=660, y=260)

        addItem_btn = Button(self.root, text="Add", width=6,
                             height=1, command=lambda: self.addItem(s_newItem.get()))
        addItem_btn.place(x=960, y=180)
        removeItem_btn = Button(
            self.root, text="Remove", width=6, height=1, command=lambda: self.removeItem(s_removeItem.get()))
        removeItem_btn.place(x=960, y=260)
        resetItem_btn = Button(
            self.root, text="Reset", width=6, height=1, command=lambda: self.resetItem())
        resetItem_btn.place(x=960, y=340)

        self.root.mainloop()

    def popupShowinfo(self):
        showinfo("About " + self.title, "Version: " + self.ver
                 + " September 2022\n\nAuthor: Jeffrey Cheung\n\n" + self.licenceStr)

    def addItem(self, newItem):
        result = self.linked_list.insert_node(newItem)
        self.canvas.itemconfig(self.store[int(result[-1])], fill="green")
        self.canvas.itemconfig(self.store2[int(result[-1])], fill="green")
        self.update_items(displaytext=result)

    def removeItem(self, dataitem):
        result = self.linked_list.delete_node(dataitem)
        self.canvas.itemconfig(self.store[int(result[-1])], fill="cadetblue2")
        self.canvas.itemconfig(self.store2[int(result[-1])], fill="cadetblue2")
        returntext = result
        self.update_items(displaytext=str(returntext))

    def resetItem(self):
        self.linked_list = linked_list(10)
        for i in range(10):
            self.canvas.itemconfig(self.store[i], fill="cadetblue2")
            self.canvas.itemconfig(self.store2[i], fill="cadetblue2")
        self.update_items(displaytext="Successful")

    def update_items(self, displaytext=''):
        for i in range(10):
            self.canvas.itemconfig(
                self.control[i], text=self.linked_list.list[i].data)
            self.canvas.itemconfig(self.control2[i], text=str(
                self.linked_list.list[i].ptr))
        self.canvas.itemconfig(
            self.startptr_label, text='Start-Ptr: {}'.format(self.linked_list.startptr))
        self.canvas.itemconfig(
            self.freelistptr_label, text='Free-Ptr: {}'.format(self.linked_list.freelistptr))
        self.canvas.itemconfig(self.large_word, text=displaytext)


def main():
    root = window()


if __name__ == "__main__":
    main()
