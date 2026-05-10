"""
import socket
import threading

clients = []

def handle(conn):
    while True:
        try:
            msg = conn.recv(1024)
            if not msg:
                break
            for c in clients:
                if c != conn:
                    c.send(msg)
        except:
            break
    clients.remove(conn)
    conn.close()

server = socket.socket()
server.bind(('0.0.0.0', 8068))
server.listen(5)
print("Server running...")

while True:
    conn, addr = server.accept()
    clients.append(conn)
    print(f"Connected: {addr}")
    threading.Thread(target=handle, args=(conn,), daemon=True).start()
"""
import socket, threading, os, io
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
from PIL import Image

END_MARKER = b"<END>"
HD = False


def add(msg):
    chat.insert("end", msg + "\n")
    chat.see("end")


def send():
    msg = entry.get()
    if msg:
        s.send(msg.encode())
        add("eslam: " + msg)
        entry.delete(0, END)


def toggle():
    global HD
    HD = not HD
    hd.config(text="HD ON" if HD else "HD OFF")


def send_img():
    path = filedialog.askopenfilename(
        filetypes=[("Images", "*.jpg *.png *.jpeg")]
    )
    if not path:
        return

    img = Image.open(path)
    data = io.BytesIO()

    img.save(data, format="JPEG", quality=100 if HD else 25)

    s.send(f"IMAGE|{os.path.basename(path)}|".encode())

    d = data.getvalue()

    total = len(d)

    for i in range(0, total, 1024):
        s.send(d[i:i+1024])
        bar['value'] = (i / total) * 100
        root.update()

    s.send(END_MARKER)

    bar['value'] = 0
    add("Image Sent")


def send_file():
    path = filedialog.askopenfilename()
    if not path:
        return

    ext = os.path.splitext(path)[1]
    t = "VIDEO" if ext in [".mp4", ".avi", ".mov"] else "FILE"

    s.send(f"{t}|{os.path.basename(path)}|".encode())

    with open(path, "rb") as f:
        while True:
            x = f.read(1024)
            if not x:
                break
            s.send(x)

    s.send(END_MARKER)
    add(f"{t} Sent")


def receive():
    while True:
        try:
            data = s.recv(1024)

            if not data:
                continue

            if data.startswith(b"IMAGE|") or data.startswith(b"FILE|") or data.startswith(b"VIDEO|"):

                info = data.decode().split("|")
                name = "received_" + info[1]

                file = b""

                while True:
                    x = s.recv(1024)
                    if END_MARKER in x:
                        file += x.replace(END_MARKER, b"")
                        break
                    file += x

                open(name, "wb").write(file)
                add(info[0] + " Received")

            else:
                add("fares: " + data.decode())

        except:
            break


# الاتصال بالسيرفر
s = socket.socket()
s.connect(('nozomi.proxy.rlwy.net', 36730))

# UI
root = Tk()
root.geometry("400x600")
root.configure(bg="#1e1e2e")

chat = Text(root, bg="#2a2a3d", fg="white")
chat.pack(fill=BOTH, expand=True, padx=10, pady=10)

entry = Entry(root, bg="#2a2a3d", fg="white")
entry.pack(fill=X, padx=10, pady=5)

Button(root, text="Send", command=send, bg="#7d2252", fg="white").pack(fill=X, padx=10, pady=3)
Button(root, text="Image", command=send_img, bg="#22577a", fg="white").pack(fill=X, padx=10, pady=3)
Button(root, text="File/Video", command=send_file, bg="#386641", fg="white").pack(fill=X, padx=10, pady=3)

hd = Button(root, text="HD OFF", command=toggle)
hd.pack(fill=X, padx=10, pady=3)

bar = Progressbar(root, orient=HORIZONTAL, mode="determinate")
bar.pack(fill=X, padx=10, pady=10)

entry.bind("<Return>", lambda e: send())

threading.Thread(target=receive, daemon=True).start()

root.mainloop()