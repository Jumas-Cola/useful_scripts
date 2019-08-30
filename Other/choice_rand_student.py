from tkinter import Tk, Frame, Entry, Label, Button
from tkinter import messagebox
from random import randint


def some_func(context):
    ran_num = randint(1, context['students_count'])
    context['self'].rand_num['text'] = str(ran_num)
    context['self'].rand_num['fg'] = '#{:02X}{:02X}{:02X}'.format(randint(0, 255), randint(0, 255), randint(0, 255))
    if context['interval'] < context['max_interval']:
        context['counter'] += 1
        if context['counter'] == 5:
            context['counter'] = 0
            context['interval'] += 8
        context['self'].parent.after(context['interval'], some_func, context)


class App(Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.geometry('300x300')
        self.parent.minsize(250, 280)
        self.parent.title('Random choice')

        self.students_count_lbl = Label(text='Количество учеников:')
        self.students_count_lbl.pack(pady=5)
        self.students_count = Entry()
        self.students_count.pack(pady=5)

        self.get_random_btn = Button(
            text='Пуск',
            command=self.get_random
        )
        self.get_random_btn.pack(pady=5)

        self.rand_num = Label(text='0')
        self.rand_num.pack()

        self.styles()

    def styles(self):
        self.rand_num['font'] = 'Calibri 150 bold'
        self.get_random_btn['bg'] = '#32CD32'
        self.get_random_btn['font'] = 'Calibri 12 bold'
        self.students_count_lbl['font'] = 'Calibri 12 bold'

    def get_random(self):
        students_count = self.students_count.get()
        if not students_count:
            messagebox.showerror(
                'Error', 'Введите число учеников в классе!')
            return
        try:
            students_count = int(students_count)
        except:
            messagebox.showerror(
                'Error', 'Введите корректное число учеников!')
            return
        some_func({
            'self': self,
            'students_count': students_count,
            'interval': 50,
            'max_interval': 110,
            'counter': 0}
        )


def main():
    root = Tk()
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
