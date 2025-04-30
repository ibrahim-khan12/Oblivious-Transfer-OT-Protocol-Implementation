# # import socket
# # import json
# # from ot_protocol import OTSender

# # class OTServer:
# #     def __init__(self, host='localhost', port=65432):
# #         self.host = host
# #         self.port = port
# #         self.sender = OTSender()
# #         self.messages = ("", "")
    
# #     def set_messages(self, m0, m1):
# #         self.messages = (m0, m1)
    
# #     def start(self):
# #         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# #             s.bind((self.host, self.port))
# #             s.listen()
# #             print(f"OT Server listening on {self.host}:{self.port}")
            
# #             while True:
# #                 conn, addr = s.accept()
# #                 with conn:
# #                     print(f"Connected by {addr}")
                    
# #                     # Send public key
# #                     conn.sendall(json.dumps({
# #                         'public_key': self.sender.public_key
# #                     }).encode())
                    
# #                     # Receive receiver's public keys
# #                     data = conn.recv(4096)
# #                     pk_data = json.loads(data.decode())
                    
# #                     # Encrypt and send messages
# #                     ciphertexts = self.sender.encrypt_messages(
# #                         pk_data['pk0'], pk_data['pk1'],
# #                         self.messages[0], self.messages[1]
# #                     )
# #                     conn.sendall(ciphertexts.encode())

# # if __name__ == "__main__":
# #     server = OTServer()
# #     m0 = input("Enter first message: ")
# #     m1 = input("Enter second message: ")
# #     server.set_messages(m0, m1)
# #     print("Server started with your messages. Waiting for receiver...")
# #     server.start()


# import socket
# import json
# from ot_protocol import NaorPinkasSender

# class OTService:
#     def __init__(self, host='localhost', port=65432):
#         self.host = host
#         self.port = port
#         self.sender = NaorPinkasSender()
#         self.messages = None
    
#     def start_server(self):
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.bind((self.host, self.port))
#             s.listen()
#             print(f"OT Server listening on {self.host}:{self.port}")
            
#             while True:
#                 conn, addr = s.accept()
#                 with conn:
#                     print(f"Connected to {addr}")
#                     self._handle_connection(conn)
    
#     def _handle_connection(self, conn):
#         # Send public key
#         conn.sendall(json.dumps({
#             'public_key': self.sender.public_key
#         }).encode())
        
#         # Receive receiver's public keys
#         pk_data = json.loads(conn.recv(4096).decode())
        
#         # Encrypt and send messages
#         encrypted = self.sender.encrypt_messages(
#             pk_data['pk0'], pk_data['pk1'],
#             self.messages[0], self.messages[1]
#         )
#         conn.sendall(json.dumps(encrypted).encode())

# if __name__ == "__main__":
#     service = OTService()
#     service.messages = [
#         input("Enter first message: "),
#         input("Enter second message: ")
#     ]
#     print("Starting OT service with your messages...")
#     service.start_server()










import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import socket
import json
from threading import Thread
from datetime import datetime
from ot_protocol import NaorPinkasSender

class SecureMessengerServer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Secure Message Server")
        self.window.geometry("800x600")
        self.configure_styles()
        
        self.sender = NaorPinkasSender()
        self.server_running = False
        self.clients = []
        
        self.create_widgets()
        self.setup_server()
    
    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 10), padding=6)
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TEntry', font=('Helvetica', 10))
        style.configure('Status.TLabel', foreground='white', background='#4CAF50')
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.window)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Message Input Section
        input_frame = ttk.LabelFrame(main_frame, text=" Secret Messages ")
        input_frame.pack(fill=tk.X, pady=10)
        
        self.message0 = self.create_message_input(input_frame, "Message Option 0:", 0)
        self.message1 = self.create_message_input(input_frame, "Message Option 1:", 1)
        
        # Server Controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        self.start_btn = ttk.Button(control_frame, text="Start Secure Server", 
                                   command=self.toggle_server, style='Accent.TButton')
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(control_frame, text=" Status: Offline ", 
                                    style='Status.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Activity Log
        log_frame = ttk.LabelFrame(main_frame, text=" Security Log ")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state='disabled',
                                           font=('Consolas', 9))
        self.log.pack(fill=tk.BOTH, expand=True)
    
    def create_message_input(self, parent, label, idx):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        
        lbl = ttk.Label(frame, text=label, width=15)
        lbl.pack(side=tk.LEFT)
        
        entry = ttk.Entry(frame, width=50)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        char_count = ttk.Label(frame, text="0/256", width=6)
        char_count.pack(side=tk.RIGHT)
        
        entry.bind('<KeyRelease>', lambda e, cc=char_count: 
            cc.config(text=f"{len(e.widget.get())}/256"))
        return entry
    
    def setup_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def toggle_server(self):
        if not self.server_running:
            if not self.validate_messages():
                return
            Thread(target=self.run_server, daemon=True).start()
            self.start_btn.config(text="Stop Secure Server")
            self.status_label.config(text=" Status: Online ", style='Online.Status.TLabel')
            self.log_message("Server started", "system")
            self.server_running = True
        else:
            self.server_running = False
            self.server_socket.close()
            self.start_btn.config(text="Start Secure Server")
            self.status_label.config(text=" Status: Offline ", style='Status.TLabel')
            self.log_message("Server stopped", "system")
    
    def validate_messages(self):
        if len(self.message0.get()) < 1 or len(self.message1.get()) < 1:
            messagebox.showerror("Validation Error", "Both messages must be provided!")
            return False
        if len(self.message0.get()) > 256 or len(self.message1.get()) > 256:
            messagebox.showerror("Validation Error", "Messages cannot exceed 256 characters!")
            return False
        return True
    
    def run_server(self):
        self.server_socket.bind(('localhost', 65432))
        self.server_socket.listen(5)
        
        while self.server_running:
            try:
                conn, addr = self.server_socket.accept()
                self.clients.append(conn)
                self.log_message(f"New connection from {addr[0]}", "connection")
                Thread(target=self.handle_client, args=(conn,), daemon=True).start()
            except:
                break
    
    def handle_client(self, conn):
        try:
            # Send public key
            conn.send(json.dumps({'public_key': self.sender.public_key}).encode())
            
            # Receive receiver's public keys
            pks = json.loads(conn.recv(4096).decode())
            
            # Encrypt messages
            encrypted = self.sender.encrypt_messages(
                pks['pk0'], pks['pk1'],
                self.message0.get(), self.message1.get()
            )
            
            conn.send(json.dumps(encrypted).encode())
            self.log_message("Messages securely delivered", "transfer")
            
        except Exception as e:
            self.log_message(f"Error: {str(e)}", "error")
        finally:
            conn.close()
    
    def log_message(self, text, msg_type):
        timestamp = datetime.now().strftime("%H:%M:%S")
        tag = ""
        if msg_type == "error":
            tag = "error"
            text = f"[ERROR] {text}"
        elif msg_type == "connection":
            tag = "connection"
            text = f"[CONNECT] {text}"
        elif msg_type == "transfer":
            tag = "transfer"
            text = f"[TRANSFER] {text}"
        
        self.log.config(state='normal')
        self.log.insert(tk.END, f"[{timestamp}] {text}\n", tag)
        self.log.config(state='disabled')
        self.log.see(tk.END)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = SecureMessengerServer()
    app.run()