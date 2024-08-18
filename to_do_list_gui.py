from tkinter import *
from tkinter import ttk

class todo:
    def init_(self,root):
        self.root=root
        self.root.title("to-do-list")
        self.root.geometry("650x410+300+150")

        self.label =Label(self.root,text="todolist app",font="ariel,25 bold",width=10,bd=5,bg="orange",fg="black")
        self.label.pack(side="top",fill=BOTH)


def main():
    root=Tk()
    ui=todo(root)
    root.mainloop()

if __name__ == "__main__":
    main()    



