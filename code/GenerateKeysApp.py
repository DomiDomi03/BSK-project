##
#	@file GenerateKeysApp.py
#	@details This application allows users to generate and securely store an RSA key pair. The private key is protected with a user-defined PIN and saved to a selected device (e.g., connected pendrive).
#	@date 11-04-2025
##

import os
import tkinter as tk
import functions as f
import declarations as ds
import RSA_keys as rsa
import AES as aes
import tkinter.ttk as ttk
import threading

## A class that generates a key pair (public and private), gets the pin from the user and saves date to the .txt file
class GenerateKeysApp(tk.Tk):
    ## Constructor of the GenerateKeysApp, starts the application.
    # @param encrypted_private_key Stores the encrypted private key, initially None.
    # @param public_key Stores the public key, initially None.
    # @param user_pin The user's PIN code, initially None.
    # @param iv Initialization vector (IV) for AES encryption, initially None.
    # @param save_location Tkinter StringVar representing the path where files will be saved.
    # @param status_label Tkinter Label widget used to display status messages.
    # @param progress Tkinter Progressbar widget showing operation progress.
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

    ## Method that creates main window of application
    def create_main_window(self):
        root = self
        root.title("Generate keys App")
        root.geometry("300x300")
        root.configure(bg="#bcbfdc")

        devices_list = list(f.find_devices())
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


    ## Method that saves the user pin and starts generating the keys for the user
    # @param new_pin is a pin given by the user
    def save_pin(self, new_pin):
        self.user_pin = new_pin.get()
        print("Pin " + self.user_pin + " saved")

        if self.user_pin is not None:
            self.status_label.config(text="Generating keys...")
            self.progress['value'] = 0
            self.progress.pack(pady=5)
            threading.Thread(target=self.run_generation_process()).start()

    ## Method that saves the generated keys and user pin to the .txt file
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
        self.save_to_file(1)
        self.save_to_file(2)

        self.after(5000, lambda: self.progress.step(20))
        self.after(6000, self.on_generation_complete)

    ## Method that informs user about the successful generation of keys and saving the date to the .txt file
    def on_generation_complete(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.status_label.config(text="Keys generated and saved successfully!")


    ## Method that save the generated keys and pin to the .txt file
    # @param mode the choice between public and private key file
    # @throws Exception if method can not save the file
    # @return Null if the path is invalid
    def save_to_file(self, mode):
        save_path = self.save_location.get()

        if not os.path.isdir(save_path): #is path valid
            print("Invalid path")
            return
        if(mode == 1):
            file_path = os.path.join(save_path, ds.file_name)
        else:
            file_path = os.path.join(save_path, ds.file_name_1)

        try:
            with open(file_path, "wb") as f:
                if(mode == 1):
                    f.write(b"Decrypted private key: ")
                    f.write(self.encrypted_private_key)  # bytes
                    print(self.encrypted_private_key)
                f.write(b"Public key: ")
                PEM_public_key = rsa.convert_PEM_public(self.public_key)
                f.write(PEM_public_key)
                print(PEM_public_key)
                if(mode == 2):
                    f.write(b"happy ending")
                if(mode == 1):
                    f.write(b"User_pin: ")
                    f.write(str(self.user_pin).encode())  # bytes - Zapiszemy PIN w formie bajtów
                    f.write(b"iv: ")
                    f.write(self.iv)  # bytes
            print(f"File saved at {file_path}")

        except Exception as e:
            print(f"Error saving file: {e}")


app = GenerateKeysApp()
app.mainloop()
