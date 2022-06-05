import os
from tkinter import *
from PIL import ImageTk, Image
from tkinter import Entry
from tkinter.filedialog import askopenfilename
import tkinter as tk
from csp import *
from KenKen import *
from inputReader import *
import sys
import time

win = tk.Tk()
var = IntVar()
var2 = IntVar()
def readfromfile(INPUTFILE):
    inFile = open(INPUTFILE, 'r') # read from file
    lines = inFile.readlines()
    inFile.close()
    return lines

img = ImageTk.PhotoImage(Image.open("ba1.jpg"))  
l=Label(image=img)
l.pack()
win.title("AI_Project")
#win.configure(background='#2f4f4f')
win.geometry("1300x682")
win.resizable(False,False)


#----------------------------
#mainlabel
#----------------------------

mainLa = tk.Label(win , text= "Kenken Solver", bg="white", fg="black")
mainLa.config(font=("BatmanForeverAlternate", 50))
mainLa.pack()
mainLa.place(bordermode=INSIDE, x=310, y=0)


#----------------------------
#labels in the middle
#----------------------------


label1 = tk.Label(win, text="No option is selected!!",bg="white", fg="black")
label1.pack()
label1.place(bordermode=INSIDE, x=12, y=570)

label2 = tk.Label(win, text="Status: (waiting for inputs)", bg="white", fg="black")
label2.pack()
label2.place(bordermode=INSIDE, x=12, y=600)





#----------------------------
#label above RUN button
#----------------------------

L1 = tk.Label(win , text= "Click Run to solve", bg="#3D75F1", fg="white")
L1.config(font=("King Richard", 25))
L1.pack()
L1.place(bordermode=INSIDE, x=1063, y=280)

#----------------------------
#label above RADIO BUTTON
#----------------------------

L2 = tk.Label(win , text= "Choose the dimentions of the game", bg="#3D75F1", fg="white")
L2.config(font=("King Richard", 21))
L2.pack()
L2.place(bordermode=INSIDE, x=80, y=85)

#----------------------------
#Entry of Directory
#----------------------------



#----------------------------
#Entry of Code
#----------------------------

E2 = Text(win, width = 60, height = 20)
E2.pack()
E2.place(x= 10, y= 230)

#----------------------------
#Result
#----------------------------

E3 = Text(win, width = 40, height = 18)
E3.pack()
E3.place(x= 650, y= 260)




#----------------------------
#result labels
#----------------------------
L45 = tk.Label(win , text= "Result", bg="#3D75F1", fg="white")
L45.config(font=("King Richard", 50))
L45.pack()
L45.place(bordermode=INSIDE, x=735, y=85)



#----------------------------
#Functions:
#----------------------------

def sel():
   selection = "You selected the dimention " + str(var.get())
   label1.config(text = selection)
   x = var.get()
   if x == 1:
       label3.config(text="Directory")
       E2.config(state='disabled')
       E1.config(state='normal')
       E2.delete(0, END)
   elif x ==2:
       
       E1.config(state='disabled')
       E2.config(state='normal')
       E2.delete('1.0', END)
       E1.delete(0, END)

def main_RUN():
    x = var.get()
    y= var2.get()
    args = ReadInput(str(x)+".txt")
    Possible_Values=""

    for i in range(1,args[0]+1):
        Possible_Values+=str(i)

    #ta domain 8a einai me thn idia seira gia olous tous algori8mous gia na einai dikaih h sugkrish
    Domain=OrderedDict()

    for i in range (0,args[0]):
        for j in range (0,args[0]):       
            Domain[str(i)+str(j)]=Possible_Values

    k = KenKen(args,Domain,0)   
    
    
    if(y==1):
        start_time = time.time()
        E3.delete('1.0', END)
        E3.insert(END,"Now executing BT\n")
        start_time = time.time()
        res = backtracking_search(k)
        table = k.PrintGrid(res)
        for i in range (0,x):
            line=""    
            for j in range (0,x):        
                line+=" "+table[str(i)+str(j)]
                
            E3.insert(END,line+"\n")
        exTime=time.time() - start_time
        E3.insert(END,"Total assignments :"+str(k.nassigns)+"\n")
        E3.insert(END,"BT execution time: %.3f secs \n" % (exTime))
        
    elif(y==2):
        E3.delete('1.0', END)
        E3.insert(END,"Now executing BT+FC\n")
        start_time = time.time()
        res = backtracking_search(k,inference=forward_checking)
        table = k.PrintGrid(res)
        for i in range (0,x):
            line=""    
            for j in range (0,x):        
                line+=" "+table[str(i)+str(j)]
                
            E3.insert(END,line+"\n")
        exTime=time.time() - start_time
        E3.insert(END,"Total assignments :"+str(k.nassigns)+"\n")
        E3.insert(END,"BT+FC execution time: %.3f secs \n" % (exTime))
        
    elif(y==3):
        E3.delete('1.0', END)
        E3.insert(END,"Now executing BT+AC\n")
        start_time = time.time()
        res = backtracking_search(k,inference=mac)
        table = k.PrintGrid(res)
        for i in range (0,x):
            line=""    
            for j in range (0,x):        
                line+=" "+table[str(i)+str(j)]
                
            E3.insert(END,line+"\n")
        exTime=time.time() - start_time
        E3.insert(END,"Total assignments :"+str(k.nassigns)+"\n")
        E3.insert(END,"BT+AC execution time: %.3f secs \n" % (exTime))

        

def show():
    x = var.get()
    if(x in [3,4,5,6,7]):
        lines = readfromfile('inputs/'+str(x)+'.txt')
        E2.config(state='normal')
        E2.delete('1.0', END)
        lines = "".join(lines)
        E2.insert(END,lines)
    else:
        label2.config(text="Status: Error, please select a dimention at first!")
#----------------------------
#Buttons:
#----------------------------

R1 = Radiobutton(win, text = "3*3", selectcolor= "white", highlightcolor = "black", activebackground="black", bg="white", fg="black", variable = var, value = 3, command = sel)
R1.pack()
R1.place(bordermode=OUTSIDE, x=80, y=130)

R2 = Radiobutton(win, text = "4*4", selectcolor= "white", highlightcolor = "black",activebackground="black", bg="white", fg="black", variable = var, value = 4, command = sel)
R2.pack()
R2.place(bordermode=OUTSIDE, x=150, y=130)

R3 = Radiobutton(win, text = "5*5", selectcolor= "white", highlightcolor = "black",activebackground="black", bg="white", fg="black", variable = var, value = 5, command = sel)
R3.pack()
R3.place(bordermode=OUTSIDE, x=220, y=130)

R4 = Radiobutton(win, text = "6*6", selectcolor= "white", highlightcolor = "black",activebackground="black", bg="white", fg="black", variable = var, value = 6, command = sel)
R4.pack()
R4.place(bordermode=OUTSIDE, x=290, y=130)

R5 = Radiobutton(win, text = "7*7", selectcolor= "white", highlightcolor = "black",activebackground="black", bg="white", fg="black", variable = var, value = 7, command = sel)
R5.pack()
R5.place(bordermode=OUTSIDE, x=362, y=130)






Run = tk.Button(win, text = "SOLVE", command = main_RUN,  width =5,activebackground= "#DE36BE", activeforeground = "black",height=3,bg="#3D75F1")
Run.config(font=("BatmanForeverAlternate", 40))
Run.pack()
Run.place(x=1050, y=320)

SHOW = tk.Button(win, text = "Genrarte the Game", command = show, width = 20,activebackground= "black", activeforeground = "green",bg="#E33D7C")
SHOW.config(font=("Times New Roman", 22))
SHOW.pack()
SHOW.place(x=80, y=165)


BT = Radiobutton(win, text = "BT", selectcolor= "white", highlightcolor = "black",activebackground="black", bg="white", fg="black", variable = var2, value = 1, command = sel)
BT.pack()
BT.place(bordermode=OUTSIDE, x=650, y=170)

FS = Radiobutton(win, text = "BT+FS", selectcolor= "white", highlightcolor = "black",activebackground="black", bg="white", fg="black", variable = var2, value = 2, command = sel)
FS.pack()
FS.place(bordermode=OUTSIDE, x=650, y=200)

AC = Radiobutton(win, text = "BT+AC", selectcolor= "white", highlightcolor = "black",activebackground="black", bg="white", fg="black", variable = var2, value = 3, command = sel)
AC.pack()
AC.place(bordermode=OUTSIDE, x=650, y=230)

win.mainloop()

