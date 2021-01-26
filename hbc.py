#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This application converts csv-files for HomeBank imports

import tkinter as tk
from tkinter import ttk, filedialog, Menu, messagebox
import csv, os

def SelectFile():
    global Value, Elem02
    TempVar=filedialog.askopenfile(
        initialdir=Value['Path'],
        title='Bitte Datei auswählen', 
        filetypes=[('csv Dateien', '*.csv')]
        )
    if TempVar=='':
        return False

    Value['File']=TempVar.name
    Elem02.config(state='normal')

def OpenFile():
    global Value

    try:
        TempVar = Value['File']
    except:
        messagebox.showerror('Speichern','Bitte zuerst Importdatei auswählen!')
        return False

    DatOp=open(Value['File'], 'r', encoding='ISO-8859-1')
    DatLe=csv.reader(DatOp, delimiter=';')
    DatIn=list(DatLe)
    DatOp.close()
    
    try:
        Expor=tk.filedialog.asksaveasfile(
            initialdir=Value['Path'], 
            mode='w', filetypes=[('csv Datei', '*.csv')]
            ).name
    except:
        return False

    Schal=0
    DaSch=open(Expor, 'w', newline='', encoding='utf-8')
    for Zei in DatIn:
        if Zei:
            if Zei[0]=='Buchung':
                Schal=1
        if Schal==1:
            Datum=Zei[0]
            Symbo='11'
            Auftr=Zei[2]
            BuTex=Zei[3]
            Zweck=Zei[4]
            Betra=Zei[-2]
            if 'VISA' in Auftr:
                Symbo='1'

            if 'Gehalt' in BuTex:
                Symbo='4'   

            if 'Dauerauftrag' in BuTex:
                Symbo='7'

            if 'berweisung' in BuTex:
                Symbo='4'

            if 'Gutschrift' in BuTex:
                Symbo='4'
            
            DaSch.write(Datum+';'+Symbo+';'+BuTex+';'+Auftr+';'+Zweck+';'+Betra+';;\n')    
    DaSch.close()

    messagebox.showinfo('Abgeschlossen', 'Die Datei wurde gespeichert.')
    
def Information():
    messagebox.showinfo(
        'Information',
        'HomeBank csv-Converter\nversion '+Value['Version']+'\n'+Value['Date']
        )

# --- Variables ----
Value={'Path': '/home/'+os.environ['USER']+'/Downloads/', 'Version': '0.1', 'Date': '2021/01/18'}

# --- prepare GUI ---
Window=tk.Tk()
Window.minsize(400, 100)
Window.resizable(False, False)
Window.title('HomeBankConvert')

# --- GUI ---

MenuBar=Menu(Window)
WinMenu=Menu(MenuBar, tearoff=0)
MenuBar.add_cascade(label='Datei', menu=WinMenu)
WinMenu.add_command(label='Laden', command=SelectFile)
WinMenu.add_command(label='Speichern', command=OpenFile)
WinMenu.add_separator() 
WinMenu.add_command(label='Quit', command=Window.quit)
MenuBar.add_command(label='Info', command=Information)
Window.config(menu=MenuBar)

Elem01=ttk.Button(Window, text='Datei auswählen', command=SelectFile)
Elem01.place(x=2, y=0, width=396, height=28)
Elem02=ttk.Button(Window, text='Konvertieren und Ausgeben', command=OpenFile, state='disabled')
Elem02.place(x=2, y=30, width=396, height=28)
Elem03=ttk.Label(Window, text='')
Elem03.place(x=2, y=60, width=396, height=28)

Window.mainloop()