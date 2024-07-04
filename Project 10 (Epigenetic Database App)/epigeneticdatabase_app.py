import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import db_config_file
import db_functions as db
from PIL import ImageTk, Image
import os
import shutil
from tkinter import filedialog

# global variables declaration
rows = None
num_of_rows = None
row_counter = 0
blank_textboxes_tab_two = True
file_name = "default.png"
path = db_config_file.PHOTO_DIRECTORY + file_name
image_selected = False
image_file_name = None
file_new_home = None
file_to_copy = None

# Function definitions
def on_tab_selected(event):
    global blank_textboxes_tab_two
    selected_tab = event.widget.select()  
    tab_text = event.widget.tab(selected_tab, "text") 
     							                      

    if tab_text == "All Records":
        print("All Records tab selected")
        if blank_textboxes_tab_two == False:
            load_database_results()

    if tab_text == "Add New Record":
        print("Add New Record tab selected") 
                                            
        blank_textboxes_tab_two = True

def forwardButtonClicked():
    print("Forward button clicked!")

def backButtonClicked():
    print("Back button clicked!")

def exitButtonClicked():
    print("Exit button clicked!")
    res = messagebox.askquestion("ask", "Are you sure?")
    if res == 'yes':
        form.destroy()
    else:
        messagebox.showinfo("return", "Returning to main app.")

def load_database_results():
    global rows
    global num_of_rows

    # connect to DB
    try:
        con = db.open_database()
    except (Exception) as e:
        messagebox.showinfo("Database connection error")
        exit()

    messagebox.showinfo("Connection", "DB connection ok")

    # retrieve data from DB
    try:
        sql = "SELECT * FROM students"
        num_of_rows, rows = db.query_database(con, sql, None)
        print("num_of_rows:", num_of_rows)
        print("rows:", rows)

    except db.DatabaseError:
        messagebox.showinfo("Error querying the DB")


    return True

def scroll_forward():
    global rows
    global num_of_rows
    global row_counter

    if row_counter >= (num_of_rows-1):
        messagebox.showinfo("DB error", "End of DB")
    else:
        row_counter = row_counter + 1
        fNameTabOne.set(rows[row_counter][2])
        lNameTabOne.set(rows[row_counter][1])
        idTabOne.set(rows[row_counter][0])

        try:
            if rows[row_counter][7]:
                ph_path = db_config_file.PHOTO_DIRECTORY + rows[row_counter][7]
                load_photo_tab_one(ph_path)
            else:
                load_photo_tab_one(db_config_file.PHOTO_DIRECTORY + "default.png")
        except FileNotFoundError:
            load_photo_tab_one(db_config_file.PHOTO_DIRECTORY + "default.png")

def scroll_backward():
    global rows
    global num_of_rows
    global row_counter

    if row_counter is 0:
        messagebox.showinfo("DB error", "Start of DB")
    else:
        row_counter = row_counter - 1
        fNameTabOne.set(rows[row_counter][2])
        lNameTabOne.set(rows[row_counter][1])
        idTabOne.set(rows[row_counter][0])

        try:
            if rows[row_counter][7]:
                ph_path = db_config_file.PHOTO_DIRECTORY + rows[row_counter][7]
                load_photo_tab_one(ph_path)
            else:
                load_photo_tab_one(db_config_file.PHOTO_DIRECTORY + "default.png")
        except FileNotFoundError:
            load_photo_tab_one(db_config_file.PHOTO_DIRECTORY + "default.png")

def add_new_record():
    global blank_textboxes_tab_two
    global image_file_name
    global file_to_copy
    global file_new_home
    blank_tb_count = 0


    if fNameTabTwo.get() == "":
        blank_tb_count += 1

    if lNameTabTwo.get() == "":
        blank_tb_count += 1

    if gradeTabTwo.get() == "":
        blank_tb_count += 1

    if blank_tb_count > 0:
        blank_textboxes_tab_two = True
        messagebox.showinfo("Database Error", "Blank Text Boxes")
    elif blank_tb_count == 0:
        blank_textboxes_tab_two = False
        if image_selected:
            try:
                shutil.copy(file_to_copy, file_new_home)
            except shutil.SameFileError:
                pass
            try:
                insert_into_database(fNameTabTwo.get(), lNameTabTwo.get(),
                                     gradeTabTwo.get(), image_file_name)
                messagebox.showinfo("Database", "Record added to DB successfully!")
            except Exception as e:
                messagebox.showinfo("Database error", e)
        else:
            messagebox.showinfo("File error", "Please select an image")

def insert_into_database(fName, lName, grade, photo_name):
    try:
        con = db.open_database()
    except Exception as e:
        messagebox.showinfo("Database error", e)
        exit()

    try:
        sql = "INSERT INTO students (first_name, last_name, grade, photo) " \
              "VALUES (%s, %s, %s, %s)"
        vals = (fName, lName, grade, photo_name)
        db.insert_database(con, sql, vals)

    except Exception as e:
        messagebox.showinfo("Error inserting data", e)
        raise db.DatabaseError(e)

def image_path(file_path):
    open_image = Image.open(file_path)
    image = ImageTk.PhotoImage(open_image)
    return image

def load_photo_tab_one(file_path):
    image = image_path(file_path)
    imgLabelTabOne.configure(image=image)
    imgLabelTabOne.image = image

def load_photo_tab_two(file_path):
    image = image_path(file_path)
    imgLabelTabTwo.configure(image=image)
    imgLabelTabTwo.image = image

def select_image():
    global image_selected
    global image_file_name
    global file_new_home
    global file_to_copy

    path_to_image = filedialog.askopenfilename(initialdir='/',
                                               title='Open File',
                                               filetypes=(("PNGs", "*.png"), ("GIFs","*.gif"), ("All files", "*.*")))
    try:
        if path_to_image:
            image_file_name = os.path.basename(path_to_image)
            file_new_home = db_config_file.PHOTO_DIRECTORY + image_file_name
            file_to_copy = path_to_image
            image_selected = True
            load_photo_tab_two(file_to_copy)
    except IOError as err:
        image_selected = False
        messagebox.showinfo("File Error", err)




# Main program=======================================
form = tk.Tk()
form.title("Student Application")
form.geometry("760x580")
tab_parent = ttk.Notebook(form)

# Create/declare two tabs
tab1 = ttk.Frame(form)
tab2 = ttk.Frame(form)
tab3 = ttk.Frame(form)

# Binding the Notebook to function def
tab_parent.bind("<<NotebookTabChanged>>", on_tab_selected)

# Add tabs to tab parent
tab_parent.add(tab1, text="All Records")
tab_parent.add(tab2, text="Add New Record")
tab_parent.add(tab3, text="Search Records")

# Add widgets to tab1
firstLabelTabOne = ttk.Label(tab1, text="First Name")
lastLabelTabOne = ttk.Label(tab1, text="Last Name")
idLabelTabOne = ttk.Label(tab1, text="Student ID")

# Setup StringVars
fNameTabOne = tk.StringVar()
lNameTabOne = tk.StringVar()
idTabOne = tk.StringVar()

firstEntryTabOne = tk.Entry(tab1, textvariable=fNameTabOne)
lastEntryTabOne = tk.Entry(tab1, textvariable=lNameTabOne)
idEntryTabOne = tk.Entry(tab1, textvariable=idTabOne)

imgTabOne = image_path(path)
imgLabelTabOne = tk.Label(tab1, image=imgTabOne)

forwardButtonTabOne = tk.Button(tab1, text="Forward", command=scroll_forward)
backButtonTabOne = tk.Button(tab1, text="Back", command=scroll_backward)
exitButtonTabOne = tk.Button(tab1, text="Exit", command=exitButtonClicked)

firstLabelTabOne.grid(row=0, column=0, padx=15, pady=15)
firstEntryTabOne.grid(row=0, column=1, padx=15, pady=15)
imgLabelTabOne.grid(row=0, column=2, padx=15, pady=15)

lastLabelTabOne.grid(row=1, column=0, padx=15, pady=15)
lastEntryTabOne.grid(row=1, column=1, padx=15, pady=15)

idLabelTabOne.grid(row=2, column=0, padx=15, pady=15)
idEntryTabOne.grid(row=2, column=1, padx=15, pady=15)

backButtonTabOne.grid(row=3, column=0, padx=15, pady=15)
forwardButtonTabOne.grid(row=3, column=1, padx=15, pady=15)
exitButtonTabOne.grid(row=3, column=2, padx=15, pady=15)

# Add widgets to tab2
firstLabelTabTwo = ttk.Label(tab2, text="First Name")
lastLabelTabTwo = ttk.Label(tab2, text="Last Name")
gradeLabelTabTwo = ttk.Label(tab2, text="Grade")

# Setup StringVars
fNameTabTwo = tk.StringVar()
lNameTabTwo = tk.StringVar()
gradeTabTwo = tk.StringVar()

firstEntryTabTwo = tk.Entry(tab2, textvariable=fNameTabTwo, state='normal')
lastEntryTabTwo = tk.Entry(tab2, textvariable=lNameTabTwo, state='normal')
gradeEntryTabTwo = tk.Entry(tab2, textvariable=gradeTabTwo, state='normal')

imgTabTwo = image_path(path)
imgLabelTabTwo = ttk.Label(tab2, image=imgTabTwo)

addRecordButtonTabTwo = tk.Button(tab2, text="Add Record to Database", command=add_new_record)
addNewImageButtonTabTwo = tk.Button(tab2, text="Add Image", command=select_image)

firstLabelTabTwo.grid(row=0, column=0, padx=15, pady=15)
firstEntryTabTwo.grid(row=0, column=1, padx=15, pady=15)
imgLabelTabTwo.grid(row=0, column=2, padx=15, pady=15)

lastLabelTabTwo.grid(row=1, column=0, padx=15, pady=15)
lastEntryTabTwo.grid(row=1, column=1, padx=15, pady=15)

gradeLabelTabTwo.grid(row=2, column=0, padx=15, pady=15)
gradeEntryTabTwo.grid(row=2, column=1, padx=15, pady=15)

addRecordButtonTabTwo.grid(row=3, column=1, padx=15, pady=15)
addNewImageButtonTabTwo.grid(row=3, column=2, padx=15, pady=15)

# Add widgets to tab3
lNameTabThree = tk.StringVar()

lastLabelTabThree = ttk.Label(tab3, text="Enter Last Name")
lastEntryTabThree = tk.Entry(tab3, textvariable=lNameTabThree)

contents = [1,2,3,4,5,6,7,8,9,10,11,12]
optionsVar = tk.IntVar()
optionsVar.set("Select grade")
dropdown = tk.OptionMenu(tab3, optionsVar, *contents)

searchButtonTabThree = tk.Button(tab3, text="Search")

lastLabelTabThree.grid(row=0, column=0, padx=15, pady=15)
lastEntryTabThree.grid(row=0, column=1, padx=15, pady=15)
dropdown.grid(row=0, column=3, padx=15, pady=15)
searchButtonTabThree.grid(row=1, column=3, padx=15, pady=15)

# Connect to DB
success = load_database_results()
if success:
    fNameTabOne.set(rows[0][2])
    lNameTabOne.set(rows[0][1])
    idTabOne.set(rows[0][0])
    photo_path = db_config_file.PHOTO_DIRECTORY + rows[0][7]
    load_photo_tab_one(photo_path)

# Layout of tabs
tab_parent.pack(expand=1, fill="both")
form.mainloop()
