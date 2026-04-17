from customtkinter import *
import socket
from threading import Thread

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("mainline.proxy.rlwy.net", 45447))

home = CTk(fg_color="#7d2252")
home.geometry('300x400')

chatarea = CTkTextbox(home, width=280, height=300)
chatarea.pack(pady=10)

entry = CTkEntry(home, width=280)
entry.pack(pady=5)

def sendmsg():
    msg = entry.get()
    if msg:
        client_socket.sendall(msg.encode())
        chatarea.insert("end", "Me: " + msg + "\n")
        chatarea.see("end")
        entry.delete(0, "end")

sendbtn = CTkButton(home, text="Send", command=sendmsg)
sendbtn.pack(pady=5)

def receivemsg():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data:
                home.after(0, lambda d=data: (
                    chatarea.insert("end", "Other: " + d + "\n"),
                    chatarea.see("end")
                ))
        except:
            break

Thread(target=receivemsg, daemon=True).start()

home.mainloop()