import tkinter as tk
import psutil
import declarations as ds
import RSA_keys as rsa
import AES as aes
import tkinter.ttk as ttk
import threading

class GenerateKeysApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.encrypted_private_key = None
        self.public_key = None
        self.user_pin = None
        self.iv = None

        self.save_location = tk.StringVar(self)

        self.status_label = tk.Label(self, text="", bg="#bcbfdc")
        self.status_label.pack(pady=5)
        self.progress = ttk.Progressbar(self, mode="determinate", maximum=100)

        self.create_main_window()

    def create_main_window(self):
        root = self
        root.title("Generate keys App")
        root.geometry("300x300")
        root.configure(bg="#bcbfdc")

        devices_list = list(self.find_devices())
        self.save_location.set(devices_list[0])  # default

        file_location_frame = tk.Frame(root, bg="#bcbfdc")
        file_location_frame.pack(pady=10, anchor="center")

        file_location_label = tk.Label(file_location_frame, text="Save location: ", bg="#bcbfdc")
        file_location_label.pack(side="left", padx=10)

        file_location_dropdown = tk.OptionMenu(file_location_frame, self.save_location, *devices_list)
        file_location_dropdown.pack(side="left")

        title_label = tk.Label(root, text="Please enter PIN to encrypt the private key:", bg="#bcbfdc")
        title_label.pack(pady=20)

        pin_entry = tk.Entry(root, show="*", width=15)
        pin_entry.pack(pady=10)

        verify_button = tk.Button(root, text="Generate", command=lambda: self.save_pin(pin_entry))
        verify_button.pack(pady=10)

    def save_pin(self, new_pin):
        self.user_pin = new_pin.get()
        print("Pin " + self.user_pin + " saved")

        if self.user_pin is not None:
            self.status_label.config(text="Generating keys...")
            self.progress['value'] = 0
            self.progress.pack(pady=5)
            threading.Thread(target=self.run_generation_process()).start()

    def run_generation_process(self):
        self.after(0, lambda: self.progress.step(0))
        private_key = rsa.create_private_key()

        self.after(1000, lambda: self.progress.step(20))
        self.public_key = rsa.create_public_key(private_key)

        self.after(2000, lambda: self.progress.step(20))
        private_key_bytes = rsa.convert_PEM_private(private_key)

        self.iv, self.encrypted_private_key = aes.encrypt_aes(self.user_pin, private_key_bytes)

        self.after(3000, lambda: self.progress.step(20))
        self.after(4000, lambda: self.status_label.config(text="Saving to file..."))
        self.save_to_file()

        self.after(5000, lambda: self.progress.step(20))
        self.after(6000, self.on_generation_complete)

    def on_generation_complete(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.status_label.config(text="Keys generated and saved successfully!")

    def save_to_file(self):
        with open(ds.file_name, "wb") as f:
            f.write(b"Decrypted private key: ")
            f.write(self.encrypted_private_key) # bytes
            f.write(b"\n\nPublic key: ")
            PEM_public_key = rsa.convert_PEM_public(self.public_key)
            f.write(PEM_public_key)  # bytes(PEM) Zapiszemy klucz publiczny w formacie PEM
            f.write(b"\nUser_pin: ")
            f.write(str(self.user_pin).encode())  # bytes Zapiszemy PIN w formie bajtów
            f.write(b"\niv: ")
            f.write(self.iv) # bytes

    @staticmethod
    def find_devices():
        return {p.device for p in psutil.disk_partitions()}

    @staticmethod
    def find_usb():
        return {p.device for p in psutil.disk_partitions() if 'removable' in p.opts.lower()}


app = GenerateKeysApp()
app.mainloop()