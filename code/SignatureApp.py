##
#	@file SignatureApp.py
#	@details This application enables users to digitally sign PDF documents and verify the signatures. It checks the validity of the signatures according to the PAdES standard.
#	@date 25-05-2025
##

import hashlib
import tkinter as tk
from tkinter import filedialog
from PDFFile import PDFFile
import declarations as ds
import os
import hashlib as hash256
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import PyPDF2
import AES as aes
import functions as f
import time
from PyPDF2 import PdfReader

## A class that creates and verifies the signature of a PDF file
class SignatureApp(tk.Tk):
    # Constructor of the SignatureApp, start the application
    # @param AES_key_pin Stores the AES key PIN used for encryption (default 0).
    # @param mode Boolean flag for mode selection: True for signature creation, False for verification.
    # @param file Instance of PDFFile representing the current PDF file.
    # @param file_state_info A Tkinter StringVar holding the status message about the chosen file.
    # @param file_label Tkinter Label widget displaying the file status.
    # @param pendrive_connected Boolean flag indicating whether a pendrive is connected.
    # @param pendrive_state_info A Tkinter StringVar holding the pendrive connection status message.
    # @param pendrive_label Tkinter Label widget displaying pendrive status.
    # @param save_location  Tkinter StringVar representing the save location path.
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.AES_key_pin = 0
        self.mode = True # True - signature, False - verify

        self.file = PDFFile(None, None)
        self.file_state_info = tk.StringVar()
        self.file_state_info.set("No file chosen")
        self.file_label = tk.Label(self, textvariable=self.file_state_info, bg="red", fg="black")

        self.pendrive_connected = False
        self.pendrive_state_info = tk.StringVar()
        self.pendrive_state_info.set("No pendrive detected")
        self.pendrive_label = tk.Label(self, textvariable=self.pendrive_state_info, bg="red", fg="black")

        self.save_location = tk.StringVar(self)
        # Początek programu
        self.create_main_window()

    ## Method that creates main window of application
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

    ## Method that creates button using by application
    # @param root is a reference to main GUI window
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
            command=lambda: self.verify_pdf(),
            fg="black",
            bg="white",
            relief="flat"
        )
        button_verify.pack(pady=(10, 0))


    ## Method that deletes the buttons from the application
    def remove_buttons(self):
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

    ## Method that continuously monitors the presence of a USB pendrive.
    def check_pendrive(self):
        pendrives = f.find_usb()

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

    ## Method that checks if the file is a .pdf type
    def choose_pdf(self):
        chosen_file = filedialog.askopenfilename(
            title="Choose PDF file",
            filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
        )
        self.file.setFile(chosen_file)
        self.check_file()

    ## Method that that changes the style of the window when the file was choosen by the user
    def check_file(self):
        if self.file.is_chosen():
            self.file_state_info.set(self.file.getName())
            self.file_label.configure(bg="#bcbfdc")
            self.configure(bg="#bcbfdc")

    ## Method that adds signature to the .pdf file
    # @param pin_entry is the pin given by the user in order to decrypt the private key from the usb's file
    # @param root is a reference to main GUI window
    def pin(self, pin_entry, root):
        self.AES_key_pin = pin_entry.get()  # Przekazujemy wprowadzone dane
        print("pin: " + self.AES_key_pin)
        root.destroy()  # zamknięcie okna

        if self.AES_key_pin:
            decrypted_key_full = self.read_private_key_from_file()

            signature = self.create_signature(decrypted_key_full)

            # Odczytaj oryginalny plik PDF w bajtach
            with open(self.file.getPath(), "rb") as pdf_file:
                pdf_bytes = pdf_file.read()

            # Dopisz podpis jako komentarz na końcu pliku
            with open(self.file.getPath(), "wb") as signed_pdf:
                signed_pdf.write(pdf_bytes)
                signed_pdf.write(b"\n%SIGNATURE=" + signature.hex().encode() + b"\n")

            success_window = tk.Toplevel(self)
            success_window.title("Successfully added signature to PDF")
            success_window.geometry("300x100")
            success_window.configure(bg="green")
            success_label = tk.Label(success_window, text="Signature successfully added!", bg="green", font=("Arial", 14))
            success_label.pack(pady=20)


            success_window.after(2000, success_window.destroy)
            print("Podpis dodany do PDF")

    ## Method that generates the signature to the .pdf file
    def sign_pdf(self):
        self.mode = True

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

        usb_path = f.find_usb()
        full_path = os.path.join(list(usb_path)[0], ds.file_name)
        print(self.file.getName())


    ## Method that reads the signature from the .pdf file
    # @param path is the system path to the .pdf file with signature
    # @return signature in hex
    # @return None if the signature is not found
    def read_signature_from_pdf(self,path):
        with open(path, "rb") as f:
            lines = f.readlines()
        # Szukamy w pliku linii komentarza ze podpisem
        for line in reversed(lines):  # od końca, bo podpis na końcu pliku
            if line.startswith(b"%SIGNATURE="):
                signature_hex = line[len(b"%SIGNATURE="):].strip()
                return signature_hex.decode()  # zwracamy jako string hex
        return None  # jeśli nie znaleziono podpisu

    ## Method that deletes the signature from the .pdf file
    # @param input_path is the system path to the .pdf file with signature
    # @param output_path is the system path to the new .pdf file without the signature
    def remove_signature_from_pdf(self, input_path, output_path):
        with open(input_path, "rb") as f:
            lines = f.readlines()

        # Usuń linie z podpisem
        lines = [line for line in lines if not line.startswith(b"%SIGNATURE=")]

        # Jeśli ostatnia linia kończy się \n i nie chcemy pustej linii na końcu, usuń ten znak
        if lines and lines[-1].endswith(b"\n"):
            lines[-1] = lines[-1].rstrip(b"\n")

        with open(output_path, "wb") as f:
            f.writelines(lines)


    ## Method that verifies the signature in .pdf file
    # @throws message if verification of signature fails (either not foud or incorrect)
    # @return Null if public key is not found
    def verify_pdf(self):
        self.mode = False

        root = tk.Toplevel(self)
        root.geometry("400x200")
        root.configure(bg="#bcbfdc")

        result_label = tk.Label(root, text="Verifying...", bg="#bcbfdc", font=("Arial", 14))
        result_label.pack(pady=30)
        root.update()
        time.sleep(2)

        #hash_encrypted_file = self.get_encrypted_hash_from_pdf()
        public_key_bytes = self.read_private_key_from_file()

        if not public_key_bytes:
            print("Public key not found.")
            return

        public_key = serialization.load_pem_public_key(
            public_key_bytes,
            backend=default_backend()
        )

        print(public_key)

        """
        with open(self.file.getPath(), "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            signature_hex = reader.metadata.get("/Signature", "")
            if not signature_hex:
                print("Signature not found.")
                return
            signature = bytes.fromhex(signature_hex)
        """
        signature_hex = self.read_signature_from_pdf(self.file.getPath())
        if(signature_hex):
            signature = bytes.fromhex(signature_hex)
        else:
            print("Brak podpisu.")

        no_signature_file = "no_signature.pdf"
        self.remove_signature_from_pdf(self.file.getPath(), no_signature_file)
        generated_hash = self.hash_pdf(no_signature_file)
        os.remove(no_signature_file)

        # wersyfikacja podpisu
        try:
            public_key.verify(
                signature,
                generated_hash,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            print("Podpis prawidłowy")
            root.config(bg="#00ff00")
            result_label.config(bg="#00ff00")
            result_label.config(text="Verification completed successfully!")
            root.after(2000, root.destroy)
        except Exception as e:
            root.config(bg="#ff0000")
            result_label.config(bg="#ff0000")
            result_label.config(text="Signature verification failure!")
            root.after(2000, root.destroy)
            print("Błąd weryfikacji podpisu", e)


    ## Method that caretes signature
    # @param decrypted_key_full is a decrypted private key in PEM format
    # @return created PAdES signature
    def create_signature(self, decrypted_key_full):
        # tworzenie hashu pdfa
        pdf_path = self.file.getPath()
        hashed_pdf = self.hash_pdf(pdf_path)

        # odszyfrowanie klucza RSA

        #pem_data = decrypted_key_full  # klucz string (PEM)
        decrypted_key_full = serialization.load_pem_private_key(
            decrypted_key_full,
            password=None,  # klucz jest odszyfrownay
            backend=default_backend()
        )

        signature = decrypted_key_full.sign(
            hashed_pdf,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return signature


    ## Method that reads the public/priavte key from usb's file
    # @return None if file does not exist
    # @return decrypted key if user chose signature option
    # @return public key if user chose verify option
    # @throws FileNotFoundError if file is not found
    def read_private_key_from_file(self):
        usb_path = f.find_usb()
        full_path = os.path.join(list(usb_path)[0], ds.file_name)
        print(full_path)

        if not (os.path.exists(full_path) and os.path.exists(full_path)):
            print("File doesn't exist.")
            return None

        try:
            with open(full_path, 'rb') as file:
                content = file.read()  # Odczytujemy zawartość binarną

            start_marker = b"Decrypted private key: "  # Zakodowane na bajty
            end_marker = b"Public key: "
            start_marker_user_pin = b"User_pin: "
            start_marker_iv = b"iv: "

            if (self.mode):
                # czytanie prywatnego klucza
                if start_marker in content and end_marker in content:
                    start_index = content.index(start_marker)  # Znajdź początek
                    content_after_marker = content[start_index + len(start_marker):]  # Po markerze
                    end_index = content_after_marker.find(end_marker)

                    if end_index != -1:
                        read_key_private = content_after_marker[:end_index]  # Wyodrębniamy klucz prywatny
                        print(read_key_private)  # Debugowanie

                # czytanie iv
                if start_marker_iv in content:
                    iv_start_index = content.index(start_marker_iv)  # Znajdujemy początek IV
                    iv = content[iv_start_index + len(start_marker_iv):iv_start_index + len(start_marker_iv) + 16]  # Zakładając, że IV ma 16 bajtów
                    print(iv)
            else:
                # czytanie klucza publicznego
                if end_marker in content:
                    start_index = content.index(end_marker)  # Znajdź początek
                    content_after_marker = content[start_index + len(end_marker):]  # Po markerze
                    end_index = content_after_marker.find(start_marker_user_pin)

                    if end_index != -1:
                        read_key_public = content_after_marker[:end_index]  # Wyodrębniamy klucz prywatny
                        print(read_key_public)  # Debugowanie

        except FileNotFoundError:
            print("File not found!")

        if self.mode:
            decrypted_key = aes.decrypt_aes(read_key_private, iv, self.AES_key_pin)
            return decrypted_key
        else:
            return read_key_public


    ## Method that hashes the .pdf file
    # @param pdf_path is the system path to the .pdf file, where we want to add signature
    # @return hased pdf file
    def hash_pdf(self, pdf_path):
        sha256_hash = hash256.sha256()
        with open(pdf_path, "rb") as f:
            # Czytanie pliku porcjami, żeby nie zużywać dużo RAM-u
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.digest()


app = SignatureApp()
app.mainloop()