import tkinter as tk
from tkinter import ttk, messagebox


class Student:
    def __init__(self, roll_no, name, subjects):
        self.roll_no = roll_no
        self.name = name
        self.subjects = subjects
        self.marks = [0.0] * len(subjects)

    def set_marks(self, marks):
        if len(marks) != len(self.subjects):
            raise ValueError("Marks count mismatch.")
        for m in marks:
            if m < 0 or m > 100:
                raise ValueError("Marks must be 0-100.")
        self.marks = marks

    def total_marks(self):
        return sum(self.marks)

    def percentage(self):
        return (self.total_marks() / (len(self.subjects) * 100)) * 100

    def grade(self):
        pct = self.percentage()
        if pct >= 90:
            return "A one"
        elif pct >= 80:
            return "A"
        elif pct >= 70:
            return " B"
        elif pct >= 60:
            return "C"
        elif pct>=50:
            return "D"
        else:
            return "F"


class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Marks Manager")
        self.students = {}
        self.subjects = []
        self.setup_subject_entry()

    def clear_root(self):
        for w in self.root.winfo_children():
            w.destroy()

    def setup_subject_entry(self):
        self.clear_root()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Enter 6 Subject Names:", font=("Arial", 14)).pack(pady=10)
        self.subject_entries = []
        for i in range(6):
            subframe = ttk.Frame(frame)
            subframe.pack(pady=5)
            ttk.Label(subframe, text=f"Subject {i+1}: ").pack(side="left")
            e = ttk.Entry(subframe, width=30)
            e.pack(side="left")
            self.subject_entries.append(e)

        ttk.Button(frame, text="Save Subjects", command=self.save_subjects).pack(pady=15)

    def save_subjects(self):
        self.subjects = [e.get().strip() for e in self.subject_entries]
        if any(not s for s in self.subjects):
            messagebox.showerror("Error", "Please enter all 6 subject names.")
            return
        self.setup_main_interface()

    def setup_main_interface(self):
        self.clear_root()
        self.tabControl = ttk.Notebook(self.root)
        self.tabControl.pack(expand=1, fill="both")

        self.tab_add = ttk.Frame(self.tabControl)
        self.tab_update = ttk.Frame(self.tabControl)
        self.tab_display = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab_add, text="Add Student")
        self.tabControl.add(self.tab_update, text="Update Marks")
        self.tabControl.add(self.tab_display, text="Display Students")

        self.setup_add_tab()
        self.setup_update_tab()
        self.setup_display_tab()

        ttk.Button(self.root, text="Exit", command=self.root.destroy).pack(pady=10)

    def setup_add_tab(self):
        frame = self.tab_add
        ttk.Label(frame, text="Add New Student", font=("Arial", 12)).pack(pady=10)

        form = ttk.Frame(frame)
        form.pack(pady=10)

        ttk.Label(form, text="Roll No: ").grid(row=0, column=0, sticky="e")
        self.add_roll_entry = ttk.Entry(form, width=25)
        self.add_roll_entry.grid(row=0, column=1, pady=5)

        ttk.Label(form, text="Name: ").grid(row=1, column=0, sticky="e")
        self.add_name_entry = ttk.Entry(form, width=25)
        self.add_name_entry.grid(row=1, column=1, pady=5)

        self.add_mark_entries = []
        for i, sub in enumerate(self.subjects):
            ttk.Label(form, text=f"{sub}: ").grid(row=2+i, column=0, sticky="e")
            e = ttk.Entry(form, width=10)
            e.grid(row=2+i, column=1, pady=3)
            self.add_mark_entries.append(e)

        ttk.Button(frame, text="Add Student", command=self.add_student).pack(pady=10)

    def add_student(self):
        roll = self.add_roll_entry.get().strip()
        name = self.add_name_entry.get().strip()
        if not roll or not name:
            messagebox.showerror("Error", "Roll number and name required.")
            return
        if roll in self.students:
            messagebox.showerror("Error", f"Roll number {roll} already exists.")
            return

        try:
            marks = [float(e.get()) for e in self.add_mark_entries]
            for m in marks:
                if not (0 <= m <= 100):
                    raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Marks must be numbers between 0 and 100.")
            return

        student = Student(roll, name, self.subjects)
        student.set_marks(marks)
        self.students[roll] = student

        messagebox.showinfo("Success", f"Student {name} added.")
        self.clear_add_form()
        self.refresh_display_tab()

    def clear_add_form(self):
        self.add_roll_entry.delete(0, tk.END)
        self.add_name_entry.delete(0, tk.END)
        for e in self.add_mark_entries:
            e.delete(0, tk.END)

    def setup_update_tab(self):
        frame = self.tab_update
        ttk.Label(frame, text="Update Student Marks", font=("Arial", 12)).pack(pady=10)

        select_frame = ttk.Frame(frame)
        select_frame.pack(pady=5)

        ttk.Label(select_frame, text="Select Roll No: ").pack(side="left")
        self.update_roll_combo = ttk.Combobox(select_frame, values=[], state="readonly")
        self.update_roll_combo.pack(side="left", padx=5)
        self.update_roll_combo.bind("<<ComboboxSelected>>", self.load_student_marks)

        self.update_marks_frame = ttk.Frame(frame)
        self.update_marks_frame.pack(pady=10)

        ttk.Button(frame, text="Update Marks", command=self.update_marks).pack(pady=10)

    def load_student_marks(self, event):
        roll = self.update_roll_combo.get()
        if not roll:
            return
        student = self.students.get(roll)
        if not student:
            return

        for widget in self.update_marks_frame.winfo_children():
            widget.destroy()

        self.update_mark_entries = []
        form = ttk.Frame(self.update_marks_frame)
        form.pack()

        for i, sub in enumerate(self.subjects):
            ttk.Label(form, text=f"{sub}: ").grid(row=i, column=0, sticky="e")
            e = ttk.Entry(form, width=10)
            e.grid(row=i, column=1, pady=2)
            e.insert(0, str(student.marks[i]))
            self.update_mark_entries.append(e)

    def update_marks(self):
        roll = self.update_roll_combo.get()
        if not roll:
            messagebox.showerror("Error", "Select a roll number.")
            return
        student = self.students.get(roll)
        if not student:
            messagebox.showerror("Error", "Student not found.")
            return
        try:
            marks = [float(e.get()) for e in self.update_mark_entries]
            for m in marks:
                if not (0 <= m <= 100):
                    raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Marks must be numbers between 0 and 100.")
            return
        student.set_marks(marks)
        messagebox.showinfo("Success", f"Marks updated for {student.name}.")
        self.refresh_display_tab()

    def setup_display_tab(self):
        frame = self.tab_display
        self.tree = ttk.Treeview(frame,
                                 columns=("Position", "Roll No", "Name", "Total", "Percentage", "Grade"),
                                 show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)

        self.tree.pack(fill="both", expand=True, pady=10)

        self.refresh_display_tab()

    def refresh_display_tab(self):
        # Update update_roll_combo options
        rolls = list(self.students.keys())
        self.update_roll_combo['values'] = rolls

        # Clear tree
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Sort students by total marks descending
        sorted_students = sorted(self.students.values(), key=lambda s: s.total_marks(), reverse=True)

        for i, s in enumerate(sorted_students, start=1):
            self.tree.insert("", "end", values=(
                i,
                s.roll_no,
                s.name,
                f"{s.total_marks():.1f}",
                f"{s.percentage():.2f}%",
                s.grade()
            ))


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()

