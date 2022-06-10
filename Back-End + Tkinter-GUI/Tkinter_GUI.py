from tkinter import *
import tkinter as tk
from tracemalloc import start
from turtle import color
from types import CellType
from tkinter import ttk
from turtle import colormode, width
from cgi import test
from optparse import Values
from kenken import kenkenGame
from kenken import generateKenkenPuzzle
from csp import CSP
from tkinter import messagebox

def generate_problem():
    global size
    size = scale.get()
    global algorithm_number
    algorithm_number = option_number.get()
    global cliques
    cliques = generateKenkenPuzzle.generate(size)
    start_window.destroy()
    create_board_window()


def back_button():
    board_window.destroy()
    create_start_window()
    

def submit():
    try:
        ken = kenkenGame.Kenken(size, cliques)
        global generated_answer
        if(algorithm_number == 1):
            generated_answer = CSP.backtracking_search(ken)
        elif(algorithm_number == 2):
            generated_answer = CSP.backtracking_search(ken,inference=CSP.forward_checking)
        elif(algorithm_number == 3):
            generated_answer = CSP.backtracking_search(ken,inference=CSP.mac)
        result_arr=ken.get_result_arr(generated_answer)
        values = [int(entry.get()) for entry in entries]
        if (values == result_arr):
            messagebox.showinfo(title='KenKen',message='Correct!')
        else:
            messagebox.showinfo(title='KenKen',message='Wrong Answer, try again.')
    except:
        messagebox.showinfo(title='KenKen',message='Error, Try Again')


    
def create_start_window():
    global start_window
    start_window = Tk()
    start_window.geometry("820x490")
    start_window.title("KenKen")
    start_window.config(background="white")
    label = Label(start_window,text="KenKen",font=('Arial',40,'bold'),fg='black',bg='white',pady=40)
    label.pack(side='top')
    radio_frame = Frame(start_window, highlightbackground='black').pack()
    label = Label(start_window,text="Choose CSP Algorithm:",font=('Arial',15,'bold'),fg='black',bg='white')
    label.pack(pady=10,anchor='w')
    global option_number
    option_number = IntVar()
    option_number.set(1)
    Radiobutton(radio_frame, font=('Arial',10,'bold'), text='Backtracking', variable=option_number, value=1, background='white').pack(anchor='w',padx=10)
    Radiobutton(radio_frame, font=('Arial',10,'bold'),text='Backtracking with forward checking', variable=option_number, value=2, background='white').pack(anchor='w',padx=10)
    Radiobutton(radio_frame, font=('Arial',10,'bold'),text='Backtracking with forward checking and arc consistency', variable=option_number, value=3, background='white').pack(anchor='w',padx=10)
    my_label = option_number.get()
    label = Label(start_window,text="",bg='white')
    label.pack(pady=5)
    label = Label(start_window,text="Choose board size:",font=('Arial',15,'bold'),fg='black',bg='white')
    label.pack(pady=10,anchor='w')
    global scale
    #GUI is up to 7x7 because tkinter scroll bar sucks :/
    scale = Scale(start_window,from_=3,to=7, orient=HORIZONTAL,length=810,showvalue=1,tickinterval=1,resolution=1,background='white')
    scale.pack()
    generateButton = Button(start_window,text='Generate Puzzle',command=generate_problem,fg='black',bg='white',activebackground='white',font=('Arial',12,'bold'),state=ACTIVE,width=420,height=20, border= 5) #we can add image with image= parameter
    generateButton.pack()
    start_window.mainloop() #place start_window on computer screen and listen to events

def create_board_window():
    top=0
    bottom=1
    left=2
    right=3
    global board_window 
    board_window = tk.Tk()
    board_window.title("KenKen")
    main_frame = tk.Frame(board_window,background='white')
    main_frame.grid(pady=10,padx=10)
    global entries
    entries = []
    global values
    values = []
    operation, remove_border = kenkenGame.gui_border_configurations(cliques,size)
    #print(operation)
    #print(remove_border)
    for i in range(size):
        for j in range(size):
            frame = tk.Frame(main_frame,height=8,border=5,borderwidth=5,background='white',highlightbackground='#DFDFDF',highlightthickness='0.5',padx=10,pady=10)
            frame.grid(row = i+1, column = j+1,sticky='nsew')
            for part in range(2):
                if(part == 0):
                    if(remove_border[i][j][top] == 0): #top
                        line_style = ttk.Style()
                        line_style.configure("Line.TSeparator", background="#000000")
                        separator = ttk.Separator(orient="vertical", style="Line.TSeparator",)
                        separator.place(in_=frame, x=0, y=-90 ,rely=1.0, height=3,width=3,bordermode='outside', relwidth=1,relheight=0)
                    if(remove_border[i][j][bottom] == 0): #bottom
                        line_style = ttk.Style()
                        line_style.configure("Line.TSeparator", background="#000000")
                        separator = ttk.Separator(orient="vertical", style="Line.TSeparator",)
                        separator.place(in_=frame, x=0, y=0 ,rely=1.0, height=3,width=3,bordermode='outside', relwidth=1,relheight=0)
                    if(remove_border[i][j][left] == 0): #left
                        line_style = ttk.Style()
                        line_style.configure("Line.TSeparator", background="#000000")
                        separator = ttk.Separator(orient="vertical", style="Line.TSeparator",)
                        separator.place(in_=frame, x=0, y=-90 ,rely=1.0, height=3,width=3,bordermode='outside', relwidth=0,relheight=1.0)
                    if(remove_border[i][j][right] == 0): #right
                        line_style = ttk.Style()
                        line_style.configure("Line.TSeparator", background="#000000")
                        separator = ttk.Separator(orient="vertical", style="Line.TSeparator",)
                        separator.place(in_=frame, x=84, y=-90 ,rely=1.0, height=3,width=3,bordermode='outside', relwidth=0,relheight=0.97)
                    if (operation[i][j] != '0' and operation[i][j] != ['0']):
                        if(operation[i][j][0] == '.'): #replacing . with * for better readability
                            lable = tk.Label(frame,text='*'+ operation[i][j][1:],font=('Helvetica', 9, 'bold'),pady=10,background='white',highlightbackground='white',highlightcolor='white').grid(row = i, column = j,sticky='nw')
                        else:
                            lable = tk.Label(frame,text=operation[i][j],font=('Helvetica', 9, 'bold'),pady=10,background='white',highlightbackground='white',highlightcolor='white').grid(row = i, column = j,sticky='nw')
                    else:
                        lable = tk.Label(frame,pady=10,background='white',highlightbackground='white',highlightcolor='white').grid(row = i, column = j,sticky='nw')
                else:
                    entry = tk.Entry(frame,
                                    width = 8,
                                    bg="white",
                                    highlightbackground='white',
                                    highlightcolor='white',
                                    borderwidth=0.5) 
                    entry.place(height=8)
                    entry.grid(row = i+part, column = j,sticky='s')
                    entries.append(entry)

    backButton = tk.Button(board_window,text='Back',command=back_button,fg='black',bg='white',activebackground='white',font=('Arial',12,'bold'),width=8*size,height=1, border= 2,pady=10) #we can add image with image= parameter
    backButton.grid(row=size+3,column=0,columnspan=size)
    submit_button = tk.Button(board_window,text='Submit',command=submit,fg='black',bg='white',activebackground='white',font=('Arial',12,'bold'),width=8*size,height=1, border= 2,pady=10) #we can add image with image= parameter
    submit_button.grid(row=size+4,column=0,columnspan=size,pady=5)
    board_window.mainloop()


create_start_window()