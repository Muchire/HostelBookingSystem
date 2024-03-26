import sqlite3
from tkinter import *
from tkinter import messagebox


class HostelBookingSystem:
    def __init__(self):
        self.room_var = None
        self.student_id_entry = None
        self.check_in_date_entry = None
        self.dorm_selection_window = None
        self.room_selection_window = None
        self.window = None
        self.main_window = Tk()
        self.main_window.title('WELCOME')
        self.main_window.geometry("400x200")
        Label(self.main_window, text="Welcome to Hostel Booking System").pack()

        self.conn = sqlite3.connect('test1.db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS test1 (
                  name TEXT,
                  student_id TEXT,
                  check_in_date TEXT,
                  dorm_name TEXT,
                  room_no INTEGER
                   )""")

        student_name = Label(self.main_window, text="Student Name:")
        student_name.pack()
        self.name_entry = Entry(self.main_window)
        self.name_entry.pack()

        password_label = Label(self.main_window, text="Password:")
        password_label.pack()
        self.password_entry = Entry(self.main_window, show="*")
        self.password_entry.pack()

        Button(self.main_window, text="Proceed to Booking", command=self.data_entry_page).pack()

        self.dorm_var = StringVar()

        self.c.execute("""CREATE TABLE IF NOT EXISTS rooms (
                  dorm_name TEXT,
                  room_no INTEGER,
                  occupants INTEGER DEFAULT 0
                 )""")

        for dorm in ["Box Ladies' Dorm", "Ladies' Dorm Annex A", "Ladies' Dorm Annex B"]:
            for i in range(1, 20) if dorm == "Box Ladies' Dorm" else range(1, 20) if dorm == "Ladies' Dorm Annex A" else (range(
                    1, 21)):
                self.c.execute("INSERT INTO rooms VALUES (?, ?, 0)", (dorm, i))

        self.conn.commit()
    #
    # def open_booking_window(self):
    #     # Destroy the initial window
    #     self.main_window.destroy()
    #
    #     # Open the booking window
    #     self.data_entry_page()

    def book(self):
        name = self.name_entry.get()
        student_id = self.student_id_entry.get()
        check_in_date = self.check_in_date_entry.get()
        selected_dorm = self.dorm_var.get()
        selected_room = self.room_var.get()

        if not name or not student_id or not check_in_date or not selected_dorm or not selected_room:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        conn = sqlite3.connect('test1.db')
        c = conn.cursor()

        c.execute("SELECT occupants FROM rooms WHERE dorm_name = ? AND room_no = ?", (selected_dorm, selected_room))
        occupants = c.fetchone()[0]
        if occupants >= 4:
            messagebox.showerror("Error", "Room is fully booked.")
            return

        c.execute("INSERT INTO test1 (name, student_id, check_in_date, dorm_name, room_no) VALUES (?, ?, ?, ?, ?)",
                  (name, student_id, check_in_date, selected_dorm, selected_room))

        c.execute("UPDATE rooms SET occupants = occupants + 1 WHERE dorm_name = ? AND room_no = ?",
                  (selected_dorm, selected_room))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Booking successful.")
        self.room_selection_window.destroy()

    def dorm_selection_window(self):

        self.dorm_selection_window = Toplevel(self.main_window)
        self.dorm_selection_window.title('SELECT DORM')
        self.dorm_selection_window.geometry("600x200")

        option_1_frame = Frame(self.dorm_selection_window)
        option_1_frame.pack()
        Radiobutton(option_1_frame, text="Box Ladies' Dorm", variable=self.dorm_var, value="Box Ladies' Dorm").pack()

        option_2_frame = Frame(self.dorm_selection_window)
        option_2_frame.pack()
        Radiobutton(option_2_frame, text="Ladies' Dorm Annex A", variable=self.dorm_var,
                    value="Ladies' Dorm Annex A").pack(
            anchor=W)

        option_3_frame = Frame(self.dorm_selection_window)
        option_3_frame.pack()
        Radiobutton(option_3_frame, text="Ladies' Dorm Annex B", variable=self.dorm_var,
                    value="Ladies' Dorm Annex B").pack(
            anchor=W)

        Button(self.dorm_selection_window, text="Next",
               command=lambda: [self.show_room_selection(), self.dorm_selection_window.destroy()]).pack()

    def show_room_selection(self):
        self.room_selection_window = Toplevel()
        self.room_selection_window.title('SELECT ROOM')
        self.room_selection_window.geometry("600x200")

        selected_dorm = self.dorm_var.get()
        self.room_var = IntVar()
        conn = sqlite3.connect('test1.db')
        c = conn.cursor()

        if selected_dorm == "Box Ladies' Dorm":
            for i in range(1, 20):
                c.execute("SELECT occupants FROM rooms WHERE dorm_name = ? AND room_no = ?", (selected_dorm, i))
                occupants = c.fetchone()[0]
                if occupants < 4:
                    Radiobutton(self.room_selection_window, text=f"Room {i}", variable=self.room_var, value=i).pack(
                        anchor=W)
        elif selected_dorm == "Ladies' Dorm Annex A":
            for i in range(1, 20):
                c.execute("SELECT occupants FROM rooms WHERE dorm_name = ? AND room_no = ?", (selected_dorm, i))
                occupants = c.fetchone()[0]
                if occupants < 4:
                    Radiobutton(self.room_selection_window, text=f"Room {i}", variable=self.room_var, value=i).pack(
                        anchor=W)
        elif selected_dorm == "Ladies' Dorm Annex B":
            for i in range(1, 21):
                c.execute("SELECT occupants FROM rooms WHERE dorm_name = ? AND room_no = ?", (selected_dorm, i))
                occupants = c.fetchone()[0]
                if occupants < 4:
                    Radiobutton(self.room_selection_window, text=f"Room {i}", variable=self.room_var, value=i).pack(
                        anchor=W)

        Button(self.room_selection_window, text="BOOK", command=self.book).pack()

    def data_entry_page(self):

        self.window = Toplevel()
        self.window.title('HOSTEL BOOKING')
        self.window.geometry("400x400")
        self.window.config(background="grey")

        name = Label(self.window, text="NAME")
        name.grid(row=0, column=0)
        self.name_entry = Entry(self.window)
        self.name_entry.grid(row=0, column=1)

        student_id = Label(self.window, text="STUDENT_ID")
        student_id.grid(row=1, column=0)
        self.student_id_entry = Entry(self.window)
        self.student_id_entry.grid(row=1, column=1)

        check_in_date = Label(self.window, text="CHECK_IN_DATE")
        check_in_date.grid(row=2, column=0)
        self.check_in_date_entry = Entry(self.window)
        self.check_in_date_entry.grid(row=2, column=1)

        Button(self.window, text="BOOK", command=self.dorm_selection_window).grid(row=3,column=1)

    def run(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    hostel_booking_system = HostelBookingSystem()
    hostel_booking_system.run()
