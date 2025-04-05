from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class StudentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Result Management System")
        self.root.geometry("1200x600+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # Title
        title = Label(self.root, text="Manage Student Details", font=("times new roman", 20, "bold"), bg="#033054", fg="white")
        title.place(x=10, y=15, width=1180, height=35)

        # Variables
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_course = StringVar()
        self.var_admission_date = StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_pin = StringVar()
        self.var_search = StringVar()

        # Main Frame
        main_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        main_frame.place(x=10, y=55, width=1180, height=530)

        # Labels and Entry Fields - Left Side
        # Row 1
        self.fetch_course()
        Label(main_frame, text="Roll No.", font=("times new roman", 15), bg='white').place(x=20, y=20)
        Entry(main_frame, textvariable=self.var_roll, font=("times new roman", 15), bg='#FFFFD0').place(x=120, y=20, width=200)

        Label(main_frame, text="D.O.B(dd-mm-yyyy)", font=("times new roman", 15), bg='white').place(x=340, y=20)
        Entry(main_frame, textvariable=self.var_dob, font=("times new roman", 15), bg='#FFFFD0').place(x=520, y=20, width=200)

        # Row 2
        Label(main_frame, text="Name", font=("times new roman", 15), bg='white').place(x=20, y=60)
        Entry(main_frame, textvariable=self.var_name, font=("times new roman", 15), bg='#FFFFD0').place(x=120, y=60, width=200)

        Label(main_frame, text="Contact No.", font=("times new roman", 15), bg='white').place(x=340, y=60)
        Entry(main_frame, textvariable=self.var_contact, font=("times new roman", 15), bg='#FFFFD0').place(x=520, y=60, width=200)

        # Row 3
        Label(main_frame, text="Email", font=("times new roman", 15), bg='white').place(x=20, y=100)
        Entry(main_frame, textvariable=self.var_email, font=("times new roman", 15), bg='#FFFFD0').place(x=120, y=100, width=200)

        Label(main_frame, text="Select Course", font=("times new roman", 15), bg='white').place(x=340, y=100)
        combo_course = ttk.Combobox(main_frame, textvariable=self.var_course, font=("times new roman", 15), state='readonly')
        combo_course['values'] = ("Select",)
        combo_course.place(x=520, y=100, width=200)
        combo_course.current(0)

        # Row 4
        Label(main_frame, text="Gender", font=("times new roman", 15), bg='white').place(x=20, y=140)
        combo_gender = ttk.Combobox(main_frame, textvariable=self.var_gender, font=("times new roman", 15), state='readonly')
        combo_gender['values'] = ("Select Gender", "Male", "Female", "Other")
        combo_gender.place(x=120, y=140, width=200)
        combo_gender.current(0)

        Label(main_frame, text="Admission Date", font=("times new roman", 15), bg='white').place(x=340, y=140)
        Entry(main_frame, textvariable=self.var_admission_date, font=("times new roman", 15), bg='#FFFFD0').place(x=520, y=140, width=200)

        # Row 5 - Address Fields
        Label(main_frame, text="State", font=("times new roman", 15), bg='white').place(x=20, y=180)
        Entry(main_frame, textvariable=self.var_state, font=("times new roman", 15), bg='#FFFFD0').place(x=120, y=180, width=150)

        Label(main_frame, text="City", font=("times new roman", 15), bg='white').place(x=280, y=180)
        Entry(main_frame, textvariable=self.var_city, font=("times new roman", 15), bg='#FFFFD0').place(x=320, y=180, width=150)

        Label(main_frame, text="Pin Code", font=("times new roman", 15), bg='white').place(x=480, y=180)
        Entry(main_frame, textvariable=self.var_pin, font=("times new roman", 15), bg='#FFFFD0').place(x=570, y=180, width=150)

        # Address
        Label(main_frame, text="Address", font=("times new roman", 15), bg='white').place(x=20, y=220)
        self.txt_address = Text(main_frame, font=("times new roman", 15), bg='#FFFFD0')
        self.txt_address.place(x=120, y=220, width=600, height=100)

        # Buttons
        btn_frame = Frame(main_frame, bg="white")
        btn_frame.place(x=120, y=340, width=600, height=35)

        save_btn = Button(btn_frame, text='Save', font=("times new roman", 15), bg="#2196f3", fg="white", cursor="hand2", command=self.add)
        save_btn.place(x=0, y=0, width=140, height=35)

        update_btn = Button(btn_frame, text='Update', font=("times new roman", 15), bg="#4caf50", fg="white", cursor="hand2", command=self.update)
        update_btn.place(x=150, y=0, width=140, height=35)

        delete_btn = Button(btn_frame, text='Delete', font=("times new roman", 15), bg="#f44336", fg="white", cursor="hand2", command=self.delete)
        delete_btn.place(x=300, y=0, width=140, height=35)

        clear_btn = Button(btn_frame, text='Clear', font=("times new roman", 15), bg="#607d8b", fg="white", cursor="hand2", command=self.clear)
        clear_btn.place(x=450, y=0, width=140, height=35)

        # Search Frame
        search_frame = Frame(main_frame, bg="white")
        search_frame.place(x=750, y=20, width=400, height=500)

        Label(search_frame, text="Search | Roll No.", font=("times new roman", 15), bg='white').place(x=10, y=10)
        Entry(search_frame, textvariable=self.var_search, font=("times new roman", 15), bg='#FFFFD0').place(x=150, y=10, width=150)
        Button(search_frame, text='Search', font=("times new roman", 15), bg="#2196f3", fg="white", cursor="hand2", command=self.search).place(x=310, y=10, width=80, height=30)

        # Table Frame
        table_frame = Frame(search_frame, bd=2, relief=RIDGE)
        table_frame.place(x=10, y=50, width=380, height=440)

        scrolly = Scrollbar(table_frame, orient=VERTICAL)
        scrollx = Scrollbar(table_frame, orient=HORIZONTAL)

        style = ttk.Style()
        style.configure("mystyle.Treeview", font=('times new roman', 13), rowheight=25)
        style.configure("mystyle.Treeview.Heading", font=('times new roman', 13, "bold"))

        self.StudentTable = ttk.Treeview(table_frame, columns=("roll", "name", "email", "gender", "dob"),
                                      xscrollcommand=scrollx.set, yscrollcommand=scrolly.set, style="mystyle.Treeview")
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.StudentTable.xview)
        scrolly.config(command=self.StudentTable.yview)

        self.StudentTable["columns"] = ("roll", "name", "email", "gender", "dob", "contact", "course", "admission_date", "state", "city", "pin", "address")

        self.StudentTable.heading("roll", text="Roll No.")
        self.StudentTable.heading("name", text="Name")
        self.StudentTable.heading("email", text="Email")
        self.StudentTable.heading("gender", text="Gender")
        self.StudentTable.heading("dob", text="D.O.B")
        self.StudentTable.heading("contact", text="Contact")
        self.StudentTable.heading("course", text="Course")
        self.StudentTable.heading("admission_date", text="Admission Date")
        self.StudentTable.heading("state", text="State")
        self.StudentTable.heading("city", text="City")
        self.StudentTable.heading("pin", text="Pin")
        self.StudentTable.heading("address", text="Address")

# Set table to display only column headings, no row numbering
        self.StudentTable["show"] = 'headings'

# Define column widths for each field
        self.StudentTable.column("roll", width=70)
        self.StudentTable.column("name", width=130)
        self.StudentTable.column("email", width=160)
        self.StudentTable.column("gender", width=90)
        self.StudentTable.column("dob", width=100)
        self.StudentTable.column("contact", width=120)      # Contact column
        self.StudentTable.column("course", width=120)       # Course column
        self.StudentTable.column("admission_date", width=130) # Admission Date column
        self.StudentTable.column("state", width=100)        # State column
        self.StudentTable.column("city", width=100)         # City column
        self.StudentTable.column("pin", width=100)          # Pin column
        self.StudentTable.column("address", width=200)      # Address column

        
        self.StudentTable.pack(fill=BOTH, expand=1)
        self.StudentTable.bind("<ButtonRelease-1>", self.get_data)
        
        self.show()
        self.fetch_course()

    # Database Operations
    def add(self):
        if self.var_roll.get() == "":
            messagebox.showerror("Error", "Roll No. is required", parent=self.root)
        else:
            try:
                con = sqlite3.connect("rms.db")
                cur = con.cursor()
                cur.execute("INSERT INTO student (roll,name,email,gender,dob,contact,course,admission_date,state,city,pin,address) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                          (
                              self.var_roll.get(),
                              self.var_name.get(),
                              self.var_email.get(),
                              self.var_gender.get(),
                              self.var_dob.get(),
                              self.var_contact.get(),
                              self.var_course.get(),
                              self.var_admission_date.get(),
                              self.var_state.get(),
                              self.var_city.get(),
                              self.var_pin.get(),
                              self.txt_address.get("1.0", END)
                          ))
                con.commit()
                messagebox.showinfo("Success", "Student added successfully", parent=self.root)
                self.show()
                con.close()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}")

    def update(self):
        if self.var_roll.get() == "":
            messagebox.showerror("Error", "Roll No. is required", parent=self.root)
        else:
            try:
                con = sqlite3.connect("rms.db")
                cur = con.cursor()
                cur.execute("UPDATE student SET name=?,email=?,gender=?,dob=?,contact=?,course=?,admission_date=?,state=?,city=?,pin=?,address=? WHERE roll=?",
                          (
                              self.var_name.get(),
                              self.var_email.get(),
                              self.var_gender.get(),
                              self.var_dob.get(),
                              self.var_contact.get(),
                              self.var_course.get(),
                              self.var_admission_date.get(),
                              self.var_state.get(),
                              self.var_city.get(),
                              self.var_pin.get(),
                              self.txt_address.get("1.0", END),
                              self.var_roll.get()
                          ))
                con.commit()
                messagebox.showinfo("Success", "Student updated successfully", parent=self.root)
                self.show()
                con.close()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}")

    def delete(self):
        if self.var_roll.get() == "":
            messagebox.showerror("Error", "Roll No. is required", parent=self.root)
        else:
            try:
                con = sqlite3.connect("rms.db")
                cur = con.cursor()
                cur.execute("DELETE FROM student WHERE roll=?", (self.var_roll.get(),))
                con.commit()
                messagebox.showinfo("Success", "Student deleted successfully", parent=self.root)
                self.clear()
                self.show()
                con.close()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}")

    def clear(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select Gender")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_course.set("Select")
        self.var_admission_date.set("")
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.txt_address.delete("1.0", END)
        self.var_search.set("")
        self.show()

    def get_data(self, ev):
        r = self.StudentTable.focus()
        content = self.StudentTable.item(r)
        row = content["values"]
        self.var_roll.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_dob.set(row[4])
        self.var_contact.set(row[5])       # Adding Contact
        self.var_course.set(row[6])        # Adding Course
        self.var_admission_date.set(row[7]) # Adding Admission Date
        self.var_state.set(row[8])         # Adding State
        self.var_city.set(row[9])          # Adding City
        self.var_pin.set(row[10])          # Adding Pin
        self.var_address.set(row[11])      # Adding Address

    def show(self):
     try:
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        cur.execute("SELECT roll, name, email, gender, dob, contact, course, admission_date, state, city, pin, address FROM student")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.StudentTable.delete(*self.StudentTable.get_children())
            for row in rows:
                self.StudentTable.insert("", END, values=row)
        con.close()
     except Exception as ex:
        messagebox.showerror("Error", f"Error due to {str(ex)}")

    def fetch_course(self):
     try:
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("SELECT name FROM course")
        rows = cur.fetchall()
        
        if len(rows) > 0:
            self.course_list = []
            self.course_list.append("Select")
            
            for row in rows:
                self.course_list.append(row[0])
                
            self.var_course.set("Select")
            combo_course = ttk.Combobox(self.root, textvariable=self.var_course, 
                                      values=self.course_list,
                                      font=("times new roman", 15), 
                                      state='readonly')
            combo_course.place(x=532, y=157, width=200)
            combo_course.current(0)
            
     except Exception as ex:
        messagebox.showerror("Error", f"Error due to {str(ex)}")
     finally:
        if con:
            con.close()


    def search(self):
        try:
            con = sqlite3.connect("rms.db")
            cur = con.cursor()
            cur.execute(f"SELECT roll,name,email,gender,dob FROM student WHERE roll=?", (self.var_search.get(),))
            rows = cur.fetchall()
            self.StudentTable.delete(*self.StudentTable.get_children())
            for row in rows:
                self.StudentTable.insert("", END, values=row)
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

if __name__ == "__main__":
    root = Tk()
    obj = StudentClass(root)
    root.mainloop()