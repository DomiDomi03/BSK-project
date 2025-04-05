import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import psutil
import declarations as ds
import os

class PDF:
    def __init__(self, pdf_name, pdf_path):
        self.pdf_name = pdf_name
        self.pdf_path = pdf_path

    def __str__(self):
        return f"{self.pdf_name}"


# podanie PIN przez użytkownika
def pin(AES_key_pin, pin_entry, root):
    AES_key_pin = pin_entry.get() # Przekazujemy wprowadzone dane
    root.destroy() # zamknięcie okna
    return AES_key_pin

# znajduje usb podpięte do komputera
def find_usb():
    return {p.device for p in psutil.disk_partitions() if 'removable' in p.opts.lower()}

# wybór tylko plików pdf
def choose_pdf(info, pdf_file):
    file = filedialog.askopenfilename(
        title="Wybierz plik PDF",
        filetypes=(("Pliki PDF", "*.pdf"), ("Wszystkie pliki", "*.*"))
    )
    if file:
        pdf_file.pdf_path = file # ścieżka do pliku
        pdf_file.pdf_name = Path(file).name # nazwa do pliku
        info.set(pdf_file.pdf_name)

# podpis pdf

def signature_pdf(AES_key_pin, pin_entry, root):
    user_pin = pin(AES_key_pin, pin_entry, root)
    usb_path = find_usb()
    full_path = os.path.join(list(usb_path)[0], ds.file_name)
    # odczytanie klucza prywatnego zasztfrowanego w AES
    if os.path.exists(full_path) and os.path.isfile(full_path):
        try:
            with open(full_path, 'rb') as file:
                content = file.read()  # Odczytujemy zawartość binarną
                content = content.decode("latin1") # koduje na odpowiedni format

            # Szukamy prywatnego klucza
            start_marker = "Decrypted private key:"
            end_marker = "Public key:"
            if start_marker in content:
                start_index = content.index(start_marker)  # Znajdź początek
                content_after_marker = content[start_index + len(start_marker)+1:]
                #decrypted_key = content[start_index+len(start_marker)+1:]
                #print(decrypted_key)
                end_index = content_after_marker.find(end_marker)

                if end_index != -1:
                    decrypted_key_full = content_after_marker[:end_index] #.strip() - usuwa białe znaki
                print(decrypted_key_full)
            # szukanie iv

       #AES.decrypt_aes(decrypted_key_full, iv, user_pin)

        except FileNotFoundError:
            print("Plik nie został znaleziony!")

def signature_pdf_window(AES_key_pin, pdf_file):
    detected_usb = True if str(find_usb()) != "set()" else False
    detected_pdf_file = True if pdf_file.pdf_path is not None else False
    # wykryto USB
    if detected_usb is True and detected_pdf_file is True:
        root = tk.Tk()
        root.title("Enter PIN")
        root.geometry("400x200")
        root.configure(bg="#bcbfdc")

        title_label = tk.Label(root, text="Please enter PIN to decrypt the private key:", bg="#bcbfdc")
        title_label.pack(pady=20)

        # Pole do wprowadzania PIN-u z maskowaniem znaków
        pin_entry = tk.Entry(root, show="*", width=15)
        pin_entry.pack(pady=10)

        # przycisk do zatwierdzenia PIN-u
        verify_button = tk.Button(root, text="OK", command=lambda: signature_pdf(AES_key_pin, pin_entry, root))
        verify_button.pack(pady=10)

        root.mainloop()
    # nie wykryto USB
    else:
        root = tk.Tk()
        root.title("Error")
        root.geometry("250x100")
        root.configure(bg="#bcbfdc")

        info_text = None
        if detected_usb is False and detected_pdf_file is False:
            info_text = "Did not detect any USB device \n and the pdf file was not choosen!"
        elif detected_usb is False:
            info_text = "Did not detect any USB device!"
        elif detected_pdf_file is False:
            info_text = "The pdf file was not choosen!"

        title_label = tk.Label(root, text=info_text, bg="#bcbfdc")
        title_label.pack(pady=10)

        verify_button = tk.Button(root, text="Close", command= root.destroy)
        verify_button.pack(pady=10)


# Funkcja do utworzenia głównego okna aplikacji
def create_window():
    root = tk.Tk()
    root.title("BSK project")
    root.geometry("400x400")
    root.configure(bg="#bcbfdc")

    # deklaracja zmiennych
    info = tk.StringVar()
    info.set("No file chosen")
    pdf_file = PDF(None, None)
    AES_key_pin = 0
    info = tk.StringVar()
    info.set("No file chosen")

    root.update()

    # przycisk do wybierania pliku pdf
    button_choose_pdf = tk.Button(
        root,
        text="Choose pdf file",
        command=lambda: choose_pdf(info, pdf_file),
        fg="black",  # Kolor tekstu
        bg="white",  # Kolor tła przycisku (czarne)
        relief="flat"  # Opcjonalnie, jeśli chcesz, by przycisk był płaski
    )
    button_choose_pdf.pack(pady=(120, 0))

    # przycisk do podpisywania pdf
    button_signature= tk.Button(
        root,
        text="Signature pdf file",
        command=lambda: signature_pdf_window(AES_key_pin, pdf_file),
        fg="black",  # Kolor tekstu
        bg="white",  # Kolor tła przycisku (czarne)
        relief="flat"  # Opcjonalnie, jeśli chcesz, by przycisk był płaski
    )
    button_signature.pack(pady=(10, 0))

    # przycisk do weryfikacji pdf
    button_verify = tk.Button(
        root,
        text="Verify signature",
        # command=,
        fg="black",  # Kolor tekstu
        bg="white",  # Kolor tła przycisku (czarne)
        relief="flat"  # Opcjonalnie, jeśli chcesz, by przycisk był płaski
    )
    button_verify.pack(pady=(10, 0))

    label = tk.Label(root, textvariable=info, bg="#bcbfdc", fg="black")
    label.pack(pady=(20, 0))

    root.mainloop()

create_window()

