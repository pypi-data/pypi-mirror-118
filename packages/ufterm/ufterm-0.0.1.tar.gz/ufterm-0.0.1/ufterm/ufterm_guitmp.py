import tkinter as tk
import time
from abc import ABC
from threading import Thread
from typing import List
import darkdetect
from os import path

from ufterm_decorator import staticproperty
from ufterm_utils import noop
from ufterm_register import Register


ICON_PATH = "icon.ico"


class _DummyException(Exception):
    pass


class _Window(ABC, tk.Misc, tk.Wm):

    def __init__(self):
        self.__geometry_updated_id = None
        self.__inner_width = self.__inner_height = None
        self.__x = self.__y = None
        self.__theme = None
        self.__theme_updated_id = None
        self.bind('<Configure>', self.on_configure)

    @property
    def frame_size(self):
        return self.winfo_rootx() - self.x

    @property
    def titlebar_height(self):
        return self.winfo_rooty() - self.y

    @property
    def width(self):
        return self.inner_width + 2 * self.frame_size

    @property
    def height(self):
        return self.inner_height + self.titlebar_height + self.frame_size

    @property
    def inner_width(self) -> int:
        if self.__inner_width is None:
            self.__inner_width = self.winfo_width()
        return self.__inner_width

    @property
    def inner_height(self) -> int:
        if self.__inner_height is None:
            self.__inner_height = self.winfo_height()
        return self.__inner_height

    @property
    def x(self) -> int:
        if self.__x is None:
            self.__x = self.winfo_x()
        return self.__x

    @property
    def y(self) -> int:
        if self.__y is None:
            self.__y = self.winfo_y()
        return self.__y

    @property
    def theme(self) -> int:
        if self.__theme is None:
            self.__theme = darkdetect.theme()
        return self.__theme

    @property
    def current_geometry(self) -> str:
        return f"{self.inner_width}x{self.inner_height}+{self.winfo_rootx()}+{self.winfo_rooty()}"

    def center(self, offset_x: int = 0, offset_y: int = 0):
        """
        centers the tkinter window in the middle of the screen
        """
        self.update_idletasks()
        x = RootWindow.screen_width // 2 - self.width // 2 + offset_x
        y = RootWindow.screen_height // 2 - self.height // 2 + offset_y
        print("centering", '{}x{}+{}+{}'.format(self.inner_width, self.inner_height, x, y))
        self.geometry('{}x{}+{}+{}'.format(self.inner_width, self.inner_height, x, y))

    def on_configure(self, event):
        if event.widget == self:
            try:
                if self.inner_width != event.width:
                    self.__inner_width = None
                    raise _DummyException
                elif self.inner_height != event.height:
                    self.__inner_height = None
                    raise _DummyException
                elif self.x != event.x:
                    self.__x = None
                    raise _DummyException
                elif self.y != event.y:
                    self.__y = None
                    raise _DummyException
                elif self.theme != darkdetect.theme():
                    self.__theme = None
                    if self.__theme_updated_id is not None:
                        self.after_cancel(self.__theme_updated_id)
                    self.__theme_updated_id = self.after(1000, self.on_theme_updated)
            except _DummyException:
                if self.__geometry_updated_id is not None:
                    self.after_cancel(self.__geometry_updated_id)
                self.__geometry_updated_id = self.after(1000, self.on_geometry_updated)

    def on_geometry_updated(self):
        pass

    def on_theme_updated(self):
        pass

    def notify_user(self):
        self.bell()
        self.deiconify()


class RootWindow(tk.Tk, _Window):

    __instance = None

    def __new__(cls, *args, **kwargs):
        if RootWindow.__instance is None:
            RootWindow.__instance = object.__new__(cls)
            RootWindow.__instance.__initialized = False
        return RootWindow.__instance

    def __init__(self, **kwargs):
        if not self.__initialized:
            self.__initialized = True
            tk.Tk.__init__(self, **kwargs)
            _Window.__init__(self)
            self.minsize(400, 220)
            self.reset_last_geometry()
            self.__resizing = False
            if path.isfile(ICON_PATH):
                self.iconphoto(False, tk.PhotoImage(file="icon.png"))

    def reset_last_geometry(self):
        last_geometry = Register("last_geometry")
        if last_geometry is None:
            self.center()
        else:
            self.geometry(last_geometry)

    def on_geometry_updated(self):
        Register['last_geometry'] = self.current_geometry

    def on_theme_updated(self):
        print("hello theme updated", self.theme)

    @staticproperty
    def screen_width() -> int:
        if RootWindow.__instance is None:
            RootWindow()
        return RootWindow.__instance.winfo_screenwidth()

    @staticproperty
    def screen_height() -> int:
        if RootWindow.__instance is None:
            RootWindow()
        return RootWindow.__instance.winfo_screenheight()


class PopupWindow(tk.Toplevel, _Window):

    def __init__(self, master: tk.Wm = None, title: str = None, **kw):
        tk.Toplevel.__init__(self, master, **kw)
        _Window.__init__(self)
        # Disable the Close Window Control Icon
        self.protocol("WM_DELETE_WINDOW", noop)
        self.title(title)
        self.attributes('-toolwindow', True)
        self.exit_btn = tk.Button(self, text="Click here to Close", command=self.destroy)
        self.exit_btn.pack()


class MenuListWindow(tk.Toplevel, _Window):

    def __init__(self, master: tk.Wm = None, choices: List[str] = (), **kw):
        super().__init__(master, **kw)
        self.overrideredirect(True)
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.listbox.configure(bg='grey')

        #self.scrollbar.geometry("200x200")
        #self.geometry("200x200")
        #self.scrollbar.columnconfigure(0, weight=1)
        self.labels = []
        self.add_choices(choices)
        # Disable the Close Window Control Icon

    def add_choices(self, choices: List[str]):
        for choice in choices:
            self.add_choice(choice)

    def add_choice(self, choice: str):
        self.listbox.insert(tk.END, choice)
        self.listbox.insert(tk.END, choice)
        self.listbox.insert(tk.END, choice)
        self.listbox.insert(tk.END, choice)
        self.listbox.insert(tk.END, choice)
        self.listbox.insert(tk.END, choice)
        self.listbox.insert(tk.END, choice)
        self.listbox.insert(tk.END, choice)
        self.listbox.insert(tk.END, choice)
        self.listbox.insert(tk.END, choice)
        self.listbox.insert(tk.END, choice)
        self.listbox.insert(tk.END, choice)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar.config(command=self.listbox.yview)
        #label = tk.Label(self.scrollbar, text=choice, borderwidth=2, relief="solid")
        #label.grid(sticky=tk.E + tk.W)
        #label.bind("<Button-1>", self.select_choice)
        #self.labels.append(label)

    def select_choice(self, event):
        print("select_choice", event)
        self.destroy()


class Select(tk.Frame):

    def __init__(self, master: tk.Wm = None, choices: List[str] = (), **kw):
        super().__init__(master, **kw)
        self.labels = []
        self.choices = choices
        self.button = tk.Button(self, text="tt", command=self.open)
        self.button.pack()

    def open(self, event=None):
        print("open", event)
        menu = MenuListWindow(self.master, ["toto", "tata"])
        print("200x200+%d+%d" % (self.winfo_rootx(), self.winfo_rooty()))
        menu.geometry("%dx%d+%d+%d" % (self.winfo_width() + 100, self.winfo_height() + 100, self.winfo_rootx(), self.winfo_rooty() + self.winfo_height()))

    def real_x(self):
        return self.winfo_rootx()


def main():
    Register.record_in_file(r"~\test")
    root_wm = RootWindow()
    root_wm2 = RootWindow()
    root_wm2 = RootWindow()
    root_wm2 = RootWindow()

    popup1 = PopupWindow(root_wm, "sqdqsd")
    #popup1.center(1000, 100)
    #popup2 = PopupWindow(root_wm, "aaaa")

    choice = Select(root_wm, ["toto", "tata"])
    choice.pack()
    #choice = MenuListWindow(root_wm, ["toto", "tata"])

    scroll = tk.Scrollbar(root_wm)

    label1 = tk.Label(scroll, text="ttt")
    label2 = tk.Label(scroll, text="toto")
    label1.pack()
    label2.pack()
    tk.Label(scroll, text="toto").pack()
    tk.Label(scroll, text="toto").pack()
    tk.Label(scroll, text="toto").pack()
    tk.Label(scroll, text="toto").pack()
    tk.Label(scroll, text="toto").pack()
    tk.Label(scroll, text="toto").pack()
    tk.Label(scroll, text="toto").pack()
    tk.Label(scroll, text="toto").pack()
    tk.Label(scroll, text="toto").pack()
    tk.Label(scroll, text="toto").pack()
    tk.Label(scroll, text="toto").pack()
    tk.Label(scroll, text="toto").pack()

    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    root_wm.title("toto")
    root_wm.mainloop()


if __name__ == '__main__':
    print(darkdetect.theme())
    main()
