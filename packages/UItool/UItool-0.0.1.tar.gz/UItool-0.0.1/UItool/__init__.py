from tkinter import *;from tkinter import messagebox,filedialog,ttk;import tkinter
class windowExitError(Exception):pass
class window(object):
    def __init__(self):
        self.Tk=tkinter.Tk()
        self.exited=False
    def close(self):
        if self.exited==False:
            self.Tk.withdraw()
        else:
            err=windowExitError("The window to close is exited")
            raise(err)
        pass
    def setSize(self,*size):
        if type(size)[0]==str and len(size)==1:
            self.Tk.geometry(size)
        elif len(size)==2:
            self.Tk.geometry(str(size[0])+"x"+str(size[1]))
        else:
            err=TypeError("getSize expected at most 1 arguments, got 2")
            raise(err)
        pass
    def exit(self):
        self.Tk.destroy()
        self.exited=True
    def xy(self,x=0,y=0):
        if self.exited==True:
            err=windowExitError("The window to set xy is exited")
            raise(err)
        self.Tk.geometry("+"+str(x)+"+"+str(y))
    def convertToTk(self):
        if self.exited==False:
            return self.Tk
        else:
            err=windowExitError("The window to convert is exited")
            raise(err)
        pass
    def title(self,title):
        if self.exited==True:
            err=windowExitError("The window to set title is exited")
            raise(err)
        self.Tk.title(title)
    def icon(self,name):
        if self.exited==True:
            err=windowExitError("The window to set icon is exited")
            raise(err)
        try:
            self.Tk.iconbitmap(name)
        except:
            err=FileNotFoundError("Icon\""+name+"\"is not found!")
            raise(err)
        pass
    def on_exit(self,func):
        self.Tk.protocol("WM_DELETE_WINDOW",func)
    def ext(self,txt):
        return eval("self.Tk."+txt)
    def protocol(self,name=None,func=None):
        self.Tk.protocol(name,func)
    def attributes(self,attr,e):
        self.Tk.attributes(attr,e)
    pass
class little_window(window):
    def __init__(self):
        self.Tk=Toplevel()
        self.closed=False
        self.exited=False
    pass
"_________________________________end_______________________________"
version="0.0.1"
is_latest_version=True