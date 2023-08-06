from tkinter import filedialog,messagebox,ttk;import tkinter;from tkinter import *
import easygui;from tkPlus import functions
def msgbox(content,title="",type="simple",buttontext="确定",image=None,root=None):
    '''显示普通弹窗\ncontent：内容\ntype:选填，显示样式。\nbuttontext：选填，按钮文本\nimage：图片\nroot：父容器，选填。\ntitle：抬头'''
    if type=="simple":
        easygui.msgbox(msg=content, title=title, ok_button=buttontext, image=image, root=root)
    elif type=="info"or type=="infomation":
        messagebox.showinfo(title,content)
    elif type=="warning":
        messagebox.showwarning(title,content)
    else:
        messagebox.showerror(title,content)
def askbox(content,title="",type="simple",buttontext="确定",notext="取消",image=None,root=None):
    '''显示普通弹窗\ncontent：内容\ntype:选填，显示样式。\nbuttontext：选填，按钮文本\nimage：图片\nroot：父容器，选填。\ntitle：抬头\nnotext:取消按钮，选填。'''
    if type=="simple":
        easygui.ccbox(msg=content, title=title, choices=(buttontext, notext), image=image)
    elif type=="info"or type=="infomation":
        messagebox.showinfo(title,content)
    elif type=="warning":
        messagebox.showwarning(title,content)
    elif not(type=="input"):
        messagebox.showerror(title,content)
    else:
        msg=content
        window = tkinter.Tk()
        txt = Label(window, text="输入<native JS>需要的信息：")
        txt.pack()
        window.title("信息输入")
        etr = functions.EntryWithPlaceholder(window, placeholder=str(msg) + ":")
        etr.pack()
        i = messagebox.askokcancel("<native JS>需要某些信息", "脚本提示：" + str(msg) + "，请输入信息然后点击“确定”。")
        if i:
            return etr.get()
        else:
            return None