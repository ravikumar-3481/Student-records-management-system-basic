import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import os

# ====== CSV FILE SETUP ======
filename = "student_records.csv"
if not os.path.exists(filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Roll", "Course", "Attendance", "Marks", "Photo"])

# ====== FUNCTIONS ======
def load_data():
    tree.delete(*tree.get_children())
    with open(filename, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            tree.insert("", tk.END, values=row)

def add_record():
    record = [name_var.get(), roll_var.get(), class_var.get(), att_var.get(), marks_var.get(), photo_var.get()]
    if "" in record:
        messagebox.showwarning("Missing Data", "Please fill all fields.")
        return

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(record)

    clear_fields()
    load_data()
    messagebox.showinfo("Success", "Record added!")

def select_record(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, "values")
        name_var.set(values[0])
        roll_var.set(values[1])
        course_var.set(values[2])
        att_var.set(values[3])
        marks_var.set(values[4])
        photo_var.set(values[5])

def update_record():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select a record to update")
        return

    updated = [name_var.get(), roll_var.get(), class_var.get(), att_var.get(), marks_var.get(), photo_var.get()]
    with open(filename, "r") as f:
        records = list(csv.reader(f))

    for i, row in enumerate(records):
        if row[1] == tree.item(selected)["values"][1]:  # matching roll no
            records[i] = updated
            break

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(records)

    clear_fields()
    load_data()
    messagebox.showinfo("Updated", "Record updated successfully!")

def delete_record():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select a record to delete")
        return

    roll_no = tree.item(selected)["values"][1]
    with open(filename, "r") as f:
        records = list(csv.reader(f))

    new_records = [records[0]] + [row for row in records[1:] if row[1] != roll_no]

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(new_records)

    clear_fields()
    load_data()
    messagebox.showinfo("Deleted", "Record deleted successfully!")

def clear_fields():
    name_var.set("")
    roll_var.set("")
    course_var.set("")
    att_var.set("")
    marks_var.set("")
    photo_var.set("")

def upload_photo():
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if path:
        photo_var.set(path)

# ====== UI DESIGN ======
root = tk.Tk()
root.title("Advanced Student Records System")
root.geometry("1000x600")
root.resizable(False, False)

# ====== VARIABLES ======
name_var = tk.StringVar()
roll_var = tk.StringVar()
class_var = tk.StringVar()
att_var = tk.StringVar()
marks_var = tk.StringVar()
photo_var = tk.StringVar()

tk.Label(root, text="Student Records Management System", font=("Helvetica", 20, "bold")).pack(pady=10)

form = tk.Frame(root)
form.pack()

fields = [("Name", name_var), ("Roll No", roll_var), ("Course", class_var),
          ("Attendance %", att_var), ("Marks", marks_var), ("Photo Path", photo_var)]

for i, (label, var) in enumerate(fields):
    tk.Label(form, text=label, font=("Arial", 12)).grid(row=i, column=0, sticky="w", padx=10, pady=5)
    tk.Entry(form, textvariable=var, width=40).grid(row=i, column=1, pady=5)
    if label == "Photo Path":
        tk.Button(form, text="Browse", command=upload_photo).grid(row=i, column=2, padx=5)

# ====== BUTTONS ======
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", bg="#4caf50", fg="white", width=15, command=add_record).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Update", bg="#2196f3", fg="white", width=15, command=update_record).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Delete", bg="#f44336", fg="white", width=15, command=delete_record).grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Clear", bg="#9c27b0", fg="white", width=15, command=clear_fields).grid(row=0, column=3, padx=10)

# ====== TREEVIEW TABLE ======
tree_frame = tk.Frame(root)
tree_frame.pack()

columns = ("Name", "Roll", "Course", "Attendance", "Marks", "Photo")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.bind("<ButtonRelease-1>", select_record)
tree.pack()

# Load records on start
load_data()

root.mainloop()
