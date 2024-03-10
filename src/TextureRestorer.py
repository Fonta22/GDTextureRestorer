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
        self.gd_path = ''
        self.zip_filepath = ''

    def setup_window(self):
        self.master.title('Geometry Dash Texture Restorer')
        self.master.iconbitmap(default='./assets/arrow.ico')
        self.master.geometry('500x250')
        self.master.resizable(False, False)
        self.setup_widgets()

    def setup_widgets(self):
        img = tk.PhotoImage(file='./assets/logo.png').subsample(3, 3)
        label = tk.Label(self.master, image=img)
        label.image = img
        label.place(relx=0.02, rely=0.02)

        self.gd_path_label = ttk.Label(self.master, text='Select Geometry Dash Path:')
        self.gd_path_label.place(relx=0.02, rely=0.64, relwidth=0.45, relheight=0.09)

        self.gd_path_entry = ttk.Entry(self.master)
        self.gd_path_entry.insert(0, 'Geometry Dash Path')
        self.gd_path_entry.place(relx=0.48, rely=0.64, relwidth=0.45, relheight=0.09)

        browse_gd_btn = ttk.Button(self.master, text='Browse...', command=self.select_gd_path)
        browse_gd_btn.place(relx=0.02, rely=0.75, relwidth=0.45, relheight=0.11)

        self.zip_path_label = ttk.Label(self.master, text='Select Resources.zip:')
        self.zip_path_label.place(relx=0.02, rely=0.87, relwidth=0.45, relheight=0.09)

        self.zip_path_entry = ttk.Entry(self.master)
        self.zip_path_entry.insert(0, 'Resources.zip Path')
        self.zip_path_entry.place(relx=0.48, rely=0.87, relwidth=0.45, relheight=0.09)

        browse_zip_btn = ttk.Button(self.master, text='Browse...', command=self.select_zip_path)
        browse_zip_btn.place(relx=0.02, rely=0.98, relwidth=0.45, relheight=0.11)

        restore_btn = ttk.Button(self.master, text='Restore Original Textures', command=self.show_unzip_progress)
        restore_btn.place(relx=0.48, rely=0.75, relwidth=0.5, relheight=0.24)

        ttk.Label(self.master, text='Fonta22 © 2023').place(relx=0.02, rely=0.90)

    def select_gd_path(self):
        filepath = filedialog.askopenfilename(
            title='Find Geometry Dash',
            filetypes=(('Executable', '*.exe'), ('All Files', '*.*')),
            initialdir=os.getcwd()
        )

        if filepath:
            self.gd_path = os.path.normpath(filepath)
            self.gd_path_entry.delete(0, tk.END)
            self.gd_path_entry.insert(0, self.gd_path)

    def select_zip_path(self):
        filepath = filedialog.askopenfilename(
            title='Select Resources.zip',
            filetypes=(('ZIP Files', '*.zip'), ('All Files', '*.*')),
            initialdir=os.getcwd()
        )

        if filepath:
            self.zip_filepath = os.path.normpath(filepath)
            self.zip_path_entry.delete(0, tk.END)
            self.zip_path_entry.insert(0, self.zip_filepath)

    def show_unzip_progress(self):
        if not self.gd_path:
            messagebox.showerror('Invalid Path', 'You need to enter the path to Geometry Dash.')
            return

        if not os.path.exists(self.gd_path):
            messagebox.showerror('Invalid Path', 'Geometry Dash Path does not exist.')
            return

        if not self.zip_filepath:
            messagebox.showerror('Invalid Path', 'You need to select the Resources.zip.')
            return

        if not os.path.exists(self.zip_filepath):
            messagebox.showerror('Invalid File', 'Resources.zip does not exist.')
            return

        if not self.verify_md5(self.zip_filepath):
            messagebox.showerror('Invalid File', 'Resources.zip does not match the expected MD5 hash. Please download Resources.zip from the official repo.')
            return

        UnzipProgressWindow(self.master, self.gd_path, self.zip_filepath)

    def verify_md5(self, filepath):
        expected_md5 = '2172221137bb57a848f6e56e3556ed9c'
        with open(filepath, 'rb') as f:
            md5_hash = hashlib.md5()
            md5_hash.update(f.read())
            return md5_hash.hexdigest() == expected_md5

class UnzipProgressWindow(tk.Toplevel):
    def __init__(self, master, gd_path, zip_filepath):
        super().__init__(master)
        self.title('Unzipping Textures')
        self.geometry('400x100')
        self.resizable(False, False)
        self.gd_path = gd_path
        self.zip_filepath = zip_filepath
        self.setup_widgets()
        self.unzip()

    def setup_widgets(self):
        ttk.Label(self, text='Restoring Original Textures').place(relx=0.03, rely=0.06)
        self.pBar = ttk.Progressbar(self, orient='horizontal', length=380, mode="determinate", maximum=100, value=0)
        self.pBar.place(relx=0.03, rely=0.31, relwidth=0.93, relheight=0.31)
        self.percentage_label = ttk.Label(self, text='0%', width='10', anchor="e", justify='left')
        self.percentage_label.place(relx=0.70, rely=0.06)

    def unzip(self):
        def _unzip():
            with zipfile.ZipFile(self.zip_filepath) as zf:
                file_infos = zf.infolist()
                uncompress_size = sum(file.file_size for file in file_infos)
                extracted_size = 0

                for file in file_infos:
                    extracted_size += file.file_size
                    percentage = extracted_size * 100 / uncompress_size

                    self.pBar['value'] = percentage
                    self.percentage_label['text'] = f'{int(percentage)}%'

                    zf.extract(file, path=self.gd_path)

                self.destroy()
                messagebox.showinfo(title="Textures Restored", message="Textures restored successfully.")

        threading.Thread(target=_unzip).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextureRestorer(root)
    root.mainloop()
