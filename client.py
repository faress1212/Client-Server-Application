import socket
import threading
import struct
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
import io
from PIL import Image
import os


def send_packet(sock, data):
    sock.sendall(struct.pack("!I", len(data)) + data)


def recvall(sock, n):
    data = b""
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


def add(msg):
    chat.insert("end", msg + "\n")
    chat.see("end")


def send():
    msg = entry.get()
    if msg:
        send_packet(s, f"TEXT|eslam|{msg}".encode())
        add("me: " + msg)
        entry.delete(0, END)


def send_img():
    path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")])
    if not path:
        return

    img = Image.open(path)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=80)

    data = buf.getvalue()

    payload = f"IMG|eslam|{os.path.basename(path)}|".encode() + data
    send_packet(s, payload)

    add("Image sent")


def send_file():
    path = filedialog.askopenfilename()
    if not path:
        return

    ext = os.path.splitext(path)[1]
    t = "VIDEO" if ext in [".mp4", ".avi", ".mov"] else "FILE"

    with open(path, "rb") as f:
        file_data = f.read()

    payload = f"{t}|eslam|{os.path.basename(path)}|".encode() + file_data
    send_packet(s, payload)

    add(t + " sent")


def receive():
    while True:
        try:
            raw_len = recvall(s, 4)
            if not raw_len:
                continue

            length = struct.unpack("!I", raw_len)[0]
            data = recvall(s, length)

            if not data:
                continue

            # TEXT
            if data.startswith(b"TEXT|"):
                _, user, msg = data.decode().split("|", 2)
                add(f"{user}: {msg}")

            # IMAGE / FILE
            elif data.startswith(b"IMG|") or data.startswith(b"FILE|") or data.startswith(b"VIDEO|"):
                header, user, name, filedata = data.split(b"|", 3)

                filename = "recv_" + name.decode()
                with open(filename, "wb") as f:
                    f.write(filedata)

                add(f"{header.decode()} received from {user.decode()}")

        except:
            break


# الاتصال
s = socket.socket()
s.connect(("nozomi.proxy.rlwy.net", 36730))


# UI
root = Tk()
root.geometry("400x600")

chat = Text(root)
chat.pack(fill=BOTH, expand=True)

entry = Entry(root)
entry.pack(fill=X)

Button(root, text="Send", command=send).pack(fill=X)
Button(root, text="Image", command=send_img).pack(fill=X)
Button(root, text="File", command=send_file).pack(fill=X)

threading.Thread(target=receive, daemon=True).start()

root.mainloop()