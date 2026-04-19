from tkinter import *
from tkinter import scrolledtext

def send():
    writescroll()
    inPut.delete(0,END)

def writescroll():
    scrolledScreen.config(state="normal")
    scrolledScreen.insert(END,"ahdks")
    scrolledScreen.config(state="disabled")




chatScreen=Tk()
scrolledScreen=scrolledtext.ScrolledText(chatScreen,width=40,height=20,state='disable')
scrolledScreen.pack()

inPut=Entry(chatScreen,width=40)
inPut.pack(side='left',pady=5,padx=5)
mybutto=Button(chatScreen,text='send',command=send)
mybutto.pack(side='left',pady=5)
chatScreen.mainloop()