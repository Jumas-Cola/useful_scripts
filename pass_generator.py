from tkinter import *
import random


class App(Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.geometry("400x250")
        self.parent.title('Password Generator')
        self.var = IntVar()
        self.var.set(12)
        self.pass_type = IntVar()

        self.scale = Scale(self.parent,
                           tickinterval=1,
                           from_=4,
                           to=18,
                           label='Password length:',
                           length=300,
                           orient=HORIZONTAL,
                           variable=self.var)
        self.scale.pack(anchor=CENTER, pady=10)

        self.chk_frm = Frame()
        self.default = Radiobutton(self.chk_frm,
                                   text="Default",
                                   variable=self.pass_type,
                                   value=0,
                                   command=self.onRadio)
        self.nums_only = Radiobutton(self.chk_frm,
                                     text="Numbers",
                                     variable=self.pass_type,
                                     value=1,
                                     command=self.onRadio)
        self.letters_only = Radiobutton(self.chk_frm,
                                        text="Letters",
                                        variable=self.pass_type,
                                        value=2,
                                        command=self.onRadio)
        self.chk_frm.pack(anchor=CENTER)
        self.default.pack(side=LEFT, pady=10)
        self.nums_only.pack(side=LEFT, pady=10)
        self.letters_only.pack(side=LEFT, pady=10)

        self.btn_frm = Frame()
        self.button = Button(self.btn_frm,
                             text="Get Password",
                             command=self.pass_gen)
        self.copy_btn = Button(self.btn_frm,
                               text="Copy",
                               command=self.copy_to_clip)
        self.btn_frm.pack(anchor=CENTER)
        self.button.pack(side=LEFT, pady=10)
        self.copy_btn.pack(side=LEFT, pady=10, padx=10)

        self.entry = Entry(self.parent,
                           width=40)
        self.entry.pack()
        self.styles()

    def styles(self):
        self.parent["bg"] = "#4671D5"
        self.scale["bg"] = "#4671D5"
        self.scale["fg"] = "#FFFFFF"
        self.scale["font"] = "Helvetica 11 bold"
        self.scale["highlightbackground"] = "#4671D5"
        self.chk_frm["bg"] = "#4671D5"
        self.default["bg"] = "#4671D5"
        self.default["fg"] = "#FFFFFF"
        self.default["font"] = "Helvetica 11 bold"
        self.nums_only["bg"] = "#4671D5"
        self.nums_only["fg"] = "#FFFFFF"
        self.nums_only["font"] = "Helvetica 11 bold"
        self.letters_only["bg"] = "#4671D5"
        self.letters_only["fg"] = "#FFFFFF"
        self.letters_only["font"] = "Helvetica 11 bold"
        self.btn_frm["bg"] = "#4671D5"
        self.button["bg"] = "#FFAA00"
        self.button["fg"] = "#FFFFFF"
        self.button["font"] = "Helvetica 11 bold"
        self.copy_btn["bg"] = "#FFAA00"
        self.copy_btn["fg"] = "#FFFFFF"
        self.copy_btn["font"] = "Helvetica 11 bold"
        self.entry["bg"] = "#98ADDE"
        self.entry["font"] = "Helvetica 11 bold"
        self.onRadio()

    def onRadio(self):
        v = self.pass_type.get()
        if v == 0:
            self.default["fg"] = "#FFAA00"
            self.nums_only["fg"] = "#FFFFFF"
            self.letters_only["fg"] = "#FFFFFF"
        elif v == 1:
            self.default["fg"] = "#FFFFFF"
            self.nums_only["fg"] = "#FFAA00"
            self.letters_only["fg"] = "#FFFFFF"
        elif v == 2:
            self.default["fg"] = "#FFFFFF"
            self.nums_only["fg"] = "#FFFFFF"
            self.letters_only["fg"] = "#FFAA00"

    def copy_to_clip(self):
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(self.entry.get())
        r.update()
        r.destroy()

    def pass_gen(self):
        selection = ''
        pass_type = self.pass_type.get()
        pass_len = self.var.get()
        if pass_type == 0:
            sgns = pass_len // 4
            selection = pass_generate(sgns, pass_len - sgns * 3, sgns, sgns)
        elif pass_type == 1:
            selection = pass_generate(pass_len, 0, 0, 0)
        elif pass_type == 2:
            sgns = pass_len // 4
            selection = pass_generate(0, pass_len - sgns, sgns, 0)
        self.entry.delete(0, len(self.entry.get()))
        self.entry.insert(0, selection)


def pass_generate(nums=3, chars=5, caps=2, signs=2):
    password = []
    for i in range(nums):
        password += random.choice([*'0123456789'])
    for i in range(chars):
        password += random.choice([chr(i) for i in range(97, 123)])
    for i in range(caps):
        password += random.choice([chr(i) for i in range(65, 91)])
    for i in range(signs):
        password += random.choice([*r'!@#$%^&*_=+-/"[](){}'])
    random.shuffle(password)
    return ''.join(password)


def main():
    root = Tk()
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
