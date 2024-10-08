from math import cos, pi, sin
from tkinter import Canvas, Menu, Tk

from clock import Clock as Clock
# from clock import Fake_Clock as Clock
from about import About


class window(About):
    """Window class for ClockDisplay"""

    def __init__(self, configs) -> None:
        # Create "about" message box
        super().__init__()

        self.root = Tk()
        self.root.title(self.title)

        self.no_clocks = len(configs)
        self.width = 300 * self.no_clocks
        self.height = 360
        self.root.resizable(True, True)
        self.canvas = Canvas(self.root, width=self.width,
                             height=self.height, bg='#F0F0F0')
        self.canvas.pack()

        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        self.operations = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_command(label="About", command=self.popupShowinfo)
        self.root.config(menu=menubar)

        self.hour_hands:    list[int] = []
        self.minute_hands:  list[int] = []
        self.second_hands:  list[int] = []

        self.configs = configs
        self.clocks: list[Clock] = []
        self.digital_clocks = []
        for i in range(self.no_clocks):
            config = self.configs[i]
            self.clocks.append(
                Clock(config['region'], config['utc_offset'], i*300+150, 150))
            self.draw_clock(i*300+150, 150)
            self.digital_clocks.append(self.canvas.create_text(
                i*300+150, 320, font=('Arial', 10, 'normal')))
            self.canvas.create_text(
                i*300+150, 340, text=config['region'], font=('Arial', 10, 'normal'))

        self.root.after(1,self.update_clocks)

    def draw_clock(self, centrex, centrey) -> None:
        """Method to create the outline of each clock object"""
        self.canvas.create_oval(centrex-150, centrey -
                                150, centrex+150, centrey+150, outline='grey')
        self.canvas.create_oval(centrex-3, centrey-3,
                                centrex+3, centrey+3, fill='black')

        for i in [i*pi/6 for i in range(12)]:  # thicker minute marks
            self.canvas.create_line(centrex-135*cos(i), centrey-135 *
                                    sin(i), centrex-150*cos(i), centrey-150*sin(i), width=5)
        for i in range(4, 16):  # number mark
            self.canvas.create_text(
                centrex-125*cos(i*pi/6), centrey-125*sin(i*pi/6), text=str((i-3)))
        for i in [i*pi/30 for i in range(60)]:  # thin minute marks
            self.canvas.create_line(
                135*cos(i)+centrex, 135*sin(i)+centrey, 150*cos(i)+centrex, 150*sin(i)+centrey)

        # Hands
        self.hour_hands.append(self.canvas.create_line(
            centrex, centrey, centrex-50, centrey-50, width=7))
        self.minute_hands.append(self.canvas.create_line(
            centrex, centrey, centrex-80, centrey-80, width=3))
        self.second_hands.append(self.canvas.create_line(
            centrex, centrey, centrex-120, centrey-120))

    def update_clocks(self) -> None:
        """Get the current time, and also update coordinate of all clock hands."""
        for i in range(len(self.clocks)):  # Update all clock hands
            self.clocks[i].calibrate()
            # self.clocks[i].increment_second()
            self.canvas.coords(self.hour_hands[i], i*300+150, 150, i*300+150-50*cos(
                (self.clocks[i].hour+3)/6*pi+self.clocks[i].minute/360*pi),
                150-50*sin((self.clocks[i].hour+3)/6*pi+self.clocks[i].minute/360*pi))
            self.canvas.coords(self.minute_hands[i], i*300+150, 150, i*300+150-80*cos(
                (self.clocks[i].minute+15)/30*pi+self.clocks[i].second/1800*pi),
                150-80*sin((self.clocks[i].minute+15)/30*pi+self.clocks[i].second/1800*pi))
            self.canvas.coords(self.second_hands[i], i*300+150, 150, i*300+150-120*cos(
                (self.clocks[i].hand_second+self.clocks[i].precise_second+15)/30*pi),
                150-120*sin((self.clocks[i].hand_second+self.clocks[i].precise_second+15)/30*pi))
            self.canvas.itemconfig(self.digital_clocks[i], text="{:02d}:{:02d}:{:02d}".format(
                abs(self.clocks[i].hour), abs(self.clocks[i].minute), abs(self.clocks[i].second)))
        self.root.after_idle(self.update_clocks)  # Schedule process
