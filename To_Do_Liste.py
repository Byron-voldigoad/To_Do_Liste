import tkinter
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import sqlite3

window = Tk()

window.title("TO DO LISTE")
window.configure(bg="skyblue")
window.geometry("500x500")

def insert():
    tache = entry.get()
    conn = sqlite3.connect("Todoliste.db")
    cur = conn.cursor()
    t = entry.get()
    if (t == ""):
        messagebox.showerror("Resultat", "Vous devez entrer une tache!!")
    else:
        req = "INSERT INTO Todo(tache,v,T) values(?,true,true)"
        cur.execute(req,(tache,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Resultat","Votre tache a ete ajouter avec succes")


def delete():
    try:
        selected_item = tree.selection()[0]
        question = messagebox.askyesnocancel('Confimation', 'Ete vous sure de vouloir supprimer cette tache?')
        if question:

            tree.delete(selected_item)
            conn = sqlite3.connect("Todoliste.db")
            cur = conn.cursor()
            a = entry.get()

            cur.execute("UPDATE Todo SET v = false WHERE id=?", (a,))

            conn.commit()
            conn.close()
            messagebox.showinfo("Resultat", "La tache a ete supprimer avec succes")
    except:
        messagebox.showerror("ERROR", "Vous devez selectionner une tache et entrer son numero!!")

def acconplie():
    conn = sqlite3.connect("Todoliste.db")
    cur = conn.cursor()
    msg = messagebox.askquestion("Avertissement","Avez vous bel et bien terminer cette tache ?")
    if msg:
        a = entry.get()
        cur.execute("UPDATE Todo SET T = false WHERE id=?", (a,))
        conn.commit()
        conn.close()
    d = c + b
    print(b)
    print(d)
    if ((b==0)):
        messagebox.showinfo("Info", "Vous navez encore terminer aucune tache sur " + str(d))
    elif ((b==0) and (d == 0)):
        messagebox.showinfo("Info", "Vous navez pas encore de taches")
    else:
        messagebox.showinfo("Info", "Felicitation vous avez deja terminer "+str(b)+" tache(s) sur "+str(d))
    if (a==''):
        messagebox.showinfo("Info", "vous devez entrer le num de la tache terminer pour la marquer comme finie")


frame = Frame(window,bg="orange",height=200,width=600)
entry = Entry(frame,font=("century",13))
entry.place(x=170,y=30)

def ex():
    screnn = tkinter.Toplevel(window)
    screnn.geometry("300x300")

    def annul():
        msg = messagebox.askquestion("Avertissement", "Avez vous bel et bien terminer cette tache ?")
        if msg:
            conn = sqlite3.connect("Todoliste.db")
            cur = conn.cursor()
            a = entry.get()
            cur.execute("UPDATE Todo SET T = true WHERE id=?", (a,))
            conn.commit()
            conn.close()
    btn = Button(screnn,font=("century",20),command=annul,width=100,text="Annuler",bg="silver")
    btn.pack()

def detail():
    screnn = tkinter.Toplevel(window)

menu = Menu(frame)
first_menu = Menu(menu,tearoff=0)
first_menu.add_command(label="option",command=ex)
first_menu.add_command(label="Detail",command=detail)
menu.add_cascade(label="Menu",menu=first_menu)

window.config(menu=menu)
add_button = Button(frame,font=("calibri",15),width=12,text="Ajouter",bg="skyblue",command=lambda :insert())
add_button.place(x=200,y=80)

del_button = Button(frame,font=("calibri",15),width=12,text="Supprimer",bg="skyblue",command=lambda :delete())
del_button.place(x=200,y=130)

fin_button = Button(window,font=("calibri",15),width=12,text="Terminer",bg="blue",command=lambda :acconplie())
fin_button.place(x=350,y=200)

tree = ttk.Treeview(window,columns=(1,2,3),height=10,show="headings")
tree.place(x=0,y=240, width=500)
tree.heading(1,text="Num")
tree.heading(2,text="Taches")
tree.column(1,width=50)
tree.column(2,width=450)
tree.column(3,width=-6)

def recherche():
    global row
    conn = sqlite3.connect("Todoliste.db")
    cur = conn.cursor()
    re = entry2.get()
    x = 0
    for record in tree.get_children():
        tree.delete(record)
    select = cur.execute("select*from Todo where id=?",(re,))
    for row in select:
        tree.insert('', END, values=(row[0], row[1], row[3]))
        x += 1
    if (x==0):
        messagebox.showinfo("Resultat", "id intouvable")

    conn.commit()
    conn.close()
    print(re)

entry2 = Entry(window,font=("century",10))
entry2.place(x=150,y=210)

search_button = Button(window,font=("calibri",10),width=12,text="Recherche",bg="silver",relief=GROOVE,command=lambda :recherche())
search_button.place(x=30,y=210)

style = ttk.Style()
style.configure("Treeview")

tree.tag_configure("valid1",background="green")
tree.tag_configure("valid2",background="white")
a = "valid1"
b = 0
c = 0
d = 0
conn = sqlite3.connect("Todoliste.db")
cur = conn.cursor()
req = "CREATE TABLE IF NOT EXISTS Todo(id integer auto_increment primary key,tache varchar(1500),v boolean)"
cur.execute(req)
select = cur.execute("select*from Todo where v=true")
for row in select:
    if (row[3]==0):
        a = "valid1"
        b += 1
    else:
        a = "valid2"
        c += 1
    tree.insert('',END,values=(row[0],row[1],row[3]),tags=(a))


barre = Scrollbar(window,bd=2,bg="orange")
barre.pack(side=RIGHT,fill=Y)
barre.config(command=tree.yview)


frame.pack()
window.mainloop()