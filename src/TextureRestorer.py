import os
import zipfile
from tkinter import *
from tkinter import filedialog, ttk, messagebox
from threading import Thread

def openFile():
    filepath = filedialog.askopenfilename(
        title='Find Geometry Dash',
        filetypes=(
            ('Executable', '*.exe'),
            ('All Files', '*.*')
        )
    )

    path_input.delete(0, END)

    if filepath == '':
        path_input.insert(0, 'Geometry Dash Path')
    else:
        filepath = filepath.replace('/', '\\')
        path_input.insert(0, filepath)

def showUnzipProgress():
    gd_path = path_input.get()

    if not os.path.isfile(gd_path):
        messagebox.showerror('Invalid Path', 'You need to enter the path to Geometry Dash.')
        return
    
    destination_path = gd_path.split('\\')
    destination_path = '\\'.join(destination_path[:-1])

    top = Toplevel()
    top.title('Unzipping Textures')

    top_width = 300
    top_height = 80

    top_x = window.winfo_x() + widnow_width/6
    top_y = window.winfo_y() + window_height/3

    top.geometry("%dx%d+%d+%d" % (top_width, top_height, top_x, top_y))
    top.resizable(False, False)

    title_label = ttk.Label(top, text='Restoring Original Textures')
    title_label.place(x=10, y=5)

    pBar = ttk.Progressbar(top, orient=HORIZONTAL, length=280, mode="determinate", maximum=100, value=0)
    pBar.place(x=10, y=25)

    percentage_label = ttk.Label(top, text='0%', width='10', anchor="e", justify=LEFT)
    percentage_label.place(x=225, y=5)

    size_label = ttk.Label(top, text='')
    size_label.place(x=10, y=50)

    def unzip():
        zf = zipfile.ZipFile('./data/Resources.zip')
        uncompress_size = sum((file.file_size for file in zf.infolist()))
        extracted_size = 0

        for file in zf.infolist():
            extracted_size += file.file_size
            percentage = extracted_size * 100 / uncompress_size

            pBar['value'] = percentage
            percentage_label['text'] = f'{int(percentage)}%'
            size_label['text'] = f'{str(round(extracted_size * 0.000001, 2))} MB of {str(round(uncompress_size * 0.000001, 2))} MB uncompressed'

            zf.extract(file, path=destination_path)
        
        top.destroy()
        top.update()

        messagebox.showinfo(title="Textures Restored", message="Textures restored successfully.")
    
    Thread(target=unzip).start()
    top.mainloop()

window = Tk()

widnow_width = 450
window_height = 220

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = (screen_width/2) - (widnow_width/2)
window_y = (screen_height/2) - (window_height/2)

window.geometry('%dx%d+%d+%d' % (widnow_width, window_height, window_x, window_y))

window.title('Geometry Dash Texture Restorer')
window.iconbitmap(default='./assets/arrow.ico')
window.resizable(False, False)

img = PhotoImage(file='./assets/logo.png').subsample(3, 3)
Label(window, image=img).pack()

path_input = ttk.Entry(window)
path_input.insert(0, 'Geometry Dash Path')
path_input.place(x=10, y=140, width=390, height=20)

browse_btn = ttk.Button(window, text='...', command=openFile)
browse_btn.place(x=410, y=140, width=30, height=20)

remove_btn = ttk.Button(window, text='Restore Original Textures', command=showUnzipProgress)
remove_btn.place(x=10, y=165, width=430, height=25)

label = ttk.Label(window, text='Fonta22 © 2023', anchor='e')
label.place(x=10, y=195)

window.mainloop()