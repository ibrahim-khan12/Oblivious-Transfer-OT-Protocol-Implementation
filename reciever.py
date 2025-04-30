# # import socket
# # import json
# # from ot_protocol import OTReceiver

# # class OTClient:
# #     def __init__(self, host='localhost', port=65432):
# #         self.host = host
# #         self.port = port
# #         self.receiver = OTReceiver()
# #         self.sender_pubkey = None
    
# #     def retrieve_message(self, choice):
# #         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# #             s.connect((self.host, self.port))
            
# #             # Get sender's public key
# #             pubkey_data = json.loads(s.recv(4096).decode())
# #             self.sender_pubkey = pubkey_data['public_key']
            
# #             # Generate and send receiver's public keys
# #             pk_payload = self.receiver.generate_pk(self.sender_pubkey, choice)
# #             s.sendall(pk_payload.encode())
            
# #             # Receive ciphertexts
# #             cipher_data = json.loads(s.recv(4096).decode())
# #             chosen = 'c0' if choice == 0 else 'c1'
# #             return self.receiver.decrypt_message(
# #                 self.sender_pubkey,
# #                 cipher_data[chosen]
# #             )

# # if __name__ == "__main__":
# #     client = OTClient()
# #     choice = int(input("Enter choice (0 or 1): "))
# #     message = client.retrieve_message(choice)
# #     print(f"\nReceived message: {message}")

# import socket
# import json

# class OTClient:
#     def __init__(self, host='localhost', port=65432):
#         self.host = host
#         self.port = port
    
#     def retrieve_message(self, choice):
#         from ot_protocol import NaorPinkasReceiver
        
#         receiver = NaorPinkasReceiver(choice)
        
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.connect((self.host, self.port))
            
#             # Get sender's public key
#             pubkey_data = json.loads(s.recv(4096))
#             sender_pubkey = pubkey_data['public_key']
            
#             # Generate and send public keys
#             pks = receiver.generate_public_keys(sender_pubkey)
#             s.sendall(json.dumps(pks).encode())
            
#             # Receive ciphertexts
#             encrypted = json.loads(s.recv(4096).decode())
#             ciphertext = encrypted['ciphertexts'][choice]
            
#             return receiver.decrypt_message(sender_pubkey, ciphertext)

# if __name__ == "__main__":
#     client = OTClient()
#     choice = int(input("Enter choice (0 or 1): "))
#     message = client.retrieve_message(choice)
#     print(f"\nReceived message: {message}")




















import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import socket
import json
from threading import Thread
from datetime import datetime
from ot_protocol import NaorPinkasReceiver

class SecureMessengerClient:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Secure Message Client")
        self.window.geometry("600x500")
        self.configure_styles()
        
        self.connected = False
        self.create_widgets()
    
    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 10), padding=6)
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('Encrypted.TLabel', foreground='#4CAF50')
        style.configure('Decrypted.TLabel', foreground='#2196F3')
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.window)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Connection Panel
        conn_frame = ttk.LabelFrame(main_frame, text=" Secure Connection ")
        conn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(conn_frame, text="Server IP:").grid(row=0, column=0, padx=5)
        self.ip_entry = ttk.Entry(conn_frame, width=20)
        self.ip_entry.grid(row=0, column=1, padx=5)
        self.ip_entry.insert(0, "localhost")
        
        ttk.Label(conn_frame, text="Select Message:").grid(row=0, column=2, padx=5)
        self.choice_entry = ttk.Combobox(conn_frame, values=["0", "1"], width=3)
        self.choice_entry.grid(row=0, column=3, padx=5)
        self.choice_entry.current(0)
        
        self.connect_btn = ttk.Button(conn_frame, text="Retrieve Secure Message", 
                                    command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=4, padx=10)
        
        # Security Indicators
        self.status_label = ttk.Label(conn_frame, text="Not Connected", style='Encrypted.TLabel')
        self.status_label.grid(row=1, columnspan=5, pady=5)
        
        # Message Display
        msg_frame = ttk.LabelFrame(main_frame, text=" Decrypted Message ")
        msg_frame.pack(fill=tk.BOTH, expand=True)
        
        self.message_display = scrolledtext.ScrolledText(msg_frame, wrap=tk.WORD, 
                                                       state='disabled', font=('Helvetica', 11))
        self.message_display.pack(fill=tk.BOTH, expand=True)
        
        # Footer
        footer = ttk.Frame(main_frame)
        footer.pack(fill=tk.X, pady=10)
        
        self.connection_status = ttk.Label(footer, text="Security Protocol: OT-1/2 (Naor-Pinkas)")
        self.connection_status.pack(side=tk.LEFT)
        
        ttk.Label(footer, text="Encryption: AES-256-GCM").pack(side=tk.RIGHT)
    
    def toggle_connection(self):
        if not self.connected:
            choice = self.choice_entry.get()
            if not choice.isdigit() or int(choice) not in [0, 1]:
                messagebox.showerror("Error", "Invalid selection! Choose 0 or 1")
                return
            
            Thread(target=self.retrieve_message, args=(int(choice),), daemon=True).start()
            self.connect_btn.config(state='disabled')
            self.status_label.config(text="Establishing Secure Connection...")
        else:
            self.connected = False
            self.connect_btn.config(text="Retrieve Secure Message")
            self.status_label.config(text="Connection Closed")
    
    def retrieve_message(self, choice):
        try:
            receiver = NaorPinkasReceiver(choice)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.ip_entry.get(), 65432))
                self.connected = True
                self.update_ui("Connected to Server", "#4CAF50")
                
                # Get public key
                pubkey = json.loads(s.recv(4096))['public_key']
                
                # Send generated PKs
                pks = receiver.generate_public_keys(pubkey)
                s.send(json.dumps(pks).encode())
                
                # Receive encrypted messages
                encrypted = json.loads(s.recv(4096).decode())
                
                # Decrypt chosen message
                ciphertext = encrypted['ciphertexts'][choice]
                decrypted = receiver.decrypt_message(pubkey, ciphertext)
                
                self.display_message(decrypted)
                self.update_ui("Message Securely Received", "#4CAF50")
        
        except Exception as e:
            self.update_ui(f"Error: {str(e)}", "#F44336")
            messagebox.showerror("Connection Error", str(e))
        finally:
            self.connect_btn.config(state='normal')
            self.connected = False
    
    def display_message(self, message):
        self.message_display.config(state='normal')
        self.message_display.delete(1.0, tk.END)
        self.message_display.insert(tk.END, f"Secure Message:\n\n{message}")
        self.message_display.config(state='disabled')
    
    def update_ui(self, text, color):
        self.status_label.config(text=text, foreground=color)
        self.window.update()
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = SecureMessengerClient()
    app.run()