import tkinter as tk
import socket
import threading

class ClientGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")

        self.server_label = tk.Label(self.master, text="Server IP: ")
        self.server_label.grid(row=0, column=0)

        self.server_entry = tk.Entry(self.master)
        self.server_entry.grid(row=0, column=1)

        self.port_label = tk.Label(self.master, text="Server Port: ")
        self.port_label.grid(row=1, column=0)

        self.port_entry = tk.Entry(self.master)
        self.port_entry.grid(row=1, column=1)

        self.username_label = tk.Label(self.master, text="Username: ")
        self.username_label.grid(row=2, column=0)

        self.username_entry = tk.Entry(self.master)
        self.username_entry.grid(row=2, column=1)

        self.recipient_label = tk.Label(self.master, text="Recipient: ")
        self.recipient_label.grid(row=3, column=0)

        self.recipient_entry = tk.Entry(self.master)
        self.recipient_entry.grid(row=3, column=1)

        self.connect_button = tk.Button(self.master, text="Connect", command=self.connect)
        self.connect_button.grid(row=4, column=0, columnspan=2)

        self.chat_text = tk.Text(self.master)
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.grid(row=5, column=0, columnspan=2)

        self.message_entry = tk.Entry(self.master)
        self.message_entry.grid(row=6, column=0)

        self.recipient_entry = tk.Entry(self.master)
        self.recipient_entry.grid(row=6, column=1)

        self.send_button = tk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.grid(row=7, column=0, columnspan=2)

        self.client_socket = None
        self.receive_thread = None

    def connect(self):
        server = self.server_entry.get()
        port = int(self.port_entry.get())
        username = self.username_entry.get()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server, port))
        self.client_socket.send(username.encode())

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()
        
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                self.chat_text.config(state=tk.NORMAL)
                self.chat_text.insert(tk.END, message + "\n")
                self.chat_text.config(state=tk.DISABLED)
                self.chat_text.see(tk.END) # Scroll to the end of the chat box
            except:
                self.client_socket.close()
                break


    def send_message(self):
        message = self.message_entry.get()
        recipient = self.recipient_entry.get()
        username = self.username_entry.get()
        if recipient:
            message = f"@{recipient} {message}"
            # Add a prefix to indicate that this is a private message
            message = f"PRIVATE {message}"
        else:
            message = f"{username}: {message}"
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, "You: " + message + "\n")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END) # Scroll to the end of the chat box
        self.client_socket.send(message.encode())
        self.message_entry.delete(0, tk.END)
        self.recipient_entry.delete(0, tk.END)


        
root = tk.Tk()
client_gui = ClientGUI(root)
root.mainloop()
