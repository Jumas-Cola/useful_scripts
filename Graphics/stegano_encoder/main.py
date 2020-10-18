import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as msgbox

from pathlib import Path
import steg_tools as st
from PIL import Image
import numpy as np


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        
        self.img_frame = tk.Frame(self)
        
        self.filedialog_btn = tk.Button(self.img_frame)
        self.filedialog_btn['text'] = 'Select BMP file'
        self.filedialog_btn['command'] = self.open_filedialog
        self.filedialog_btn.pack(side='left')

        self.img_name = tk.StringVar()
        self.img_name_label = tk.Label(self.img_frame, textvariable=self.img_name)
        self.img_name_label.pack(side='right')

        self.img_frame.pack(side='top')


        self.encodec_frame = tk.Frame(self)

        self.filedialog_btn = tk.Button(self.encodec_frame)
        self.filedialog_btn['text'] = 'Stegano encode'
        self.filedialog_btn['command'] = self.steg_encode
        self.filedialog_btn.pack(side='left')

        self.filedialog_btn = tk.Button(self.encodec_frame)
        self.filedialog_btn['text'] = 'Stegano decode'
        self.filedialog_btn['command'] = self.steg_decode
        self.filedialog_btn.pack(side='right')

        self.encodec_frame.pack(side='top')

        
        self.password_label = tk.Label(self, text='Password (optional):')
        self.password_label.pack(side='top')

        
        self.password = tk.StringVar()
        self.password_entry = tk.Entry(self, textvariable=self.password, show='*')
        self.password_entry.pack(side='top')


        self.textarea = tk.Text(self, height=5, width=50)
        self.textarea.pack()

    def open_filedialog(self):
        self.img_path = filedialog.askopenfilename(
            initialdir = './',
            title = 'Select BMP file',
            filetypes = (('bmp files','*.bmp'),)
        )
        self.img_name.set(Path(self.img_path).name)

    def steg_encode(self):
        text = self.textarea.get('1.0', 'end').strip()

        if len(text) == 0:
            msgbox.showwarning('Warning!', 'Text area is empty!')
            return

        if not hasattr(self, 'img_path'):
            msgbox.showerror('Error!', 'Input image is not specified!')
            return

        password = self.password.get().strip()
        
        img = Image.open(self.img_path)
        img_bytes = np.asarray(img).copy()
        
        text_bytes = bytearray(text.encode())

        if len(text_bytes) > len(img_bytes) * len(img_bytes[0]) - 1:
            msgbox.showerror('Error!', 'Text length is longer than image bytes!')
            return

        out_name = Path(self.img_path).stem + '_steg' + Path(self.img_path).suffix
        out_path = Path(self.img_path).parent.joinpath(out_name)

        if len(password) == 0:
            Image.fromarray(st.stegano_encoder(img_bytes, text_bytes)).save(out_path)
        else:
            Image.fromarray(st.rand_stegano_encoder(img_bytes, text_bytes, password)).save(out_path)

        msgbox.showinfo('Sucess!', 'Sucessfuly encoded!')

    def steg_decode(self):

        if not hasattr(self, 'img_path'):
            msgbox.showerror('Error!', 'Input image is not specified!')
            return

        password = self.password.get().strip()

        img = Image.open(self.img_path)
        img_bytes = np.asarray(img).copy()

        self.textarea.delete('1.0', 'end')

        if len(password) == 0:
            self.textarea.insert('end', st.stegano_decoder(img_bytes).decode(errors='ignore').strip())
        else:
            self.textarea.insert('end', st.rand_stegano_decoder(img_bytes, password).decode(errors='ignore').strip())


root = tk.Tk()
app = Application(master=root)
app.mainloop()
