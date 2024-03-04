import os
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
            filetypes=(('Executable', '*.exe'), ('All Files', '*.*'))
        )

        if filepath:
            filepath = filepath.replace('/', '\\')
            self.path_input.delete(0, tk.END)
            self.path_input.insert(0, filepath)

    def show_unzip_progress(self):
        gd_path = self.path_input.get()

        if not os.path.isfile(gd_path):
            messagebox.showerror('Invalid Path', 'You need to enter the path to Geometry Dash.')
            return

        destination_path = os.path.dirname(gd_path)

        progress_window = UnzipProgressWindow(self.master, destination_path)
        progress_window.start_unzip_thread()

class UnzipProgressWindow(tk.Toplevel):
    def __init__(self, master, destination_path):
        super().__init__(master)
        self.title('Unzipping Textures')
        self.geometry('300x80')
        self.resizable(False, False)
        self.destination_path = destination_path
        self.setup_widgets()

    def setup_widgets(self):
        ttk.Label(self, text='Restoring Original Textures').place(x=10, y=5)
        self.pBar = ttk.Progressbar(self, orient='horizontal', length=280, mode="determinate", maximum=100, value=0)
        self.pBar.place(x=10, y=25)
        self.percentage_label = ttk.Label(self, text='0%', width='10', anchor="e", justify='left')
        self.percentage_label.place(x=225, y=5)
        self.size_label = ttk.Label(self, text='')
        self.size_label.place(x=10, y=50)

    def start_unzip_thread(self):
        threading.Thread(target=self.unzip).start()

    def unzip(self):
        with zipfile.ZipFile('./data/Resources.zip') as zf:
            uncompress_size = sum(file.file_size for file in zf.infolist())
            extracted_size = 0

            for file in zf.infolist():
                extracted_size += file.file_size
                percentage = extracted_size * 100 / uncompress_size

                self.pBar['value'] = percentage
                self.percentage_label['text'] = f'{int(percentage)}%'
                size_label_text = f'{round(extracted_size * 0.000001, 2)} MB of {round(uncompress_size * 0.000001, 2)} MB uncompressed'
                self.size_label['text'] = size_label_text

                zf.extract(file, path=self.destination_path)

            self.destroy()
            messagebox.showinfo(title="Textures Restored", message="Textures restored successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextureRestorer(root)
    root.mainloop()
