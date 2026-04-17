from customtkinter import *
import socket
from threading import Thread

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# منع الكونكشن من الانقطاع
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 30)   # ابدأ بعد 30 ثانية
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)  # كل 10 ثواني
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)     # 5 محاولات

client_socket.connect(("monorail.proxy.rlwy.net", 59181))

home = CTk(fg_color="#7d2252")
home.geometry('300x400')

chatarea = CTkTextbox(home, width=280, height=300)
chatarea.pack(pady=10)

entry = CTkEntry(home, width=280)
entry.pack(pady=5)

connected = True  # متغير لحالة الكونكشن

def sendmsg(event=None):
    if not connected:
        chatarea.insert("end", "⚠ انت مش متصل!\n")
        return
    msg = entry.get()
    if msg:
        try:
            client_socket.sendall(msg.encode())
            chatarea.insert("end", "Me: " + msg + "\n")
            chatarea.see("end")
            entry.delete(0, "end")
        except:
            chatarea.insert("end", "⚠ فشل الإرسال!\n")

sendbtn = CTkButton(home, text="Send", command=sendmsg)
sendbtn.pack(pady=5)

entry.bind("<Return>", sendmsg)

def receivemsg():
    global connected
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data:
                home.after(0, lambda d=data: (
                    chatarea.insert("end", "Other: " + d + "\n"),
                    chatarea.see("end")
                ))
        except:
            connected = False
            home.after(0, lambda: chatarea.insert("end", "⚠ انقطع الاتصال!\n"))
            break

Thread(target=receivemsg, daemon=True).start()

home.mainloop()

