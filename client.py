import socket
import tkinter as tk
from tkinter import scrolledtext
import threading

def enviar():
    message = message_entry.get()
    client_socket.send(f"Cliente: {message}".encode())
    text_area.insert(tk.END, f"Vos: {message}\n")
    message_entry.delete(0, tk.END)
    if message.lower() == "chau":
        client_socket.close()
        window.quit()

def recibir():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            text_area.insert(tk.END, data + "\n")
            if data.lower() == "chau":
                client_socket.close()
                window.quit()
                break
        except ConnectionAbortedError:
            break
        except:
            print("Error al recibir mensajes.")
            break

    client_socket.close()
    text_area.insert(tk.END, "Conexión cerrada.\n")

def main():
    host = "127.0.0.1"  
    port = 12345       

    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    global window
    window = tk.Tk()
    window.title("Cliente")

    global text_area
    text_area = scrolledtext.ScrolledText(window)
    text_area.pack(padx=10, pady=10)

    global message_entry
    message_entry = tk.Entry(window, width=50)
    message_entry.pack(padx=10, pady=10)

    send_button = tk.Button(window, text="Enviar", command=enviar)
    send_button.pack(padx=10, pady=5)

    receive_thread = threading.Thread(target=recibir)
    receive_thread.start()

    window.mainloop()

if __name__ == "__main__":
    main()