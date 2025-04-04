import tkinter as tk
from tkinter import filedialog
from pathlib import Path

class PDF:
    def __init__(self, pdf_name, pdf_path):
        self.pdf_name = pdf_name
        self.pdf_path = pdf_path

    def __str__(self):
        return f"{self.pdf_name}"


def pin(AES_key_pin, pin_entry, root):
    AES_key_pin = pin_entry.get() # Przekazujemy wprowadzone dane
    print(AES_key_pin)
    root.destroy() # zamknięcie okna

def choose_pdf(info, pdf_file):
    file = filedialog.askopenfilename(
        title="Wybierz plik PDF",
        filetypes=(("Pliki PDF", "*.pdf"), ("Wszystkie pliki", "*.*"))
    )
    if file:
        pdf_file.pdf_path = file # ścieżka do pliku
        pdf_file.pdf_name = Path(file).name # nazwa do pliku
        info.set(pdf_file.pdf_name)

def signature_pdf(AES_key_pin):
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
    verify_button = tk.Button(root, text="OK", command=lambda: pin(AES_key_pin, pin_entry, root))
    verify_button.pack(pady=10)

    root.mainloop()

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
        command=lambda: signature_pdf(AES_key_pin),
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

