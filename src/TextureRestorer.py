import os
import zipfile

from tkinter   import Tk, PhotoImage, Label, Entry, Button, filedialog, ttk, Toplevel, messagebox
from threading import Thread


class TextureRestorer:
    def __init__(self, master):
        """
        Initialize the TextureRestorer class.

        Parameters:
        - master (Tk): The Tkinter root window.
        """
        self.master = master
        self.setup_window()

    def setup_window(self):
        """
        Set up the main Tkinter window.
        """
        self.master.title('Geometry Dash Texture Restorer')
        self.master.iconbitmap(default='./assets/arrow.ico')
        self.master.geometry('450x220')
        self.master.resizable(False, False)

        self.setup_widgets()

    def setup_widgets(self):
        """
        Set up the widgets in the main window.
        """
        img = PhotoImage(file='./assets/logo.png').subsample(3, 3)
        Label(self.master, image=img).pack()

        self.path_input = ttk.Entry(self.master)
        self.path_input.insert(0, 'Geometry Dash Path')
        self.path_input.place(x=10, y=140, width=390, height=20)

        browse_btn = ttk.Button(self.master, text='...', command=self.open_file)
        browse_btn.place(x=410, y=140, width=30, height=20)

        restore_btn = ttk.Button(self.master, text='Restore Original Textures', command=self.show_unzip_progress)
        restore_btn.place(x=10, y=165, width=430, height=25)

        label = ttk.Label(self.master, text='Fonta22 © 2023', anchor='e')
        label.place(x=10, y=195)

    @staticmethod
    def open_file():
        """
        Open a file dialog to select the Geometry Dash executable.
        """
        filepath = filedialog.askopenfilename(
            title='Find Geometry Dash',
            filetypes=(('Executable', '*.exe'), ('All Files', '*.*'))
        )

        if filepath:
            filepath = filepath.replace('/', '\\')
            self.path_input.delete(0, ttk.END)
            self.path_input.insert(0, filepath)

    def show_unzip_progress(self):
        """
        Show the progress window for unzipping textures.
        """
        gd_path = self.path_input.get()

        if not os.path.isfile(gd_path):
            messagebox.showerror('Invalid Path', 'You need to enter the path to Geometry Dash.')
            return

        destination_path = os.path.dirname(gd_path)

        progress_window = UnzipProgressWindow(self.master, destination_path)
        progress_window.start_unzip_thread()

class UnzipProgressWindow(Toplevel):
    def __init__(self, master, destination_path):
        """
        Initialize the UnzipProgressWindow class.

        Parameters:
        - master (Tk): The Tkinter root window.
        - destination_path (str): The path where the textures will be extracted.
        """
        super().__init__(master)
        self.title('Unzipping Textures')
        self.geometry('300x80')
        self.resizable(False, False)

        self.setup_widgets()

        self.destination_path = destination_path

    def setup_widgets(self):
        """
        Set up widgets in the progress window.
        """
        title_label = ttk.Label(self, text='Restoring Original Textures')
        title_label.place(x=10, y=5)

        self.pBar = ttk.Progressbar(self, orient=ttk.HORIZONTAL, length=280, mode="determinate", maximum=100, value=0)
        self.pBar.place(x=10, y=25)

        self.percentage_label = ttk.Label(self, text='0%', width='10', anchor="e", justify=ttk.LEFT)
        self.percentage_label.place(x=225, y=5)

        size_label = ttk.Label(self, text='')
        size_label.place(x=10, y=50)

    def start_unzip_thread(self):
        """
        Start a thread for the unzip process.
        """
        Thread(target=self.unzip).start()

    def unzip(self):
        """
        Unzip the textures and update the progress bar.
        """
        zf = zipfile.ZipFile('./data/Resources.zip')
        uncompress_size = sum((file.file_size for file in zf.infolist()))
        extracted_size = 0

        for file in zf.infolist():
            extracted_size += file.file_size
            percentage = extracted_size * 100 / uncompress_size

            self.pBar['value'] = percentage
            self.percentage_label['text'] = f'{int(percentage)}%'
            size_label_text = f'{round(extracted_size * 0.000001, 2)} MB of {round(uncompress_size * 0.000001, 2)} MB uncompressed'
            size_label['text'] = size_label_text

            zf.extract(file, path=self.destination_path)

        self.destroy()
        messagebox.showinfo(title="Textures Restored", message="Textures restored successfully.")

if __name__ == "__main__":
    root = Tk()
    app = TextureRestorer(root)
    root.mainloop()
