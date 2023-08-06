import tkinter as tk
import time

from threading import Thread


_root_window = "None"


def get_root_window():
    global _root_window
    if _root_window is None:
        _root_window = tk.Tk()
        _root_window.title("Super Prog Auto Logger")
        _root_window.minsize(300, 300)
    return _root_window


def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


class Window:

    __tk_root = None
    __instance = None

    class __Root(tk.Frame):
        pass

    def __new__(cls, name: str):
        print("__new__")
        if Window.__instance is None:
            Window.__instance = object.__new__(cls)
            Window.__instance.__singleton_init()
            Window.__get_tk_root().title(name)
            center(Window.__get_tk_root())
            #Window.__get_tk_root().eval('tk::PlaceWindow . center')

        return Window.__instance

    def loop(self, *args, **kwargs):
        for thread in self.__threads:
            thread.start()
        self.__root.mainloop(*args, **kwargs)

    def add_button(self, *args, **kwargs):
        new_button = tk.Button(self.__root, *args, **kwargs)
        self.__buttons.append(new_button)
        new_button.pack()

    def pack(self, *args, **kwargs):
        self.__root.pack(*args, **kwargs)

    def __singleton_init(self):
        self.__root = Window.__Root(Window.__get_tk_root())
        self.__buttons = []
        self.__threads = []
        self.add_button(text="Hello World\n(click me)", command=self.say_hi)
        self.add_button(text="QUIT", fg="red", command=Window.__get_tk_root().destroy)
        #self.quit = tk.Button(root, text="QUIT", fg="red", command=Window.__get_tk_root().destroy)
        #self.quit.pack(side="bottom")
        self.__root.pack()

    def create_widget(self):
        print("create_widget")
        #self.pack()

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=Window.__get_tk_root().destroy)
        self.quit.pack(side="bottom")

    @staticmethod
    def __get_tk_root():
        if Window.__tk_root is None:
            Window.__tk_root = tk.Tk()
            Window.__tk_root.minsize(400, 180)
            Window.__tk_root.update()

        return Window.__tk_root

    def say_hi(self):
        print("hi there, everyone!")

    def set_loop(self, other_loop):
        self.__threads.append(Thread(target=other_loop, daemon=True, args=(self,)))

    def input(self, label, _type=str):
        for child in self.__root.winfo_children():
            child.configure(state='disable')
        top = tk.Tk()
        L1 = tk.Label(top, text=label)
        L1.pack(side=tk.LEFT)
        E1 = tk.Entry(top, bd=5)
        E1.pack(side=tk.RIGHT)

        top.mainloop()


def test_loop(win):
    while True:
        print("HELLOE TOTTTTT")
        win.input("Enter a number")
        time.sleep(1)


if __name__ == '__main__':
    win = Window("Test UFTERM")
    win = Window("Test UFTERM")
    win = Window("Test UFTERM")
    win.set_loop(test_loop)
    win.loop()



def main():
    root = tk.Tk()
    root.minsize(1000, 200)
    root.update()
    root.attributes('-alpha', 0.0)
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)
    frm = tk.Frame(root, bd=4, relief='raised')
    frm.pack(fill='x')
    lab = tk.Label(frm, text='Hello World!', bd=4, relief='sunken')
    lab.pack(ipadx=4, padx=4, ipady=4, pady=4, fill='both')
    center(root)
    root.attributes('-alpha', 1.0)
    root.mainloop()
