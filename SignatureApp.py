import tkinter as tk
from tkinter import filedialog
from PDFFile import PDFFile

class SignatureApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.file = PDFFile(None, None)
        self.AES_key_pin = 0

        # Początek programu
        self.create_main_window()

    def choose_pdf(self, info):
        chosen_file = filedialog.askopenfilename(
            title="Choose PDF file",
            filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
        )
        if chosen_file is not None:
            self.file.setFile(chosen_file)
            info.set(self.file.getName())

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

        root.mainloop()

    def create_main_window(self):
        root = self
        root.title("BSK project")
        root.geometry("300x300")
        root.configure(bg="#bcbfdc")

        info = tk.StringVar()
        info.set("No file chosen")

        button_choose_pdf = tk.Button(
            root,
            text="Choose pdf file",
            command=lambda: self.choose_pdf(info),
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

        label = tk.Label(root, textvariable=info, bg="#bcbfdc", fg="black")
        label.pack(pady=(20, 0))


app = SignatureApp()
app.mainloop()