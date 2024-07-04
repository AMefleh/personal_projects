import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import shutil

import db_config_file
import db_functions as db

# Function definitions
def verify_login(username, password):
    try:
        conn = db.open_database()
        cursor = conn.cursor()
        query = "SELECT * FROM login WHERE username = %s AND password =SHA(%s)"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        messagebox.showerror("Login Failed", f"Database error: {str(e)}")
        return None

def login_dialog():
    login_window = tk.Toplevel()
    login_window.title("Login")

    # Labels
    username_label = ttk.Label(login_window, text="Username:")
    username_label.grid(row=0, column=0, padx=10, pady=10)
    password_label = ttk.Label(login_window, text="Password:")
    password_label.grid(row=1, column=0, padx=10, pady=10)

    # Entry widgets for username and password
    username_entry = ttk.Entry(login_window)
    username_entry.grid(row=0, column=1, padx=10, pady=10)
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    # Login button
    login_button = ttk.Button(login_window, text="Login", command=lambda: check_credentials(username_entry.get(), password_entry.get(), login_window))
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

def check_credentials(username, password, window):
    if verify_login(username, password):
        messagebox.showinfo("Login Success", "You are now logged in.")
        window.destroy()
        form.deiconify()  # Show the main window after successful login
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        form.destroy()



# Main application logic, shown after successful login
def main_app():
    tab_parent = ttk.Notebook(form)
    tab1 = ttk.Frame(tab_parent)
    tab2 = ttk.Frame(tab_parent)
    tab3 = ttk.Frame(tab_parent)
    tab4 = ttk.Frame(tab_parent)
    tab_parent.add(tab1, text="All Records")
    tab_parent.add(tab2, text="Add New Record")
    tab_parent.add(tab3, text="Search Records")
    tab_parent.add(tab4, text="Advanced Search Records")
    tab_parent.pack(expand=1, fill="both")

    # Add widgets and logic for each tab here

    # Example widget in tab1
    exit_button = ttk.Button(tab1, text="Exit", command=exit_app)
    exit_button.pack()

    # Call the login dialog before showing the main window
    login_dialog()

# Main program initialization
form = tk.Tk()
form.title("Student Management System")
form.geometry("760x580")
form.withdraw()  # Hide the main window until login is successful

# Start the main application
if __name__ == "__main__":
    main_app()
    form.mainloop()
