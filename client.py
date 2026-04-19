import socket
import threading
from tkinter import *

def send():
    msg = entry.get()
    if msg:
        s.send(msg.encode())
        frame.insert(END, "Fares: " + msg + "\n")
        entry.delete(0, END)

def receive():
    while True:
        try:
            msg = s.recv(1024).decode()
            if msg:
                frame.insert(END, "Eslam: " + msg + "\n")
        except:
            frame.insert(END, "Disconnected\n")
            break

s = socket.socket()
s.connect(('nozomi.proxy.rlwy.net', 36730))

myScreen = Tk()
myScreen.title("Client Server")
myScreen.geometry("400x500")  
myScreen.configure(bg="#1e1e2e")  

frame = Text(myScreen, bg="#2a2a3d", fg="white")
frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

entry = Entry(myScreen, bg="#2a2a3d", fg="white",font=16)
entry.pack(fill=X, padx=10, pady=10)

btn = Button(myScreen, text="Send", bg="#7d2252", fg="white",command=send)
btn.pack(padx=10, pady=(0, 10), fill=X)

entry.bind("<Return>", lambda e: send())

threading.Thread(target=receive, daemon=True).start()

myScreen.mainloop()