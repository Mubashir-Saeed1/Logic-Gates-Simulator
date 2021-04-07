from tkinter import *
a="hello"
def savefile():
        top = Tk()
        def print_contents(event) :
                print(text.get(1.0, END))
                global a
                a=text.get(1.0, END)
                top.destroy()
                
        label = Label(top, text='Enter name of file you wish to save')
        label.pack()
        text = Text(width="50", height="1")

        text.insert(END, "a.jpg")
        text.pack()


        button1 = Button(top, text='Enter')
        button1.bind('<Button-1>', print_contents)
        button1.pack()



        mainloop()

def showfile():
        top = Tk()
        f = open("help.txt","r")
        contents = f.read()
        label = Label(top, text=contents)
        label.pack()
        f.close()
        mainloop()
        
                
