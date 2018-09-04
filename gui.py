# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 17:43:43 2018

@author: Francesco
"""
import os
from smarthouse import setup
from calculate_all import ourModel 
from calculate_all import equiprob 
from calculate_all import baseline 
from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

LARGE_FONT = ("Verdana", 12) # font's family is Verdana, font's size is 12 
days=14
tipo=""
class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Progetto") # set the title of the main window
        self.geometry('{}x{}'.format(1280, 720)) # set size of the main window to 300x300 pixels
 
        # this container contains all the pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)   # make the cell in grid cover the entire window
        container.grid_columnconfigure(0,weight=1) # make the cell in grid cover the entire window
        self.frames = {} # these are pages we want to navigate to
 
        for F in [StartPage]: # for each page
            frame = F(container, self) # create the page
            self.frames[F] = frame  # store into frames
            frame.grid(row=0, column=0, sticky="nsew") # grid it to container
 
        self.show_frame(StartPage) # let the first page is StartPage
 
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

class StartPage(tk.Frame):
    global days                                
    
    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
#        label = tk.Label(self, text='Scelta del numero dei giorni', font=LARGE_FONT)
#        label.pack(pady=10, padx=10)

        #self.geometry('{}x{}'.format(1280, 720)) # set size of the main window to 1280x720 pixels
        button1 = tk.Button(self, text="Sfoglia...", command=self.load_file, width=10)
        button1.pack()
       
        
    def funzione(self,days,tipo):
        var = tk.IntVar()
        if days==13:
            w1 = tk.Scale(self, from_=0, to=13,orient="horizontal",variable = var)
            #w1.set(14)
            w1.pack()
            button3 = tk.Button(self, text='Avvia',  # when click on this button, call the show_frame method to make PageOne appear     
                               command=lambda: self.stampa(var,tipo))
            button3.pack() # pack it in
            button2 = tk.Button(self, text='Cancella',  # when click on this button, call the show_frame method to make PageOne appear
                            command=lambda : self.cancella())
            button2.pack() # pack it in
        
        else:
            w2 = tk.Scale(self, from_=0, to=21,orient="horizontal",variable=var)
            #w2.set(14)
            w2.pack()
            button4 = tk.Button(self, text='Avvia',  # when click on this button, call the show_frame method to make PageOne appear        
                                command=lambda: self.stampa(var,tipo))
            button4.pack() # pack it in
            button7 = tk.Button(self, text='Cancella',  # when click on this button, call the show_frame method to make PageOne appear
                            command=lambda : self.cancella())
            button7.pack() # pack it in
        #show_frame(PageOne)
    def load_file(self):
        fname = askopenfilename(filetypes=(("TXT files", "*.txt;*.TXT"),
                                           ("All files", "*.*") ))
        fname = os.path.basename(fname)
        if fname:
        
            try:
                _, lista =setup(fname)
                if fname == 'OrdonezA_integrated.txt':
                    tipo="A"
                    
                    days =13
                    buttona = tk.Button(self, text="Avanti",
                                    command=lambda : self.funzione(days,tipo))
                    buttona.pack() 
                else:
                    tipo="B"
                    
                    days =21
                    buttonb = tk.Button(self, text="Avanti",
                                    command=lambda : self.funzione(days,tipo))
                    buttonb.pack() 
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Errore di lettura del file\n'%s'" % fname)
            return

    def stampa(self,var,tipo):
        
        
        out1= ourModel(var.get(),tipo)
        out2= baseline(var.get(),tipo)
        out3= equiprob(var.get(),tipo)
        app=out1+out2+out3
        app2=tk.Label(self,text=app) 
        app2.pack()
        
        
    def cancella(self):
        for widget in StartPage.winfo_children(self):
            if widget == StartPage.winfo_children(self)[0]:
                continue
            widget.destroy()  
        

    

 
if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()



