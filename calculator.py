from tkinter import *
from math import floor
import re

cur=""
prev=""
h=2
w=6

def to_str(number):
    if number.is_integer():
        return str(int(number))
    else:
        return str(number)

def split():
    global cur
    return [i for i in re.split(r'[divmod+\-/*]',cur) if i.strip()]

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
    if cur!="Error":
        if len(cur)==1 and cur[-1]=="0" and (symbl.isdigit() or symbl=="-"):
            cur=symbl
        elif cur!="" and (cur[-1] in "+-/*%" and cur[-2] in "oi") and symbl in "+-/*%moddiv" :
            if cur[-1] in "dv":
                cur = cur[:-3] + symbl
            else:
                cur = cur[:-1] + symbl
        elif (cur=="" and symbl.isdigit()) or (cur!="" and cur[-1].isdigit() and ((not "." in result[-1] and symbl==".") or symbl!=".")) or (cur!="" and symbl.isdigit()):
            cur += symbl
    frame_now.config(text=cur)

def plsmin():
    global cur
    result = split()
    if len(result)>0:
        result_len = len(result[-1])
        if cur!="Error":
            try:
                if len(result)==1:
                    cur = to_str(float(cur)*(-1))
                else:
                        cur = cur[:-result_len] + to_str(float(cur[-result_len:])*(-1))
            except Exception:
                cur = cur + "-"
            cur = replace_in_string(cur)
    frame_now.config(text=cur)

def clear():
    global cur, prev
    cur,prev="",""
    frame_now.config(text=cur)
    frame_prev.config(text=prev)

def clear_one():
    global cur
    if len(cur)>0:
        if cur[-1]=="d" or cur[-1]=="v":
            cur = cur[:-3]
        else:
            cur = cur[:-1]
    frame_now.config(text=cur)
def evaluate():
    global cur, prev
    if cur!="" and len(split())>1:
        s = cur
        s = s.replace("mod","%")
        s = s.replace("div", "//")
        print(s)
        try:
            prev = cur
            cur = to_str(eval(s))
        except Exception:
            cur = "Error"
        frame_now.config(text=cur)
        frame_prev.config(text=prev)

root = Tk()
root.title("Calculator")
root.resizable(False, False)

frame_prev = Label(root, text="",width=floor(w*4.5),font="Arial 12",anchor=E)
frame_prev.grid(column=0,row=0,columnspan=6)
frame_now = Label(root, text=cur,width=floor(w*2.5),font="Arial 20 bold",anchor=E)
frame_now.grid(column=0,row=1,columnspan=6)

btn_back = Button(root, text="<-", width=w,height=h,command=clear_one)
btn_back.grid(row=2, column=5)
btn_AC = Button(root, text="AC", width=w,height=h,command=clear)
btn_AC.grid(row=2, column=0)
btn_pm = Button(root, text="+/-", width=w,height=h,command=plsmin)
btn_pm.grid(row=4, column=5)
btn_mod = Button(root, text="mod", width=w,height=h,command=lambda: change_cur("mod"))
btn_mod.grid(row=2, column=1)
btn_div = Button(root, text="div", width=w,height=h,command=lambda: change_cur("div"))
btn_div.grid(row=2, column=2)
btn_division = Button(root, text="/", width=w,height=h,command=lambda: change_cur("/"))
btn_division.grid(row=2, column=3)
btn_mul = Button(root, text="*", width=w,height=h,command=lambda: change_cur("*"))
btn_mul.grid(row=3, column=5)
btn_min = Button(root, text="-", width=w,height=h,command=lambda: change_cur("-"))
btn_min.grid(row=3, column=3)
btn_pls = Button(root, text="+", width=w,height=h,command=lambda: change_cur("+"))
btn_pls.grid(row=4, column=3)
btn_eql = Button(root, text="=", width=floor(w*2.4),height=floor(h*2.8),command=evaluate, bg="orange")
btn_eql.grid(row=5, column=3, columnspan=3,rowspan=2)
btn_point = Button(root, text=".", width=w,height=h,command=lambda: change_cur("."))
btn_point.grid(row=6, column=2)
btn_0 = Button(root, text="0", width=floor(w*2.4),height=h,command=lambda: change_cur("0"))
btn_0.grid(row=6, column=0, columnspan=2)

k = 0
buttons = []
for i in range(3):
    for j in range(3):
        btn = Button(root, text=str(9 - k), width=w, height=h, command=lambda idx=k: change_cur(str(9-idx)))
        btn.grid(row=3 + i, column=j)
        buttons.append(btn)
        k += 1

root.mainloop()