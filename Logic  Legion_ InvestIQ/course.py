from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # Title
        title = Label(self.root, text="Manage Course Details", font=("goudy old style", 20, "bold"), bg="#033054", fg="white")
        title.place(x=10, y=15, width=1180, height=35)

        # Variables
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_search = StringVar()

        # Labels and Entry Fields
        Label(self.root, text="Course Name", font=("Times new roman", 15, 'bold'), bg='white').place(x=10, y=60)
        self.txt_courseName = Entry(self.root, textvariable=self.var_course, font=("Times new roman", 15, 'bold'), bg='lightyellow')
        self.txt_courseName.place(x=150, y=60, width=200)

        Label(self.root, text="Duration", font=("Times new roman", 15, 'bold'), bg='white').place(x=10, y=100)
        self.txt_duration = Entry(self.root, textvariable=self.var_duration, font=("Times new roman", 15, 'bold'), bg='lightyellow')
        self.txt_duration.place(x=150, y=100, width=200)

        Label(self.root, text="Charges", font=("Times new roman", 15, 'bold'), bg='white').place(x=10, y=140)
        self.txt_charges = Entry(self.root, textvariable=self.var_charges, font=("Times new roman", 15, 'bold'), bg='lightyellow')
        self.txt_charges.place(x=150, y=140, width=200)

        Label(self.root, text="Description", font=("Times new roman", 15, 'bold'), bg='white').place(x=10, y=180)
        self.txt_description = Text(self.root, font=("Times new roman", 15, 'bold'), bg='lightyellow')
        self.txt_description.place(x=150, y=180, width=500, height=130)

        # Buttons
        Button(self.root, text='Save', font=("Times new roman", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.add).place(x=150, y=400, width=110, height=40)
        Button(self.root, text='Update', font=("Times new roman", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2", command=self.update).place(x=270, y=400, width=110, height=40)
        Button(self.root, text='Delete', font=("Times new roman", 15, "bold"), bg="#f44336", fg="white", cursor="hand2", command=self.delete).place(x=390, y=400, width=110, height=40)
        Button(self.root, text='Clear', font=("Times new roman", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2", command=self.clear).place(x=510, y=400, width=110, height=40)

        # Search Panel
        Label(self.root, text="Course Name", font=("Times new roman", 15, 'bold'), bg='white').place(x=720, y=60)
        Entry(self.root, textvariable=self.var_search, font=("Times new roman", 15, 'bold'), bg='lightyellow').place(x=870, y=60, width=180)
        Button(self.root, text='Search', font=("Times new roman", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.search).place(x=1070, y=60, width=120, height=28)

        # Content Frame
        self.c_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        self.c_frame.place(x=720, y=100, width=470, height=340)

        scrolly = Scrollbar(self.c_frame, orient=VERTICAL)
        scrollx = Scrollbar(self.c_frame, orient=HORIZONTAL)

        self.CourseTable = ttk.Treeview(self.c_frame, columns=("cid", "name", "duration", "charges", "description"),
                                        xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)

        self.CourseTable.heading("cid", text="Course ID")
        self.CourseTable.heading("name", text="Name")
        self.CourseTable.heading("duration", text="Duration")
        self.CourseTable.heading("charges", text="Charges")
        self.CourseTable.heading("description", text="Description")
        self.CourseTable["show"] = 'headings'
        self.CourseTable.column("cid", width=100)
        self.CourseTable.column("name", width=100)
        self.CourseTable.column("duration", width=100)
        self.CourseTable.column("charges", width=100)
        self.CourseTable.column("description", width=150)
        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def execute_db_query(self, query, params=()):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        cur.execute(query, params)
        con.commit()
        con.close()

    def add(self):
        if self.var_course.get() == "":
            messagebox.showerror("Error", "Course name is required", parent=self.root)
        else:
            self.execute_db_query("INSERT INTO course (name, duration, charges, description) VALUES (?, ?, ?, ?)", (
                self.var_course.get(),
                self.var_duration.get(),
                self.var_charges.get(),
                self.txt_description.get("1.0", END)
            ))
            messagebox.showinfo("Success", "Course added successfully", parent=self.root)
            self.show()

    def update(self):
        if self.var_course.get() == "":
            messagebox.showerror("Error", "Course name is required", parent=self.root)
        else:
            self.execute_db_query("UPDATE course SET duration=?, charges=?, description=? WHERE name=?", (
                self.var_duration.get(),
                self.var_charges.get(),
                self.txt_description.get("1.0", END),
                self.var_course.get()
            ))
            messagebox.showinfo("Success", "Course updated successfully", parent=self.root)
            self.show()

    def delete(self):
        if self.var_course.get() == "":
            messagebox.showerror("Error", "Course name is required", parent=self.root)
        else:
            self.execute_db_query("DELETE FROM course WHERE name=?", (self.var_course.get(),))
            messagebox.showinfo("Success", "Course deleted successfully", parent=self.root)
            self.show()
            self.clear()

    def clear(self):
        self.show()
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete("1.0", END)
        self.txt_courseName.config(state=NORMAL)

    def get_data(self, event):
        selected_row = self.CourseTable.focus()
        content = self.CourseTable.item(selected_row)
        row = content["values"]
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        self.txt_description.delete("1.0", END)
        self.txt_description.insert(END, row[4])

    def search(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM course WHERE name LIKE ?", ('%' + self.var_search.get() + '%',))
        rows = cur.fetchall()
        con.close()
        self.CourseTable.delete(*self.CourseTable.get_children())
        for row in rows:
            self.CourseTable.insert("", END, values=row)

    def show(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM course")
        rows = cur.fetchall()
        con.close()
        self.CourseTable.delete(*self.CourseTable.get_children())
        for row in rows:
            self.CourseTable.insert("", END, values=row)

if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()
