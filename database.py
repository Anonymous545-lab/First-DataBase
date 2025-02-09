import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# Create database and table
def create_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY, name TEXT, surname TEXT, grade TEXT, amount REAL, phone TEXT)''')
    conn.commit()
    conn.close()

# Insert record
def add_student(name, surname, grade, amount, phone):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, surname, grade, amount, phone) VALUES (?, ?, ?, ?, ?)",
              (name, surname, grade, amount, phone))
    conn.commit()
    conn.close()
    update_total_amount()
    display_students()

# Delete record
def delete_student(student_id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    update_total_amount()
    display_students()

# Display records
def display_students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    rows = c.fetchall()
    conn.close()

    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        # Format amount with Rand symbol
        formatted_row = (row[0], row[1], row[2], row[3], f"R {row[4]:.2f}", row[5])
        tree.insert("", "end", values=formatted_row)

# Update total amount
def update_total_amount():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM students")
    total = c.fetchone()[0]
    conn.close()

    if total is None:
        total = 0.00

    total_amount_label.config(text=f"Total Amount: R {total:.2f}")

# GUI for adding students
def add_student_gui():
    def submit(event=None):
        name = entry_name.get()
        surname = entry_surname.get()
        grade = entry_grade.get()
        amount = entry_amount.get()
        phone = entry_phone.get()
        if name and surname and grade and amount and phone:
            try:
                add_student(name, surname, grade, float(amount), phone)
                messagebox.showinfo("Success", "Student added successfully!")
                entry_name.delete(0, END)
                entry_surname.delete(0, END)
                entry_grade.delete(0, END)
                entry_amount.delete(0, END)
                entry_phone.delete(0, END)
            except ValueError:
                messagebox.showerror("Error", "Amount should be a number.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    def delete_selected_row():
        selected_item = tree.selection()
        if selected_item:
            item_id = tree.item(selected_item)["values"][0]
            delete_student(item_id)
        else:
            messagebox.showwarning("Warning", "No row selected!")

    root = Tk()
    root.title("Student Database")

    # Set default window size
    window_width = 1200
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_right = int(screen_width/2 - window_width/2)
    position_down = int(screen_height/2 - window_height/2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

    # Load background image
    bg_image = Image.open("stars_background.jpg")
    bg_image = bg_image.resize((window_width, window_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a canvas and set the background image
    canvas = Canvas(root, width=window_width, height=window_height)
    canvas.pack(fill='both', expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor='nw')

    # Create a frame to center the widgets with solid background color
    frame = Frame(canvas, bg='white', highlightbackground='grey', highlightthickness=1)
    canvas.create_window(window_width//2, window_height//2, window=frame)

    Label(frame, text="Name:").grid(row=0, column=0, padx=10, pady=5)
    entry_name = Entry(frame)
    entry_name.grid(row=0, column=1, padx=10, pady=5)
    entry_name.bind("<Return>", submit)
    entry_name.bind("<KP_Enter>", submit)

    Label(frame, text="Surname:").grid(row=1, column=0, padx=10, pady=5)
    entry_surname = Entry(frame)
    entry_surname.grid(row=1, column=1, padx=10, pady=5)
    entry_surname.bind("<Return>", submit)
    entry_surname.bind("<KP_Enter>", submit)

    Label(frame, text="Grade:").grid(row=2, column=0, padx=10, pady=5)
    entry_grade = Entry(frame)
    entry_grade.grid(row=2, column=1, padx=10, pady=5)
    entry_grade.bind("<Return>", submit)
    entry_grade.bind("<KP_Enter>", submit)

    Label(frame, text="Amount:").grid(row=3, column=0, padx=10, pady=5)
    entry_amount = Entry(frame)
    entry_amount.grid(row=3, column=1, padx=10, pady=5)
    entry_amount.bind("<Return>", submit)
    entry_amount.bind("<KP_Enter>", submit)

    Label(frame, text="Phone:").grid(row=4, column=0, padx=10, pady=5)
    entry_phone = Entry(frame)
    entry_phone.grid(row=4, column=1, padx=10, pady=5)
    entry_phone.bind("<Return>", submit)
    entry_phone.bind("<KP_Enter>", submit)

    Button(frame, text="Submit", command=submit).grid(row=5, column=0, columnspan=2, pady=10)
    Button(frame, text="Close", command=root.quit).grid(row=6, column=0, columnspan=2, pady=10)
    Button(frame, text="Delete Selected", command=delete_selected_row).grid(row=7, column=0, columnspan=2, pady=10)

    Label(frame, text="Recorded Students:").grid(row=8, column=0, columnspan=2)

    global tree
    columns = ("ID", "Name", "Surname", "Grade", "Amount", "Phone")
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    tree.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

    for col in columns:
        tree.heading(col, text=col, anchor=CENTER)
        tree.column(col, anchor=CENTER, width=100)

    global total_amount_label
    total_amount_label = Label(frame, text="Total Amount: R 0.00", font=('Helvetica', 12, 'bold'))
    total_amount_label.grid(row=10, column=0, columnspan=2, pady=10)

    update_total_amount()
    display_students()

    root.mainloop()

# Create the database and table
create_db()

# Run the GUI
add_student_gui()
