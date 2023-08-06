try:
    import UItool,tkinter,tkPlus;from UItool import *;from tkinter import *;from tkPlus import *
except:
    print("请安装本作者的tkinter扩展库tkPlus！")
class label(tkinter.Label):
    def __init__(self,master,text="",image=None,font=["微软雅黑",15]):
        if type(master)!=tkinter.Tk and type(master)!=tkinter.Toplevel:
            master=master.Tk
        else:
            master=master
        if image:
            Label.__init__(self,master,text=text,image=image,font=font)
        else:
            Label.__init__(self,master,text=text,font=font)
    def display(self,type=tkinter.Label.pack,**kwargs):
        str=getName(type)+"("
        for i in kwargs.keys():
            str+=(i+"="+kwargs[i])
        str+=')'
        exec(str)
    def toTk(self):
        return self
def getName(obj):
    return [name for name in namespace if globals()[name] is obj]
class button(tkinter.Button):
    def __init__(self,master,text="",image=None,font=["微软雅黑",15],
                 bg="white",fg="black"):
        if type(master)!=tkinter.Tk and type(master)!=tkinter.Toplevel:
            master=master.Tk
        else:
            master=master
        if image:
            Label.__init__(self,master,text=text,image=image,bg=bg,fg=fg)
        else:
            Label.__init__(self,master,text=text,bg=bg,fg=fg)
    def display(self,type=tkinter.Label.pack,**kwargs):
        str=getName(type)+"("
        for i in kwargs.keys():
            str+=(i+"="+kwargs[i])
        str+=')'
        exec(str)
    def toTk(self):
        return self
