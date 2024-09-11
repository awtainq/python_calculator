from tkinter import *
from math import floor
import re

cur = ""
prev = ""
h = 2
w = 5

def to_str(number):
    if number.is_integer():
        return str(int(number))
    else:
        return str(number)

def split():
    global cur
    return [i for i in re.split(r'[divmod+\-/*]', cur) if i.strip()]

def replace_in_string(s):
    while '++' in s or '--' in s or '+-' in s or '-+' in s:
        s = s.replace('++', '+')
        s = s.replace('--', '+')
        s = s.replace('+-', '-')
        s = s.replace('-+', '-')
        s = s.replace('*+', '*')
        s = s.replace('/+', '/')
        s = s.replace('mod+', 'mod')
        s = s.replace('div+', 'div')
    return s

def change_cur(symbl):
    global cur
    result = split()
    if cur != "Error":
        if len(cur) == 1 and cur[-1] == "0" and (symbl.isdigit() or symbl == "-"):
            cur = symbl
        elif cur != "" and (cur[-1] in "+-/*%" and cur[-2] in "oi") and symbl in "+-/*%moddiv":
            if cur[-1] in "dv":
                cur = cur[:-3] + symbl
            else:
                cur = cur[:-1] + symbl
        elif (cur == "" and symbl.isdigit()) or (cur != "" and cur[-1].isdigit() and ((not "." in result[-1] and symbl == ".") or symbl != ".")) or (cur != "" and symbl.isdigit()):
            cur += symbl
    frame_now.config(text=cur)

def plsmin():
    global cur
    result = split()
    if len(result) > 0:
        result_len = len(result[-1])
        if cur != "Error":
            try:
                if len(result) == 1:
                    cur = to_str(float(cur) * (-1))
                else:
                    cur = cur[:-result_len] + to_str(float(cur[-result_len:]) * (-1))
            except Exception:
                cur = cur + "-"
            cur = replace_in_string(cur)
    frame_now.config(text=cur)

def clear():
    global cur, prev
    cur, prev = "", ""
    frame_now.config(text=cur)
    frame_prev.config(text=prev)

def clear_one():
    global cur
    if len(cur) > 0:
        if cur[-1] == "d" or cur[-1] == "v":
            cur = cur[:-3]
        else:
            cur = cur[:-1]
    frame_now.config(text=cur)

def evaluate():
    global cur, prev
    if cur != "" and len(split()) > 1:
        s = cur
        s = s.replace("mod", "%")
        s = s.replace("div", "//")
        print(s)
        try:
            prev = cur
            cur = to_str(eval(s))
        except Exception:
            cur = "Error"
        frame_now.config(text=cur)
        frame_prev.config(text=prev)

def Keyboard(event):
    key = event.char
    if key.isdigit() or key in "+-/*.":
        change_cur(key)
    elif key == '\r' or key == "=":
        evaluate()
    elif key == '\b':
        clear_one()
    elif key == 'c' or key == 'C':
        clear()
    elif key == "m" or key == "M":
        change_cur("mod")
    elif key == "d" or key == "D":
        change_cur("div")


def adjust_font_size(event):
    new_width = event.width
    new_height = event.height
    font_size_now = max(20, int(new_width / 20+10))
    font_size_prev = max(12, int(new_width / 30+5))
    frame_now.config(font=("Arial", font_size_now, "bold"))
    frame_prev.config(font=("Arial", font_size_prev))
    button_font_size = max(10, int(new_width / 40))
    for button in buttons:
        button.config(font=("Arial", button_font_size))

    btn_back.config(font=("Arial", button_font_size))
    btn_AC.config(font=("Arial", button_font_size))
    btn_pm.config(font=("Arial", button_font_size))
    btn_mod.config(font=("Arial", button_font_size))
    btn_div.config(font=("Arial", button_font_size))
    btn_division.config(font=("Arial", button_font_size))
    btn_mul.config(font=("Arial", button_font_size))
    btn_min.config(font=("Arial", button_font_size))
    btn_pls.config(font=("Arial", button_font_size))
    btn_eql.config(font=("Arial", button_font_size))
    btn_point.config(font=("Arial", button_font_size))
    btn_0.config(font=("Arial", button_font_size))


root = Tk()
root.title("Calculator")
root.resizable(True, True)
root.bind("<Key>", Keyboard)
root.bind("<Configure>", adjust_font_size)
root.minsize(230, 300)

for i in range(7):
    root.grid_rowconfigure(i, weight=1)
for i in range(5):
    root.grid_columnconfigure(i, weight=1)

frame_prev = Label(root, text="", width=w, height=1, font="Arial 12", anchor=E)
frame_prev.grid(column=0, row=0, columnspan=5, sticky="nsew")
frame_now = Label(root, text=cur, width=w, height=1, font="Arial 20 bold", anchor=E)
frame_now.grid(column=0, row=1, columnspan=5, sticky="nsew")

btn_back = Button(root, text="<-", width=w, height=h, command=clear_one)
btn_back.grid(row=2, column=4, sticky="nsew")
btn_AC = Button(root, text="AC", width=w, height=h, command=clear)
btn_AC.grid(row=2, column=0, sticky="nsew")
btn_pm = Button(root, text="+/-", width=w, height=h, command=plsmin)
btn_pm.grid(row=4, column=4, sticky="nsew")
btn_mod = Button(root, text="mod", width=w, height=h, command=lambda: change_cur("mod"))
btn_mod.grid(row=2, column=1, sticky="nsew")
btn_div = Button(root, text="div", width=w, height=h, command=lambda: change_cur("div"))
btn_div.grid(row=2, column=2, sticky="nsew")
btn_division = Button(root, text="/", width=w, height=h, command=lambda: change_cur("/"))
btn_division.grid(row=2, column=3, sticky="nsew")
btn_mul = Button(root, text="*", width=w, height=h, command=lambda: change_cur("*"))
btn_mul.grid(row=3, column=4, sticky="nsew")
btn_min = Button(root, text="-", width=w, height=h, command=lambda: change_cur("-"))
btn_min.grid(row=3, column=3, sticky="nsew")
btn_pls = Button(root, text="+", width=w, height=h, command=lambda: change_cur("+"))
btn_pls.grid(row=4, column=3, sticky="nsew")
btn_eql = Button(root, text="=", width=w * 2, height=h * 2, command=evaluate, bg="#orange")
btn_eql.grid(row=5, column=3, columnspan=2, rowspan=2, sticky="nsew")
btn_point = Button(root, text=".", width=w, height=h, command=lambda: change_cur("."))
btn_point.grid(row=6, column=2, sticky="nsew")
btn_0 = Button(root, text="0", width=floor(w * 2.4), height=h, command=lambda: change_cur("0"))
btn_0.grid(row=6, column=0, columnspan=2, sticky="nsew")

k = 0
buttons = []
for i in range(3):
    for j in range(3):
        btn = Button(root, text=str(9 - k), width=w, height=h, command=lambda idx=k: change_cur(str(9 - idx)))
        btn.grid(row=3 + i, column=j, sticky="nsew")
        buttons.append(btn)
        k += 1

root.mainloop()