#Spaghetti Code Warning
from tkinter import *
from tkinter.messagebox import showinfo

class stack:
    def __init__(self, size):
        self.store = [''] * size
        self.size = size
        self.pointer = 0

    def push(self, value):
        if self.pointer == self.size - 1:
            print("Stack Overflow")
        self.store[self.pointer] = value
        self.pointer += 1
        return value

    def pop(self):
        if self.pointer == 0:
            print("Stack Underflow")
        self.pointer -= 1
        value = self.store[self.pointer]
        self.store[self.pointer] = ''
        return value


def evaluator():
    print("Input RPN expression.")
    expression = input().split(' ')
    operands = stack(len(expression))
    for i in expression:
        try:
            operands.push(int(i))
            continue
        except ValueError:
            pass
        if i in ['+', '-', '*', '/']:
            operand1 = operands.pop()
            operand2 = operands.pop()
            match i:
                case '+':
                    result = operand2 + operand1
                    operands.push(result)
                case '-':
                    result = operand2 - operand1
                    operands.push(result)
                case '*':
                    result = operand2 * operand1
                    operands.push(result)
                case '/':
                    result = operand2 / operand1
                    operands.push(result)
        else:
            print('Error')
    print(operands.pop())


def shunting_yard(expression=None):
    if expression is None:
        print("Input infix expression.")
        expression = input()
    tokens = expression.split(' ')
    operators = stack(len(expression))
    output = ""
    for i in tokens:
        try:
            output += str(int(i)) + ' '
            continue
        except ValueError:
            pass
        if i in ['+', '-', '*', '/']:
            if operators.pointer > 0:
                top = operators.push(operators.pop())
                if ((i in ['+', '-']) and top in ['+', '-', '*', '/']) or (top in ['*', '/']):
                    output += operators.pop() + ' '
            operators.push(i)
        elif i == '(':
            operators.push(i)
        elif i == ')':
            top = operators.pop()
            while top != '(':
                output += top + ' '
                top = operators.pop()
    while operators.pointer > 0:
        output += operators.pop() + ' '
    output = output.rstrip(' ')
    if expression is None:
        print(output)
    return output


class window:
    def __init__(self):
        self.title = "RPN Expression evaluator"
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
        self.canvas = Canvas(self.root, width = width, height = height, bg = '#F0F0F0')
        self.canvas.pack()

        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_command(label="About", command=self.popupShowinfo)
        self.root.config(menu=menubar)

        self.store=[]
        for i in range(15): #support up to only stack size 15
            self.canvas.create_rectangle((200, 180+i*40,400, 220+i*40), width = 1, fill = "cadetblue2")
            self.canvas.create_text((180,200+i*40), fill='black', font=('Arial', 10), text=str(14-i))
            self.store.append(self.canvas.create_text((300,200+i*40), fill='black', font=('Arial', 10), text=""))

        self.large_word = self.canvas.create_text((450, 180), fill='black', font=('Courier',24), text='', anchor='nw')
        self.dot_indicator = self.canvas.create_oval(460, 240, 464, 244, width=2, fill='grey')

        btnstep = Button(self.root, text="Step", width=15, height=5, bd=2, command=self.step_evaluator, font=('Arial', 10))
        btnstep.place(x=980, y=640)

        Infix_expression_value = StringVar()
        Infix_expression_label = Label(self.root, text='Infix expression', font=('Arial', 10, 'normal'))
        Infix_expression_label.place (x=220, y=40)
        Infix_expression_entry = Entry(self.root, textvariable=Infix_expression_value, width=30, font=('Arial', 10, 'normal'))
        Infix_expression_entry.place (x=220, y=80)
        Infix_btnsubmit = Button(self.root, text="Submit", width=6, height=1, command=lambda:self.translate_expression(Infix_expression_value.get()), font=('Arial', 10))
        Infix_btnsubmit.place(x=460,y=80)

        RPN_expression_value = StringVar()
        RPN_expression_label = Label(self.root, text='RPN expression', font=('Arial', 10, 'normal'))
        RPN_expression_label.place (x=760, y=40)
        RPN_expression_entry = Entry(self.root, textvariable=RPN_expression_value, width=30, font=('Arial', 10, 'normal'))
        RPN_expression_entry.place (x=760, y=80)
        RPN_btnsubmit = Button(self.root, text="Submit", width=6, height=1, command=lambda:self.get_expression(RPN_expression_value.get()), font=('Arial', 10))
        RPN_btnsubmit.place(x=1000,y=80)

        self.root.mainloop()


    def popupShowinfo(self):
        showinfo("About " + self.title, "Version: " + self.ver
                + " September 2022\n\nAuthor: Jeffrey Cheung\n\n"
                + self.licenceStr)


    def step_evaluator(self):
        if self.step >= len(self.expression): return
        i = self.expression[self.step]
        try:
            self.operands.push(int(i))
            self.step += 1
            self.update_items()
            return
        except ValueError:
            pass
        if i in ['+', '-', '*', '/']:
            operand1 = self.operands.pop()
            operand2 = self.operands.pop()
            match i:
                case '+':
                    result = operand2 + operand1
                    self.operands.push(result)
                case '-':
                    result = operand2 - operand1
                    self.operands.push(result)
                case '*':
                    result = operand2 * operand1
                    self.operands.push(result)
                case '/':
                    result = operand2 / operand1
                    self.operands.push(result)
        else:
            print('Error')
        self.step += 1
        self.update_items()


    def translate_expression(self,value):
        output = shunting_yard(value)
        self.get_expression(output)

    
    def get_expression(self,value):
        self.raw = value#.replace(' ','')
        self.expression = value.split(' ')
        self.operands = stack(15)
        self.step = 0
        self.update_items()


    def update_items(self):
        for i in range(len(self.operands.store)):
            self.canvas.itemconfig(self.store[i],text=str(self.operands.store[14-i]))
        self.canvas.itemconfig(self.large_word,text=self.raw)
        current = "".join(self.expression[:self.step-1]) + ' '*(self.step-1)
        self.canvas.move(self.dot_indicator,460+len(current)*19-self.canvas.bbox(self.dot_indicator)[0],0)


def main():
    root = window()


if __name__ == "__main__":
    main()