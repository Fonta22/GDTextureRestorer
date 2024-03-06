import os
import hashlib
import zipfile
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class TextureRestorer:
    def __init__(self, master):
        self.master = master
        self.setup_window()

    def setup_window(self):
        self.master.title('Geometry Dash Texture Restorer')
        self.master.iconbitmap(default='./assets/arrow.ico')
        self.master.geometry('450x220')
        self.master.resizable(False, False)
        self.setup_widgets()

    def setup_widgets(self):
        img = tk.PhotoImage(file='./assets/logo.png').subsample(3, 3)
        label = tk.Label(self.master, image=img)
        label.image = img
        label.pack()

        self.path_input = ttk.Entry(self.master)
        self.path_input.insert(0, 'Geometry Dash Path')
        self.path_input.place(x=10, y=140, width=390, height=20)

        browse_btn = ttk.Button(self.master, text='...', command=self.open_file)
        browse_btn.place(x=410, y=140, width=30, height=20)

        restore_btn = ttk.Button(self.master, text='Restore Original Textures', command=self.show_unzip_progress)
        restore_btn.place(x=10, y=165, width=430, height=25)

        ttk.Label(self.master, text='Fonta22 © 2023', anchor='e').place(x=10, y=195)

    def open_file(self):
        filepath = filedialog.askopenfilename(
            title='Find Geometry Dash',
            filetypes=(('Executable', '*.exe'), ('All Files', '*.*')),
            initialdir=os.getcwd()
        )

        if filepath:
            filepath = os.path.normpath(filepath)
            self.path_input.delete(0, tk.END)
            self.path_input.insert(0, filepath)

    def show_unzip_progress(self):
        gd_path = self.path_input.get()

        if not os.path.isfile(gd_path):
            messagebox.showerror('Invalid Path', 'You need to enter the path to Geometry Dash.')
            return

        destination_path = os.path.dirname(gd_path)

        zip_filepath = filedialog.askopenfilename(
            title='Select Resources.zip',
            filetypes=(('ZIP Files', '*.zip'), ('All Files', '*.*')),
            initialdir=os.getcwd()
        )

        if not zip_filepath:
            messagebox.showerror('Invalid File', 'You need to select the Resources.zip.')
            return

        if not self.verify_md5(zip_filepath):
            messagebox.showerror('Invalid File', 'esources.zip does not match the expected MD5 hash. Please download Resources.zip from the official repo.')
            return

        unzip_window = UnzipProgressWindow(self.master, destination_path, zip_filepath)
        unzip_window.unzip()

    def verify_md5(self, filepath):
        expected_md5 = '2172221137bb57a848f6e56e3556ed9c'
        with open(filepath, 'rb') as f:
            md5_hash = hashlib.md5()
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest() == expected_md5

class UnzipProgressWindow(tk.Toplevel):
    def __init__(self, master, destination_path, zip_filepath):
        super().__init__(master)
        self.title('Unzipping Textures')
        self.geometry('300x80')
        self.resizable(False, False)
        self.destination_path = destination_path
        self.zip_filepath = zip_filepath
        self.setup_widgets()

    def setup_widgets(self):
        ttk.Label(self, text='Restoring Original Textures').place(x=10, y=5)
        self.pBar = ttk.Progressbar(self, orient='horizontal', length=280, mode="determinate", maximum=100, value=0)
        self.pBar.place(x=10, y=25)
        self.percentage_label = ttk.Label(self, text='0%', width='10', anchor="e", justify='left')
        self.percentage_label.place(x=225, y=5)
        self.size_label = ttk.Label(self, text='')
        self.size_label.place(x=10, y=50)

    def unzip(self):
        with zipfile.ZipFile(self.zip_filepath) as zf:
            uncompress_size = sum(file.file_size for file in zf.infolist())
            extracted_size = 0

            for file in zf.infolist():
                extracted_size += file.file_size
                percentage = extracted_size * 100 / uncompress_size

                self.pBar['value'] = percentage
                self.percentage_label['text'] = '{}%'.format(int(percentage))
                size_label_text = '{:.2f} MB of {:.2f} MB uncompressed'.format(extracted_size * 0.000001, uncompress_size * 0.000001)
                self.size_label['text'] = size_label_text

                zf.extract(file, path=self.destination_path)

            self.destroy()
            messagebox.showinfo(title="Textures Restored", message="Textures restored successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextureRestorer(root)
    root.mainloop()
