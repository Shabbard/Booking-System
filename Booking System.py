#Booking System

import tkinter as tk
from tkinter import messagebox
import ttkcalendar #taken from https://svn.python.org/projects/sandbox/trunk/ttk-gsoc/samples/ttkcalendar.py
import sqlite3
from sqlite3 import Error
import tkSimpleDialog # taken from https://bugs.python.org/file22286/tkSimpleDialog.py

class Database():

    def __init__(self):

        database = "db.db"
        self.connection = self.Create_Connection(database)
        
        sql_Client_table = """CREATE TABLE IF NOT EXISTS Clients (
            id integer PRIMARY KEY,
            firstname text,
            surname text,
            phonenumber integer UNIQUE
        );"""

        sql_Staff_table = """CREATE TABLE IF NOT EXISTS Staff (
            id integer PRIMARY KEY,
            username text UNIQUE,
            password text
        );"""

        sql_Service_table = """CREATE TABLE IF NOT EXISTS Services (
            id integer PRIMARY KEY,
            service_name text UNIQUE,
            price real
        );"""

        sql_Appointment_table = """CREATE TABLE IF NOT EXISTS Appointments (
            id integer PRIMARY KEY,
            date text,
            start_time text UNIQUE,
            client_id integer,
            service_id integer,
            staff_id integer,
            FOREIGN KEY (client_id) REFERENCES Clients (id),
            FOREIGN KEY (service_id) REFERENCES Services (id),
            FOREIGN KEY (staff_id) REFERENCES Staff (id)
        );"""

        if self.connection is not None:
        
            self.Create_Table(self.connection, sql_Client_table)
            self.Create_Table(self.connection, sql_Staff_table)
            self.Create_Table(self.connection, sql_Appointment_table)
            self.Create_Table(self.connection, sql_Service_table)

    
    def Perform_Function(self, sql, parameter):

            cursor = self.connection.cursor()
            cursor.execute(sql, parameter)         
       
    def Return_Data(self, sql, parameter):

        if parameter != None:

            cursor = self.connection.cursor()
            cursor.execute(sql, parameter)

            data = cursor.fetchall()

            return data

        else:

            cursor = self.connection.cursor()
            cursor.execute(sql)

            data = cursor.fetchall()

            return data
        
    def Create_Connection(self, database):

        try:
            connection  = sqlite3.connect(database)
            return(connection)
        except Error as e:
            print(e)
        return None

    def Create_Table(self, connection, create_table_sql):

        try:
            cursor = connection.cursor()
            cursor.execute(create_table_sql)
        except Error as e:
            print(e)



class MainApplication(tk.Frame):

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        root.title("Main")    
        root.minsize(300, 300)
        root.maxsize(300, 300)
        self.MenuBar(root)
        
    def MenuBar(self, root):

        self.menubar = tk.Menu(root)
        self.staffmenu = tk.Menu(self.menubar, tearoff=0)
        self.staffmenu.add_command(label="Login", command=self.Login)
        self.staffmenu.add_command(label="Add a user", command=self.Add_Staff)
        self.staffmenu.add_command(label="Delete a user", command=self.Delete_Staff)

        self.staffmenu.add_separator()

        self.staffmenu.add_command(label="Search staff availability", command=self.Staff_Availability)
      
        self.staffmenu.add_separator()

        self.staffmenu.add_command(label="Logout", command=self.Logout)
       
        self.menubar.add_cascade(label="Staff", menu=self.staffmenu)

        self.clientmenu = tk.Menu(self.menubar, tearoff=0)
        self.clientmenu.add_command(label="View ", command=self.View_Clients)

        self.menubar.add_cascade(label="Clients", menu=self.clientmenu)

        self.servicemenu = tk.Menu(self.menubar, tearoff=0)
        self.servicemenu.add_command(label="View services", command=self.View_Services)

        self.servicemenu.add_separator()

        self.servicemenu.add_command(label="Add a service", command=self.Add_Service)
        self.servicemenu.add_command(label="Remove a service", command=self.Remove_Service)

        self.menubar.add_cascade(label="Services", menu=self.servicemenu)

        self.appointmentmenu = tk.Menu(self.menubar, tearoff=0)
        self.appointmentmenu.add_command(label="View Calendar", command=self.Show_Calendar)

        self.appointmentmenu.add_separator()

        self.appointmentmenu.add_command(label="Book an appointment", command=self.Book_Appoint)
        self.appointmentmenu.add_command(label="Cancel an appointment", command=self.Cancel_Appointment)

        self.menubar.add_cascade(label="Appointments", menu=self.appointmentmenu)
        
        root.config(menu = self.menubar)
            
    def Login(self):
        LoginGUI(root)

    def Logout(self):

        global LoggedIn

        if LoggedIn == True:
            LoggedIn = False
            messagebox.showinfo("Alert", "You've successfully logged out!")
        else:
            messagebox.showerror("Error", "There is no one logged in...")

    def View_Clients(self):
        ViewClients(root)
        
    def Add_Staff(self):
        AddStaff(root)

    def Delete_Staff(self):
        DeleteStaff(root)
       
    def Show_Calendar(self):
         calendar = Calendar(root)

    def Book_Appoint(self):
        BookAppointment(root)

    def View_Services(self):
        ViewServices(root)
        
    def Add_Service(self):
        AddService(root)

    def Staff_Availability(self):
        StaffAvailability(root)

    def Remove_Service(self):
        RemoveService(root)

    def Cancel_Appointment(self):
        CancelAppointment(root)

class ViewClients(MainApplication):

    def __init__(self, root):

        tk.Frame.__init__(self, root)
        self.Win = tk.Toplevel()
        self.Win.title("View Clients")
        self.Win.minsize(225, 220)
        self.Win.maxsize(225, 220)

        global db

        self.clienttemp = db.Return_Data(""" SELECT DISTINCT surname FROM Clients """, None)
        self.clientdata = tk.StringVar(self.Win)
        self.clientdata.set(self.clienttemp[0])

        self.lstClientList = tk.Listbox(self.Win, width = 50)
        self.lstClientList.pack()

        self.ClientMenu = tk.OptionMenu(self.Win, self.clientdata, *self.clienttemp)
        self.ClientMenu.pack()
        
        self.btnViewEvents = tk.Button(self.Win, text = "View Events", command =self.View_Events)
        self.btnViewEvents.pack()
        

    def View_Events(self):

        Clienttmp = self.clientdata.get()
        Clienttmp1 = Clienttmp[2:]
        Clienttmp = Clienttmp1[:-3]
        lst = []
        lst.append(Clienttmp)

        data = []

        data.append(db.Return_Data(""" SELECT firstname, surname, phonenumber FROM Clients WHERE surname=?""", lst))

        self.lstClientList.delete(0, "end")
        self.lstClientList.insert("end", *data)
        
        

class CancelAppointment(MainApplication):

    def __init__(self, root):

        tk.Frame.__init__(self, root)
        self.Win = tk.Toplevel()
        self.Win.title("Cancel Appointment")
        self.Win.minsize(225, 200)
        self.Win.maxsize(225, 200)

        self.lblDate = tk.Label(self.Win, text = "Date:")
        self.lblTime = tk.Label(self.Win, text = "Time:")

        self.txtDate = tk.Entry(self.Win, state = "readonly")
        self.txtTime = tk.Entry(self.Win, state = "readonly")

        self.btnShowCalendar = tk.Button(self.Win, text = "Show Calendar", command = self.Show_Calendar)
        self.btnShowTimes = tk.Button(self.Win, text = "Show Times", command = self.Show_Times)
        self.btnCancelAppointment = tk.Button(self.Win, text = "Cancel Appointment", command = self.Cancel_Appointment)

        self.lblDate.place(x = 10, y = 10)
        self.lblTime.place(x = 10, y = 50)

        self.txtDate.place(x = 50, y = 10)
        self.txtTime.place(x = 50, y = 50)

        self.btnShowCalendar.place(x = 50, y = 90)
        self.btnCancelAppointment.place(x = 50, y = 130)

    def Show_Calendar(self):

        self.calendar = AppointmentCalendar(self.Win)
        global date

        if date == None:

            messagebox.showerror("Error", "Please choose a date")
            self.Win.focus_force()

        else:

            self.Date = date
            self.txtDate.config(state = "normal")
            self.txtDate.insert(0, self.Date)
            self.txtDate.config(state = "readonly")
            self.btnShowCalendar.place_forget()
            self.btnShowTimes.place(x = 50, y = 100)
        
    def Show_Times(self):

        self.TimeSelect = PickTime(self.Win)
        global time

        if time == "":

            messagebox.showerror("Error", "Please choose a time")
            self.Win.focus_force()

        else:
           
            global date
            parameter = [date, time]
            Time = None

            try:

                Time = db.Return_Data(""" SELECT id FROM Appointments WHERE date=? AND start_time=? """, parameter)

                if Time == []:

                    messagebox.showerror("Error", "That time slot has no appointment.")
                    self.Win.focus.force()
               
            except:

                if Time == None:
            
                    self.Time = time[0][0]
                    self.txtTime.config(state = "normal")
                    self.txtTime.insert(0, self.Time)
                    self.txtTime.config(state = "readonly")
            
    def Cancel_Appointment(self):

        global db

        Date = self.txtDate.get()
        Time = self.txtTime.get()

        if Date == "" or Time == "":

            messagebox.showerror("Error", "Please choose a date and/or time")
            self.Win.focus_force()

        else:

            parameter = [Date, Time]
            db.Perform_Function(""" DELETE FROM Appointments WHERE date=? AND start_time=? """, parameter)



class RemoveService(MainApplication):

    def __init__(self, root):

        tk.Frame.__init__(self, root)
        self.Win = tk.Toplevel()
        self.Win.title("Remove Service")
        self.Win.minsize(225, 80)
        self.Win.maxsize(225, 80)

        global db
        self.servicetemp = db.Return_Data(""" SELECT service_name FROM Services """, None)
        self.servicedata = tk.StringVar(self.Win)
        self.servicedata.set(self.servicetemp[0])

        self.ServiceMenu = tk.OptionMenu(self.Win, self.servicedata , *self.servicetemp)

        self.btnRemoveService = tk.Button(self.Win, text = "Remove Service", command = self.Remove_Service_Click)

        self.ServiceMenu.place(x = 10, y = 10)
        self.btnRemoveService.place(x = 110, y = 12)

    def Remove_Service_Click(self):

        Servicetmp = self.servicedata.get()
        Servicetmp1 = Servicetmp[2:]
        Servicetmp = Servicetmp1[:-3]
        lst = []
        lst.append(Servicetmp)

        global db

        db.Perform_Function(""" DELETE FROM Services WHERE service_name=? """, lst)
        db.connection.commit()


class Calendar(tkSimpleDialog.Dialog):
   
    def body(self, root):
        self.calendar = ttkcalendar.Calendar(root)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection
        if self.result == None:

            messagebox.showerror("Error", "Please choose a date")
            
        else:

            global date 
            date = str(self.result)
            date = date[:-9]
            PickTime(root)

class StaffAvailability(MainApplication):

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.Win = tk.Toplevel()
        self.Win.title("Staff Availability")
        self.Win.minsize(325, 275)
        self.Win.maxsize(325, 275)

        global db

        self.stafftemp = db.Return_Data(""" SELECT username FROM Staff """, None)
        self.staffdata = tk.StringVar(self.Win)
        self.staffdata.set(self.stafftemp[0])

        self.StaffMenu = tk.OptionMenu(self.Win, self.staffdata , *self.stafftemp)
        
        self.btnViewNearEvents = tk.Button(self.Win, text = "View Upcoming Events", command = self.View_Near_Events)
       
        self.NearEvents = tk.Listbox(self.Win, width = 50)
        
        self.StaffMenu.place(x = 10, y = 10)
        self.btnViewNearEvents.place(x = 10, y = 50)

    def View_Near_Events(self):

        global db

        Stafftmp = self.staffdata.get()
        Stafftmp1 = Stafftmp[2:]
        Stafftmp = Stafftmp1[:-3]
        lst = []
        lst.append(Stafftmp)
                
        staffid = db.Return_Data(""" SELECT id FROM Staff WHERE username=? """, lst)
        staffid = staffid[0]

        data = (db.Return_Data(""" SELECT Appointments.start_time, Appointments.date, Clients.firstname as client_firstname, Clients.surname as client_surname
                                        FROM Appointments
                                        JOIN Clients ON Appointments.client_id = Clients.id
                                        WHERE Appointments.staff_id=?
                                        ORDER BY Appointments.date ASC, Appointments.start_time ASC""", staffid))


       
        self.NearEvents.place(x = 0, y = 90)
        self.NearEvents.delete(0, "end")
        self.NearEvents.insert("end", *data)
        
    def ShowCalendar(self):
        AppointmentCalendar(self.Win)

        
class PickStaffTime(tkSimpleDialog.Dialog):

    def body(self, root):

        global db
        global time
        global date
        
        self.lstTimes = tk.Listbox(root, width = 50)
        self.lstTimes.pack()

        data = []
               
        Times = [
            "09:00:00",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
            ]

        for i in range(1,9):

            Times[i] = str((i + 9)) + ":00:00"

        for i in range(9):

            parameter = [Username, date]

            data.append(db.Return_Data(""" SELECT Appointments.start_time, Appointments.date, Clients.firstname as client_firstname, Clients.surname as client_surname, Staff.username as staff_name
                                           FROM Appointments
                                           JOIN Clients ON Appointments.client_id = Clients.id
                                           JOIN Staff ON Appointments.staff_id = Staff.id 
                                           WHERE Staff.username=? AND Appointments.date=?""", parameter))
            
        for i in range(9):

            if data[i] != []:

                Times[i] = data[i]

                        
        self.lstTimes.insert("end", *Times)

    def apply(self):

        time = self.lstTimes.get(self.lstTimes.curselection())
        self.temp = time[0]

        if len(self.temp) > 1:

            messagebox.showerror("Error", "That time slot has already been taken.")
            self.temp = ""
        
        else:

            return self.result
        
        

class ViewServices(MainApplication):
    
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.Win = tk.Toplevel()
        self.Win.title("View Services")
        self.Win.minsize(230, 150)
        self.Win.maxsize(230, 150)

        global db

        data = db.Return_Data(""" SELECT service_name, price FROM Services """, None)

        self.ServiceList = tk.Listbox(self.Win)
        self.ServiceList.pack()

        self.ServiceList.insert("end", *data)

class AddService(MainApplication):

    def __init__(self, root):
        
        tk.Frame.__init__(self, root)
        self.Win = tk.Toplevel()
        self.Win.title("Add Service")
        self.Win.minsize(230, 120)
        self.Win.maxsize(230, 120)

        self.lblServiceName = tk.Label(self.Win, text = "Service Name:")
        self.lblPrice = tk.Label(self.Win, text = "Price:")

        self.txtServiceName = tk.Entry(self.Win)
        self.txtPrice = tk.Entry(self.Win)

        self.btnAddService = tk.Button(self.Win, text = "Add Service", command = self.AddService_Click)

        self.lblServiceName.place(x=10, y=10)
        self.lblPrice.place(x=10, y=50)

        self.txtServiceName.place(x=90, y=10)
        self.txtPrice.place(x = 90, y = 50)

        self.btnAddService.place(x = 80, y = 80)

        self.Win.mainloop

    def AddService_Click(self):

        global db

        ServiceName = self.txtServiceName.get()
        Price = self.txtPrice.get()

        if ServiceName == "" or Price == "":

            messagebox.showerror("Error", "Please enter a service name/price!")
            self.Win.focus_force()

        else:

            Price = "£" + Price

            data = (ServiceName, Price)

            db.Perform_Function(""" INSERT INTO Services(service_name, price) VALUES(?, ?); """, data)
            db.connection.commit()
                


class BookAppointment(MainApplication):

    def __init__(self, root):

         tk.Frame.__init__(self, root)
         self.Date = ""
         
         self.Win = tk.Toplevel()
         self.Win.title("Book Appointment")
         self.Win.minsize(250, 500)
         self.Win.maxsize(250, 500)

         global db
         self.servicetemp = db.Return_Data(""" SELECT service_name FROM Services """, None)
         self.servicedata = tk.StringVar(self.Win)
         self.servicedata.set(self.servicetemp[0])
         
         self.stafftemp = db.Return_Data(""" SELECT username FROM Staff """, None)
         self.staffdata = tk.StringVar(self.Win)
         self.staffdata.set(self.stafftemp[0])

         self.lblFirstname = tk.Label(self.Win, text = "First name:")
         self.lblSurname = tk.Label(self.Win, text = "Surname:")
         self.lblPhoneNum = tk.Label(self.Win, text = "Phone Number:")
         self.lblDate = tk.Label(self.Win, text = "Date:")
         self.lblTime = tk.Label(self.Win, text = "Time:")

         self.txtFirstname = tk.Entry(self.Win)
         self.txtSurname = tk.Entry(self.Win)
         self.txtPhoneNum = tk.Entry(self.Win)
         self.txtDate = tk.Entry(self.Win, state = "readonly")
         self.txtTime = tk.Entry(self.Win, state = "readonly")

         self.btnShowTimes = tk.Button(self.Win, text = "Show Times", command = self.Show_Times)
         self.btnBookAppoint = tk.Button(self.Win, text = "Book Appointment", command = self.BookAppointment__Click)
         self.btnShowCalendar = tk.Button(self.Win, text = "Show Calendar", command = self.Show_Calendar)

         self.ServiceMenu = tk.OptionMenu(self.Win, self.servicedata , *self.servicetemp)
         self.StaffMenu = tk.OptionMenu(self.Win, self.staffdata , *self.stafftemp)
         
         self.lblFirstname.place(x = 10, y = 10)
         self.lblSurname.place(x = 10, y = 50)
         self.lblPhoneNum.place(x = 10, y = 90)
         self.lblDate.place(x = 10, y = 130)
         self.lblTime.place(x = 10, y = 170)

         self.txtFirstname.place(x = 100, y = 10)
         self.txtSurname.place(x = 100, y = 50)
         self.txtPhoneNum.place(x = 100, y = 90)
         self.txtDate.place(x = 100, y = 130)
         self.txtTime.place(x = 100, y = 170)

         self.btnBookAppoint.place(x = 80, y = 400)
         self.btnShowCalendar.place(x = 20, y = 250)
         
         self.StaffMenu.place(x = 20, y = 210)
         self.ServiceMenu.place(x = 120, y = 210)
                  
         self.Win.mainloop

    def Show_Calendar(self):
        
        self.calendar = AppointmentCalendar(self.Win)
        global date

        if date == None:

            messagebox.showerror("Error", "Please choose a date")
            
        else:

            self.Date = date
            self.txtDate.config(state = "normal")
            self.txtDate.insert(0, self.Date)
            self.txtDate.config(state = "readonly")
            self.btnShowCalendar.place_forget()
            self.btnShowTimes.place(x = 20, y = 250)

    def Show_Times(self):

        self.TimeSelect = PickTime(self.Win)
        global time

        if time == "":

            messagebox.showerror("Error", "Please choose a time")
            self.Win.focus_force()

        else:

            temp = time[0]
            if len(temp) > 1:

                messagebox.showerror("Error", "That time slot has already been taken.")
                time = ""

            else:
                self.Time = time
                self.txtTime.config(state = "normal")
                self.txtTime.insert(0, self.Time)
                self.txtTime.config(state = "readonly")

    
    def BookAppointment__Click(self):
               
        global db

        ClientData = [self.txtFirstname.get(), self.txtSurname.get(), self.txtPhoneNum.get()]

        db.Perform_Function(""" INSERT INTO Clients(firstname, surname, phonenumber) VALUES(?, ?, ?); """, ClientData)

        ClientName = [self.txtFirstname.get(), self.txtSurname.get()]
        ClientTemp = db.Return_Data(""" SELECT id FROM Clients WHERE firstname=? AND surname=? """, ClientName)
        ClientID = ClientTemp[0][0]

        Servicetmp = self.servicedata.get()
        Servicetmp1 = Servicetmp[2:]
        Servicetmp = Servicetmp1[:-3]
        lst = []
        lst.append(Servicetmp)
        ServiceTemp = db.Return_Data(""" SELECT id FROM Services WHERE service_name=? """, lst)
        ServiceID = ServiceTemp[0][0]

        Stafftmp = self.staffdata.get()
        Stafftmp1 = Stafftmp[2:]
        Stafftmp = Stafftmp1[:-3]
        lst = []
        lst.append(Stafftmp)
        StaffTemp = db.Return_Data(""" SELECT id FROM Staff WHERE username=? """, lst)
        StaffID = StaffTemp[0][0]

        Date = self.txtDate.get()
        Time = self.txtTime.get()

        if Date == "" or Time == "" or ClientData[0] == "" or ClientData[1] == "" or ClientData[2] == "":

            messagebox.showerror("Error", "Please complete the form before booking.")
            self.Win.focus_force()

        else:

            AppointmentData = [Date, Time, ClientID, ServiceID, StaffID]

            db.Perform_Function(""" INSERT INTO Appointments(date, start_time, client_id, service_id, staff_id) VALUES(?, ?, ?, ?, ?)""", AppointmentData)
            db.connection.commit()
            messagebox.showinfo("Alert", "You have successfully booked an appointment!")

        

class PickTime(tkSimpleDialog.Dialog):

    def body(self, root):

        global db
        global date
        
        self.lstTimes = tk.Listbox(root, width = 50)
        self.lstTimes.pack()

        data = []
               
        Times = [
            "09:00:00",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
            ]

        for i in range(1,9):

            Times[i] = str((i + 9)) + ":00:00"

        for i in range(9):

            parameter = [Times[i], date]

            data.append(db.Return_Data(""" SELECT Appointments.start_time, Clients.firstname as client_firstname, Clients.surname as client_surname, Staff.username as staff_name
                                           FROM Appointments
                                           JOIN Clients ON Appointments.client_id = Clients.id
                                           JOIN Staff ON Appointments.staff_id = Staff.id 
                                           WHERE Appointments.start_time=? AND Appointments.date=?""", parameter))
            
        for i in range(9):

            if data[i] != []:

                Times[i] = data[i]

                        
        self.lstTimes.insert("end", *Times)

    def apply(self):

        try:

            global time
            time = self.lstTimes.get(self.lstTimes.curselection())

        except:
            print("")



class AppointmentCalendar(tkSimpleDialog.Dialog):
       
    def body(self, root):
        self.calendar = ttkcalendar.Calendar(root)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection
        global date
        if self.result == None:

            date = None

        else:

            date = str(self.result)
            date = date[:-9]
      

        
class AddStaff(MainApplication):

     def __init__(self, root):
         tk.Frame.__init__(self, root)
         self.Win = tk.Toplevel()
         self.Win.title("Add Staff")
         self.Win.minsize(210, 120)
         self.Win.maxsize(210, 120)
         self.lblName = tk.Label(self.Win, text = "Name:")
         self.lblPassword = tk.Label(self.Win, text = "Password:")
         self.txtName = tk.Entry(self.Win)
         self.txtPassword = tk.Entry(self.Win)
         self.btnAddStaff = tk.Button(self.Win, text = "Add Staff Member", command = self.AddStaff_Click)
         self.lblName.place(x=10, y=10)
         self.txtName.place(x=70, y=10)
         self.lblPassword.place(x=10, y=50)
         self.txtPassword.place(x = 70, y = 50)
         self.btnAddStaff.place(x = 80, y = 80)
         self.Win.mainloop

     def AddStaff_Click(self):
         global db
         Name = self.txtName.get()
         Password = self.txtPassword.get()

         if Name == "" or Password == "":

             messagebox.showerror("Error", "Please enter a username/password")
             self.Win.focus_force()

         else:

             try:

                data = (Name, Password)
                db.Perform_Function(""" INSERT INTO Staff(username, password) VALUES(?, ?); """, data)
                db.connection.commit()
                messagebox.showinfo("Alert", "You have successfully added a staff member!")
                self.Win.destroy()
         
             except:
                messagebox.showerror("Error", "That Username has been taken!")


class DeleteStaff(MainApplication):

     def __init__(self, root):
         tk.Frame.__init__(self, root)
         self.Win = tk.Toplevel()
         self.Win.title("Delete Staff")
         self.Win.minsize(210, 100)
         self.Win.maxsize(210, 100)
         self.lblName = tk.Label(self.Win, text = "Name:")
         
         global db
         self.stafftemp = db.Return_Data(""" SELECT username FROM Staff """, None)
         self.staffdata = tk.StringVar(self.Win)
         self.staffdata.set(self.stafftemp[0])

         self.StaffMenu = tk.OptionMenu(self.Win, self.staffdata , *self.stafftemp)
                
         self.btnDelStaff = tk.Button(self.Win, text = "Remove Staff Member", command = self.DeleteStaff_Click)
         
         self.StaffMenu.place(x = 10, y= 10)
         self.btnDelStaff.place(x = 10, y = 50)
         self.Win.mainloop

     def DeleteStaff_Click(self):

         global db

         Stafftmp = self.staffdata.get()
         Stafftmp1 = Stafftmp[2:]
         Stafftmp = Stafftmp1[:-3]
                           
         db.Perform_Function("""DELETE FROM Staff WHERE username=? """, [Stafftmp])
                
         db.connection.commit()

         messagebox.showinfo("Alert", "You have successfully deleted a staff member!")
         self.Win.destroy()
 
        

class LoginGUI(MainApplication):

    def __init__(self, root):

        tk.Frame.__init__(self, root)
        self.Win = tk.Toplevel()
        self.Win.title("Login")
        self.Win.minsize(210, 120)
        self.Win.maxsize(210, 120)
        self.lblName = tk.Label(self.Win, text="Name:")
        self.lblPass = tk.Label(self.Win, text="Password:")
        self.txtName = tk.Entry(self.Win)
        self.txtPass = tk.Entry(self.Win, show = "*")
        self.btnLogin = tk.Button(self.Win, text = "Login", command = self.Login_Click)
        self.lblName.place(x=10, y=10)
        self.txtName.place(x=70, y=10)
        self.lblPass.place(x=10, y=50)
        self.txtPass.place(x = 70, y = 50)
        self.btnLogin.place(x = 100, y = 80)
        self.Win.mainloop

    def Login_Click(self):

        Username = self.txtName.get()
        Password = self.txtPass.get()

        if Username == "" or Password == "":

            messagebox.showerror("Error", "Please enter a username/password")
            self.Win.focus_force()

        else:

            temp = db.Return_Data(""" SELECT password FROM Staff WHERE username=? """, [Username])
            dbPass = temp[0][0]
            
            global LoggedIn
        
            if Password == dbPass:

               messagebox.showinfo("Alert", "You've successfully logged in!")
               LoggedIn = True
               self.Win.destroy()

            elif Password != dbPass:

                messagebox.showerror("Error", "That's the wrong password")
                self.Win.focus_force()



if __name__ == "__main__":
    LoggedIn = False
    db = Database()
    date = ""
    time = ""
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()
    db.connection.close()