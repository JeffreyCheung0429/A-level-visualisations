from tkinter.messagebox import showinfo


class About:
    def __init__(self) -> None:
        self.title = "Clock"
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

    def popupShowinfo(self) -> None:
        """Message box for copyright"""
        showinfo("About " + self.title, "Version: " + self.ver
                 + " September 2022\n\nAuthor: Jeffrey Cheung\n\n"
                 + self.licenceStr)
