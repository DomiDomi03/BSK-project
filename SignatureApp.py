import tkinter as tk
from tkinter import filedialog
from PDFFile import PDFFile
import psutil
import declarations as ds
import os

class SignatureApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.AES_key_pin = 0

        self.file = PDFFile(None, None)
        self.file_state_info = tk.StringVar()
        self.file_state_info.set("No file chosen")
        self.file_label = tk.Label(self, textvariable=self.file_state_info, bg="red", fg="black")

        self.pendrive_connected = False
        self.pendrive_state_info = tk.StringVar()
        self.pendrive_state_info.set("No pendrive detected")
        self.pendrive_label = tk.Label(self, textvariable=self.pendrive_state_info, bg="red", fg="black")

        # Początek programu
        self.create_main_window()

    def choose_pdf(self):
        chosen_file = filedialog.askopenfilename(
            title="Choose PDF file",
            filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
        )
        self.file.setFile(chosen_file)
        self.check_file()

    def check_file(self):
        if self.file.is_chosen():
            self.file_state_info.set(self.file.getName())
            self.file_label.configure(bg="#bcbfdc")
            self.configure(bg="#bcbfdc")

    def pin(self, pin_entry, root):
        self.AES_key_pin = pin_entry.get()  # Przekazujemy wprowadzone dane
        print(self.AES_key_pin)
        root.destroy()  # zamknięcie okna

    def sign_pdf(self):
        root = tk.Toplevel(self)
        root.title("Create PIN")
        root.geometry("400x200")
        root.configure(bg="#bcbfdc")

        title_label = tk.Label(root, text="Please enter PIN to decrypt the private key:", bg="#bcbfdc")
        title_label.pack(pady=20)

        # Pole do wprowadzania PIN-u z maskowaniem znaków
        pin_entry = tk.Entry(root, show="*", width=15)
        pin_entry.pack(pady=10)

        # przycisk do zatwierdzenia PIN-u
        verify_button = tk.Button(root, text="OK", command=lambda: self.pin(pin_entry, root))
        verify_button.pack(pady=10)

        usb_path = self.find_usb()
        full_path = os.path.join(list(usb_path)[0], ds.file_name)

        # odczytanie klucza prywatnego zaszyfrowanego w AES
        if os.path.exists(full_path) and os.path.isfile(full_path):
            try:
                with open(full_path, 'rb') as file:
                    content = file.read()  # Odczytujemy zawartość binarną
                    content = content.decode("latin1")  # koduje na odpowiedni format

                # Szukamy prywatnego klucza
                start_marker = "Decrypted private key:"
                end_marker = "Public key:"
                if start_marker in content:
                    start_index = content.index(start_marker)  # Znajdź początek
                    content_after_marker = content[start_index + len(start_marker) + 1:]
                    # decrypted_key = content[start_index+len(start_marker)+1:]
                    # print(decrypted_key)
                    end_index = content_after_marker.find(end_marker)

                    if end_index != -1:
                        decrypted_key_full = content_after_marker[:end_index]  # .strip() - usuwa białe znaki
                    print(decrypted_key_full)


            except FileNotFoundError:
                print("File not found!")

    def create_buttons(self, root):
        button_choose_pdf = tk.Button(
            root,
            text="Choose pdf file",
            command=lambda: self.choose_pdf(),
            fg="black",
            bg="white",
            relief="flat"
        )
        button_choose_pdf.pack(pady=(120, 0))

        button_signature = tk.Button(
            root,
            text="Signature pdf file",
            command=lambda: self.sign_pdf(),
            fg="black",
            bg="white",
            relief="flat"
        )
        button_signature.pack(pady=(10, 0))

        button_verify = tk.Button(
            root,
            text="Verify signature",
            # command=,
            fg="black",
            bg="white",
            relief="flat"
        )
        button_verify.pack(pady=(10, 0))

    def create_main_window(self):
        root = self
        root.title("Signature App")
        root.geometry("300x300")
        root.configure(bg="red")

        # Wyświetlanie stanu pendrive'a
        self.pendrive_label.pack(pady=(20, 0))

        # Wyświetlanie stanu pliku
        self.file_label.pack(pady=(10, 0))

        self.check_pendrive()

    def check_pendrive(self):
        pendrives = self.find_usb()

        if pendrives and not self.pendrive_connected:
            self.pendrive_connected = True
            self.pendrive_state_info.set("Pendrive detected!")
            self.pendrive_label.configure(bg="#bcbfdc")

            self.create_buttons(self)

        elif not pendrives and self.pendrive_connected:
            self.pendrive_connected = False
            self.pendrive_state_info.set("No pendrive detected")
            self.pendrive_label.configure(bg="#ff0000")
            self.file_state_info.set("No file chosen")
            self.file_label.configure(bg="#ff0000")

            self.remove_buttons()

        self.after(500, lambda: self.check_pendrive())

    @staticmethod
    def find_usb():
        return {p.device for p in psutil.disk_partitions() if 'removable' in p.opts.lower()}

    def remove_buttons(self):
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

app = SignatureApp()
app.mainloop()