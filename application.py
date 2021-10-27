from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from files import files


#moving the selected rows up
def up():
    rows = my_tree.selection()
    for row in rows:
        my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)
        my_tree.see(row)

#moving the selected rows down
def down():
    rows = my_tree.selection()
    for row in reversed(rows):
        my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)
        my_tree.see(row)

#moving selected rows to top
def top():
    rows = my_tree.selection()
    count = 0
    for row in rows:
        my_tree.move(row, my_tree.parent(row), count)
        my_tree.see(row)
        count += 1

#moving selected rows to bottom
def bottom():
    rows = my_tree.selection()
    count = len(my_tree.get_children()) - 1
    for row in reversed(rows):
        my_tree.move(row, my_tree.parent(row), count)
        my_tree.see(row)
        count -= 1

#populating the tree view with data
def populate_tree():
    data = file_obj.get_pdf_file_names()
    count = 0

    for index,record in enumerate(data):
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(index+1, record), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(index+1, record), tags=('oddrow',))
        count += 1

#merging the pdfs as given in the list
def merge_pdfs():
    if pdf_entry.get() == "":
        messagebox.showerror('Required Field', 'Please Enter Merged File Name')
        return

    pdfs = []
    for node in my_tree.get_children():
        pdfs.append(my_tree.item(node)['values'][1])

    file_obj.merge_pdfs(pdfs, pdf_entry.get())
    messagebox.showinfo('Success','PDFs are Merged Successfully!!')

#Closing the application
def close_application():
    root.quit()
    root.destroy()


# Root of the application
root = Tk()
root.title('Merge Pdf')
root.geometry('500x500')

#Styling the application
style = ttk.Style()

style.theme_use('default')

style.configure("Treeview",
    background="#D3D3D3",
    foreground="black",
    rowheight=25,
    fieldbackground="#D3D3D3")

style.map('Treeview', background=[('selected', '#347083')])

#Creating Tree Frame
tree_frame = Frame(root)
tree_frame.pack(pady=10)

#Creating Scroll bar for Tree Frame
tree_scoll = Scrollbar(tree_frame)
tree_scoll.pack(side=RIGHT, fill=Y)

#Creating the TreeView
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scoll.set, selectmode="extended")
my_tree.pack()

#Configuring Scrollbar
tree_scoll.config(command=my_tree.yview)


#Define Columns
my_tree['columns'] = ("No.", "File Name")

#Formatting Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column('No.', anchor=W, width=12)
my_tree.column('File Name', anchor=W, width=280)

#Formatting Headers
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("No.", text="No.", anchor=W)
my_tree.heading("File Name", text="File Name", anchor=W)


data = ["File 1","File 2"]

my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")


#binding the tree to the release of the left click
my_tree.bind("<ButtonRelease-1>")


#move up button and binding it to the up function
move_up = Button(root, text="Move Up", command=up)
move_up.pack(side='left', padx=30, pady=10)

#move down button and binding it to the down function
move_down = Button(root, text="Move Down", command=down)
move_down.pack(side='left', pady=10)

move_top = Button(root, text="Move Top", command=top)
move_top.pack(side='right', padx=30, pady=10)

move_bottom = Button(root, text="Move Button", command=bottom)
move_bottom.pack(side='right', pady=10)


#Pdf Entry and Label
#pdf_label = Label(root, text='Merged File Name')
pdf_entry = Entry(root)

#pdf_label.pack(pady=10)
pdf_entry.pack(pady=10)


#button to initiate the merge pdf 
merge_pdf = Button(root, text="Merge PDFs", command=merge_pdfs)
merge_pdf.pack(pady=10)


file_obj = files()

#populating tree with data
populate_tree()

#overriding the close button
root.protocol("WM_DELETE_WINDOW", close_application)

#running the application
root.mainloop()
