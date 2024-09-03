from tkinter import *
from tkinter import ttk

headlabelfont = ("Bold Italic", 15, 'bold')
labelfont = ('Bold Italic', 10)

main = Tk()
main.title('MENÚ PRINCIPAL')
main.geometry('1000x600')

Label(main, text="MENÚ PRICIPAL", font=headlabelfont, bg='#D9D9D9').pack(side=TOP, fill=X)
right_frame = Frame(main, bg="#1F6095")
right_frame.place(x=0.275, y=30, relheight=1, relwidth=1)
left_frame = Frame(main, bg="#A6C3FF")
left_frame.place(x=0, y=30, relheight=1, relwidth=0.275)

Button(left_frame, text='Caracterización Eléctrica',bg="#FDFDFD", font=labelfont, width=24, height=4 ).place(relx=0.13, rely=0.1)
Button(left_frame, text='Caracterización Magnetoeléctrica', font=labelfont, width=24, height=4).place(relx=0.13, rely=0.3)
Button(left_frame, text='Caracterización Magnetoeléctrica Invertida', font=labelfont, width=24, height=4).place(relx=0.13, rely=0.5)
Button(left_frame, text='Pruebas', font=labelfont, width=24, height=4).place(relx=0.13, rely=0.7)

main.update()
main.mainloop()
