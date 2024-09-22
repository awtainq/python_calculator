from tkinter import *
from math import floor
import re

class Calculator:
    def __init__(self, root):
        self.cur = ""
        self.prev = ""
        self.h = 2
        self.w = 5
        self.root = root
        self.create_widgets()
        self.bind_events()

    def to_str(self, number):
        return str(int(number)) if number.is_integer() else str(number)

    def split(self):
        return [i for i in re.split(r'[divmod+\-/*]', self.cur) if i.strip()]

    def replace_in_string(self, s):
        replacements = {
            '++': '+', '--': '+', '+-': '-', '-+': '-',
            '*+': '*', '/+': '/', 'mod+': 'mod', 'div+': 'div'
        }
        for old, new in replacements.items():
            s = s.replace(old, new)
        return s

    def change_cur(self, symbl):
        result = self.split()
        if self.cur != "Error":
            if len(self.cur) == 1 and self.cur[-1] == "0" and (symbl.isdigit() or symbl == "-"):
                self.cur = symbl
            elif self.cur and (self.cur[-1] in "+-/*%" and self.cur[-2] in "oi") and symbl in "+-/*%moddiv":
                self.cur = self.cur[:-3] + symbl if self.cur[-1] in "dv" else self.cur[:-1] + symbl
            elif (self.cur == "" and symbl.isdigit()) or (self.cur and self.cur[-1].isdigit() and ((not "." in result[-1] and symbl == ".") or symbl != ".")) or (self.cur and symbl.isdigit()):
                self.cur += symbl
        self.frame_now.config(text=self.cur)

    def plsmin(self):
        result = self.split()
        if result:
            result_len = len(result[-1])
            if self.cur != "Error":
                try:
                    if len(result) == 1:
                        self.cur = self.to_str(float(self.cur) * (-1))
                    else:
                        self.cur = self.cur[:-result_len] + self.to_str(float(self.cur[-result_len:]) * (-1))
                except Exception:
                    self.cur += "-"
                self.cur = self.replace_in_string(self.cur)
        self.frame_now.config(text=self.cur)

    def clear(self):
        self.cur, self.prev = "", ""
        self.frame_now.config(text=self.cur)
        self.frame_prev.config(text=self.prev)

    def clear_one(self):
        if self.cur:
            self.cur = self.cur[:-3] if self.cur[-1] in "dv" else self.cur[:-1]
        self.frame_now.config(text=self.cur)

    def evaluate(self):
        if self.cur and len(self.split()) > 1:
            s = self.cur.replace("mod", "%").replace("div", "//")
            try:
                self.prev = self.cur
                self.cur = self.to_str(eval(s))
            except Exception:
                self.cur = "Error"
            self.frame_now.config(text=self.cur)
            self.frame_prev.config(text=self.prev)

    def keyboard(self, event):
        key = event.char
        if key.isdigit() or key in "+-/*.":
            self.change_cur(key)
        elif key in ('\r', '='):
            self.evaluate()
        elif key == '\b':
            self.clear_one()
        elif key in ('c', 'C'):
            self.clear()
        elif key in ('m', 'M'):
            self.change_cur("mod")
        elif key in ('d', 'D'):
            self.change_cur("div")

    def adjust_font_size(self, event):
        new_width = event.width
        font_size_now = max(20, int(new_width / 20 + 10))
        font_size_prev = max(12, int(new_width / 30 + 5))
        button_font_size = max(10, int(new_width / 40))

        self.frame_now.config(font=("Arial", font_size_now, "bold"))
        self.frame_prev.config(font=("Arial", font_size_prev))
        for button in self.buttons:
            button.config(font=("Arial", button_font_size))

        self.btn_back.config(font=("Arial", button_font_size))
        self.btn_AC.config(font=("Arial", button_font_size))
        self.btn_pm.config(font=("Arial", button_font_size))
        self.btn_mod.config(font=("Arial", button_font_size))
        self.btn_div.config(font=("Arial", button_font_size))
        self.btn_division.config(font=("Arial", button_font_size))
        self.btn_mul.config(font=("Arial", button_font_size))
        self.btn_min.config(font=("Arial", button_font_size))
        self.btn_pls.config(font=("Arial", button_font_size))
        self.btn_eql.config(font=("Arial", button_font_size))
        self.btn_point.config(font=("Arial", button_font_size))
        self.btn_0.config(font=("Arial", button_font_size))

    def create_widgets(self):
        self.root.title("Calculator")
        self.root.resizable(True, True)
        self.root.minsize(230, 300)

        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)

        self.frame_prev = Label(self.root, text="", width=self.w, height=1, font="Arial 12", anchor=E)
        self.frame_prev.grid(column=0, row=0, columnspan=5, sticky="nsew")
        self.frame_now = Label(self.root, text=self.cur, width=self.w, height=1, font="Arial 20 bold", anchor=E)
        self.frame_now.grid(column=0, row=1, columnspan=5, sticky="nsew")

        self.btn_back = Button(self.root, text="<-", width=self.w, height=self.h, command=self.clear_one)
        self.btn_back.grid(row=2, column=4, sticky="nsew")
        self.btn_AC = Button(self.root, text="AC", width=self.w, height=self.h, command=self.clear)
        self.btn_AC.grid(row=2, column=0, sticky="nsew")
        self.btn_pm = Button(self.root, text="+/-", width=self.w, height=self.h, command=self.plsmin)
        self.btn_pm.grid(row=4, column=4, sticky="nsew")
        self.btn_mod = Button(self.root, text="mod", width=self.w, height=self.h, command=lambda: self.change_cur("mod"))
        self.btn_mod.grid(row=2, column=1, sticky="nsew")
        self.btn_div = Button(self.root, text="div", width=self.w, height=self.h, command=lambda: self.change_cur("div"))
        self.btn_div.grid(row=2, column=2, sticky="nsew")
        self.btn_division = Button(self.root, text="/", width=self.w, height=self.h, command=lambda: self.change_cur("/"))
        self.btn_division.grid(row=2, column=3, sticky="nsew")
        self.btn_mul = Button(self.root, text="*", width=self.w, height=self.h, command=lambda: self.change_cur("*"))
        self.btn_mul.grid(row=3, column=4, sticky="nsew")
        self.btn_min = Button(self.root, text="-", width=self.w, height=self.h, command=lambda: self.change_cur("-"))
        self.btn_min.grid(row=3, column=3, sticky="nsew")
        self.btn_pls = Button(self.root, text="+", width=self.w, height=self.h, command=lambda: self.change_cur("+"))
        self.btn_pls.grid(row=4, column=3, sticky="nsew")
        self.btn_eql = Button(self.root, text="=", width=self.w * 2, height=self.h * 2, command=self.evaluate, bg="orange")
        self.btn_eql.grid(row=5, column=3, columnspan=2, rowspan=2, sticky="nsew")
        self.btn_point = Button(self.root, text=".", width=self.w, height=self.h, command=lambda: self.change_cur("."))
        self.btn_point.grid(row=6, column=2, sticky="nsew")
        self.btn_0 = Button(self.root, text="0", width=floor(self.w * 2.4), height=self.h, command=lambda: self.change_cur("0"))
        self.btn_0.grid(row=6, column=0, columnspan=2, sticky="nsew")

        self.buttons = []
        k = 0
        for i in range(3):
            for j in range(3):
                btn = Button(self.root, text=str(9 - k), width=self.w, height=self.h, command=lambda idx=k: self.change_cur(str(9 - idx)))
                btn.grid(row=3 + i, column=j, sticky="nsew")
                self.buttons.append(btn)
                k += 1

    def bind_events(self):
        self.root.bind("<Key>", self.keyboard)
        self.root.bind("<Configure>", self.adjust_font_size)


if __name__ == "__main__":
    root = Tk()
    calculator = Calculator(root)
    root.mainloop()