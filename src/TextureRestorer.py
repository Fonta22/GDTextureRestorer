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
        self.path_input.place(relx=0.02, rely=0.64, relwidth=0.88, relheight=0.09)

        browse_btn = ttk.Button(self.master, text='...', command=self.open_file)
        browse_btn.place(relx=0.92, rely=0.64, relwidth=0.05, relheight=0.09)

        restore_btn = ttk.Button(self.master, text='Restore Original Textures', command=self.show_unzip_progress)
        restore_btn.place(relx=0.02, rely=0.75, relwidth=0.95, relheight=0.11)

        ttk.Label(self.master, text='Fonta22 © 2023', anchor='e').place(relx=0.02, rely=0.90)

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
            messagebox.showerror('Invalid File', 'Resources.zip does not match the expected MD5 hash. Please download Resources.zip from the official repo.')
            return

        UnzipProgressWindow(self.master, destination_path, zip_filepath)

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
        self.unzip()

    def setup_widgets(self):
        ttk.Label(self, text='Restoring Original Textures').place(relx=0.03, rely=0.06)
        self.pBar = ttk.Progressbar(self, orient='horizontal', length=280, mode="determinate", maximum=100, value=0)
        self.pBar.place(relx=0.03, rely=0.31, relwidth=0.93, relheight=0.31)
        self.percentage_label = ttk.Label(self, text='0%', width='10', anchor="e", justify='left')
        self.percentage_label.place(relx=0.70, rely=0.06)
        self.size_label = ttk.Label(self, text='')
        self.size_label.place(relx=0.03, rely=0.66)

    def unzip(self):
        def _unzip():
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
        
        threading.Thread(target=_unzip).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextureRestorer(root)
    root.mainloop()
