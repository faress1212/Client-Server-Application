import socket
import threading
from tkinter import *

def send():
    msg = entry.get()
    if msg:
        s.send(msg.encode())
        chat.insert(END, "me: " + msg + "\n")
        entry.delete(0, END)

def receive():
    while True:
        try:
            msg = s.recv(1024).decode()
            if msg:
                chat.insert(END, "other: " + msg + "\n")
        except:
            chat.insert(END, "انقطع الاتصال\n")
            break

s = socket.socket()
s.connect(('nozomi.proxy.rlwy.net', 36730))

root = Tk()
root.title("Chat")
root.configure(bg="#1e1e2e")

chat = Text(root, bg="#2a2a3d", fg="#cdd6f4", insertbackground="white",
            font=("Segoe UI", 11), bd=0, padx=10, pady=10)
chat.pack(fill=BOTH, expand=True, padx=10, pady=10)

frame = Frame(root, bg="#1e1e2e")
frame.pack(fill=X, padx=10, pady=(0, 10))

entry = Entry(frame, bg="#2a2a3d", fg="#cdd6f4", insertbackground="white",
              font=("Segoe UI", 11), bd=0, relief=FLAT)
entry.pack(side=LEFT, fill=X, expand=True, ipady=8, padx=(0, 8))
entry.bind("<Return>", lambda e: send())

Button(frame, text="Send", bg="#7d2252", fg="white",
       activebackground="#a33370", activeforeground="white",
       font=("Segoe UI", 11), bd=0, relief=FLAT,
       padx=16, pady=8, cursor="hand2", command=send).pack(side=LEFT)

threading.Thread(target=receive, name="receive", daemon=True).start()
root.mainloop()