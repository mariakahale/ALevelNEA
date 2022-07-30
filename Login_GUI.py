#login_page and register_page section
#GUI section
from tkinter import * #imports tkinter library for GUI
from PIL import ImageTk, Image
from tkinter.font import Font
#imports Validations and Connections python functions
from Login_Validations_and_Connections import *
from Inventory_System_GUI import *

class Login_GUI:

    def __init__(self,parent):
        login_page=Tk() #creates the tkinter root window, from which all the other tkinter components are managed
        self.parent=login_page #creates an instance of the class using the root tkinter window that can be accessed throughout the class

    def create_login_page(self, login_page):
        #initialises main module for login_page window
        self.parent.title("Command Lab - Login") #sets title of the window
        self.parent.iconbitmap("logo.ico") #sets icon of the window
        self.parent.geometry("910x607") #sets size of login_page window as that of background image

        #inserts image in background of main window
        global img
        img=ImageTk.PhotoImage(file='img1.png') #defined the background image
        back_label = Label(login_page, image=img) #created a label for image
        back_label.place(x=0, y=0, relheight=1, relwidth=1) #positioned image at the top left

        #title text
        self.title_font = Font(family = "SF Compact Text", size=42)
        self.title_text = Label(login_page, text="Command Lab", fg="navy blue", font=self.title_font)
        self.title_text.grid(row=0, column=0, padx=(0,150))


    def login_entries(self, login_page):
        #sets title for login frame
        self.login_text_font = Font(family = "SF Compact Display", size = 20)
        self.login_frame = LabelFrame(login_page, text="Login", font=self.login_text_font)
        self.login_frame.grid(row=1, column=1)

        #creates labels for username and password entry boxes
        self.u_name_label = Label(self.login_frame, text="Username")
        self.u_name_label.grid(row=2, column=0, pady=(50,0))
        self.p_name_label = Label(self.login_frame, text = "Password")
        self.p_name_label.grid(row=3, column=0, pady=(50,50))

        #creates text boxes for username and password for login_page 
        self.u_name = Entry(self.login_frame, width=40) #username
        self.u_name.grid(row=2, column=2, pady=(50,0))

        self.p_name = Entry(self.login_frame, width=40) #password
        self.p_name.grid(row=3, column=2, pady=(50,50))

    def login_buttons(self, login_page):
        self.Login_Successful="" #initializes the value of Login_Successful variable as blank. This will then be populated with whether the login was successful, so that the user can open the inventory page.
        
        #creates submit button
        self.submit_button = Button(self.parent, text = "Login", command = lambda: self.Login_Successful == self.submit_login(), padx=20) #this button calls the submit_login function
        self.submit_button.grid(row=3, column=1, pady=(45,15))

        #creates register button
        self.register_button = Button(self.parent, text = "Register", command= self.call_register_page_window, padx=14) #this button calls the register_page_window
        self.register_button.grid(row=4, column=1)

        try:
            self.parent.mainloop() #this encloses the root window's widgets
        except:
            pass

        return  self.Login_Successful
    
    def submit_login(self): #this function is called from the above login button
        try: #if there is an existing error response label, program destroys the label.
            self.Response_Label.destroy()
            self.UsernameResponse_Label.destroy()
        except:
            pass
 
        #this is where the user's input are being checked            
        self.entered_username, self.entered_password = self.get_values() # getting the values in the password and username entries by calling the get_values function
        u2=self.validate_username() #calls the validate username function to see if the user's input is valid and to check whether the username exists

        try: #this part attempts to check the password. If any part of this process fails, including checking validity as well as existence of password, then the login is failed
            u2.salt, u2.hash_key = u2.retrieve_salt_and_hashkey(self.entered_username) #calls and gets the values of the salt and hash key that matches the username entered by the user
            self.Login_Successful = u2.check_entered_password(self.entered_password, u2.salt, u2.hash_key) #compares it with the existing salt and hash key associated with the username in the database

        except:
            self.Login_Successful = False #otherwise, the login fails
        if self.Login_Successful == False: #outputs an appropriate error message
            self.Response_Label = Label(self.login_frame, text="Login Unsuccessful")
            self.Response_Label.grid(row=4,column=0)
            #clears the entries for the username and password
            self.u_name.delete(0,END) 
            self.p_name.delete(0,END)



        self.open_inventory_page(self.Login_Successful) #calls the inventory page function to attempt to launch, based on whether the login was successful

        return self.Login_Successful
    
    def get_values(self): #this function is called to return the values in the username and password entries
        try: 
            self.entered_username =  self.u_name.get()

            self.entered_password = self.p_name.get()
        except: 
            pass
        return self.entered_username, self.entered_password #returns the values of the username and password

    def validate_username(self): #this function is to validate the username
        #creates an instance of the login class in the LOgin_Validations_and_Connections file
        u2=login(self.entered_username, "", "", "", "", self.entered_password) #passes in the values that were returned from the get_values function
        u2.Username_format_valid=u2.check_entered_username(self.entered_username) #calls the check_entered_username function to check the input's validity
        if u2.Username_format_valid == False: 
            self.UsernameResponse_Label = Label(self.login_frame, text="Username invalid") #displays an error message to the user
            self.UsernameResponse_Label.grid(row=5,column=0)

        return u2
        
    def open_inventory_page(self, Login_Successful):
        if self.Login_Successful == True: #checks whether Login_Successful variable is true
            self.teacher_or_technician = self.check_permissions() #gets the value of the teacher_or_technician for the specific user logging in
            self.close_LoginPage()
            u2=Inventory_GUI(self.parent, self.teacher_or_technician)

            u2.configure_GUI()  
            u2.chart_buttons()  
    def check_permissions(self):
        u2=login(self.entered_username, "", "", "", "", "") #creates another instance of the login class, passing in the entered username
        #calls the function check_teacher_or_technician to check whether the user logged in is a teacher or technician
        u2.teacher_or_technician = u2.check_teacher_or_technician (self.entered_username)
        if u2.teacher_or_technician == 0: #if they are a technician, they get access to editing controls of database
            self.edit_permissions=True
        else:
            self.edit_permissions=False #else, teachers have viewing access to the database
        return self.edit_permissions

    def close_LoginPage(self):
        self.parent.withdraw()


    def call_register_page_window(self):
        #clear the page to get ready for registration menu
        self.login_frame.destroy()
        self.u_name_label.destroy()
        self.p_name_label.destroy()
        self.u_name.destroy()
        self.p_name.destroy()
        self.submit_button.destroy()
        self.register_button.destroy()
        new_u1 = Register_GUI(self.parent) #creates an instance of the child class Register GUI

#Register_GUI is the window that allows to register a new user
class Register_GUI(Login_GUI):

    def __init__(self, parent):
        self.parent=parent
        self.registration_entries(self.parent) #calls the function that displays the entries in the registration window
        self.registration_buttons(self.parent) #calls the function that displays the buttons in the registration window

    def registration_entries(self, parent):
        #creates a frame to visually separate different sections
        self.register_text_font = Font(family = "SF Compact Display", size = 20)
        self.register_frame=LabelFrame(self.parent, text="Register New User", font=self.register_text_font)
        self.register_frame.grid(row=1, column=2, pady=(50,0))

        #creates labels for entry optionsself.
        self.email_label = Label(self.register_frame, text="School-Issued Email Address")
        self.email_label.grid(row=1, column=2, pady=(30,0))
        self.password_label = Label(self.register_frame, text="Enter desired password")
        self.password_label.grid(row=2, column=2, pady=(20,0))
        self.password_repeat_label = Label(self.register_frame, text="Enter same password again")
        self.password_repeat_label.grid(row=3, column=2, pady=(20,0))
        self.teacher_or_technician = Label(self.register_frame, text="Please select:")
        self.teacher_or_technician.grid(row=4, column=2, pady=(20,0))

        #creates text boxes for entries
        self.email=Entry(self.register_frame, width=30)
        self.email.grid(row=1, column=3, pady=(30,0))
        self.password=Entry(self.register_frame, width=30)
        self.password.grid(row=2, column=3, pady=(20,0))
        self.password_repeat=Entry(self.register_frame, width=30)
        self.password_repeat.grid(row=3, column=3, pady=(20,0))

        #uses radio buttons for user to select whether teacher or technician
        self.r=IntVar()
        self.r1=Radiobutton(self.register_frame, text="Technician", variable=self.r, value=0)
        self.r1.grid(row=4, column=3, pady=(40,10)) 

        self.r2=Radiobutton(self.register_frame, text="Teacher", variable=self.r, value=1)
        self.r2.grid(row=5, column=3)

    def registration_buttons(self, parent):
        #submit button
        self.register_button = Button(self.parent, text = "Register", command= lambda: self.submit_register(parent), padx=20) #calls the function submit_register when the registration process is called
        self.register_button.grid(row=2, column=2, pady=10)

        self.delete_button = Button(self.parent, text="Delete User", command=self.delete_user_window, padx=20) #this button redirects you to the delete user window
        self.delete_button.grid(row=3, column=2, pady=10)

    def submit_register(self, parent):
        #these are the functions that the button calls, one by one
        self.new_user_email, self.new_user_1_or_0, self.new_user_password, self.new_user_passord_repeat = self.get_values(parent) #calls the function to get the entry values in the child class
        new_u1 = register("", self.new_user_email, self.new_user_1_or_0, self.new_user_password, self.new_user_passord_repeat, "", "") #calls the function to create first instance of register in the Login_Validations_and_Connections file
        self.Email_Format_Valid = new_u1.validate_email(self.new_user_email) #checks whether the formatting of the email entered by the user is valid
        self.Password_Valid = new_u1.validate_password(self.new_user_password, self.new_user_passord_repeat) #checks whether the formatting of the password entered by the user is valid
        if self.Password_Valid and self.Email_Format_Valid == True: #if all entries match formatting...
            self.salt, self.hash_key = new_u1.hash_password(self.new_user_password) #calls hash function to hash the password and stores results in 'salt' and 'hash'
            self.generated_username=new_u1.generate_username(self.new_user_email) #generates username from the user's email by truncating email domain
            self.submission_success=new_u1.submit_to_db() #submits entries to the database
        else:
            self.submission_success=""
            self.error_message(self.Email_Format_Valid, self.Password_Valid, self.submission_success)
        if self.submission_success==True:
            self.registration_complete(self.parent, self.generated_username)
        else:
            pass
        return new_u1
    
    def get_values(self, parent):
        #gets values entered in entry boxes
        self.new_user_email=self.email.get()
        #gets user input on whether new user is a technician or teacher
        self.new_user_1_or_0=self.r.get()
        self.new_user_password=self.password.get()
        self.new_user_passord_repeat=self.password_repeat.get()

        return self.new_user_email, self.new_user_1_or_0, self.new_user_password, self.new_user_passord_repeat


    def error_message(self, Email_Format_Valid, Password_Valid, submission_success): #this function is called to display an appropriate error message based on the error
        if self.Email_Format_Valid == False: #if the email entered has incorrect formatting, then this message is displayed
            self.Email_error_message=Label(self.register_frame, text="Email format invalid", fg="red")
            self.Email_error_message.grid(row=7, column=3)
            self.email.delete(0, END) #clears the email entry

        else:
            try:
                self.Email_error_message.destroy() #if an existing error message exists, then it should be destroyed if the formatting is valid
            except:
                pass
        if self.Password_Valid == False: #if the password entered has incorrect formatting, then this message is displayed
            self.password_error_message=Label(self.register_frame, text="Password too short OR does not match\nPassword must have one lower case, one upper case, \none special character, and one number", fg="red")
            self.password_error_message.grid(row=8, column=2, columnspan=2)
            self.password.delete(0, END)
            self.password_repeat.delete(0,END) #clears the password entry       
        else:
            try:
                self.Password_error_message.destroy() #if an existing error message exists, then it should be destroyed if the formatting is valid
            except:
                pass
        
        if self.submission_success == False: #if the user already exists in the database, this error message is displayed
            self.registration_error_message=Label(self.register_frame, text="User already exists", fg="red")
            self.registration_error_message.grid(row=6, column=3)
        else:
            try:
                self.registration_error_message.destroy() #if an existing error message exists, then it should be destroyed if the formatting is valid
            except:
                pass

    def registration_complete(self, parent, generated_username):
        #clears out window
        self.email_label.destroy()
        self.password_label.destroy()
        self.password_repeat_label.destroy()
        self.teacher_or_technician.destroy()

        self.email.destroy()
        self.password.destroy()
        self.password_repeat.destroy()
        self.r1.destroy()
        self.r2.destroy()

        self.register_button.destroy()

        #registration explanation text
        self.register_text_font = Font(family = "SF Compact Display", size = 10)
        self.register_text = Label(self.register_frame, text = "Registration Complete", font=self.register_text_font)
        self.register_text.grid(row=0, column=0)

        self.text_message= "Username: " + self.generated_username + "\nPassword: "+ self.new_user_password #displays the generated username and password to the user for safekeeping

        self.explanation_text = Label(self.register_frame, text = self.text_message)
        self.explanation_text.grid(row=1, column=3)




    def delete_user_window(self): #this is the window that deletes a user from the database
        def delete():
            user=user_entry.get() #gets the value in the username entry on the delete user window
            u1=Delete_User(user) #creates an instance of the class Delete_User that deletes the user
            self.deletion_successful=u1.delete_record() #deletes the record
            if self.deletion_successful==True:
                deletion_complete = Label(delete_user_page, text = "Deletion Complete")
                deletion_complete.grid(row=3, column=0, pady=(100,0))
            else:
                deletion_complete = Label(delete_user_page, text = "Deletion Failed")
                deletion_complete.grid(row=3, column=0, pady=(100,0))


        delete_user_page = Toplevel() #creates a window that lies above the registration window
        delete_user_page.title("Command Lab - Delete User")
        delete_user_page.iconbitmap("logo.ico")
        delete_user_page.geometry("500x400") #sets size of delete_user_page window as that of background image

        global img2
        img2=ImageTk.PhotoImage(file='img1.png') #defined the background image
        back2_label = Label(delete_user_page, image=img2) #created a label for image
        back2_label.place(x=0, y=0, relheight=1, relwidth=1) #positioned image at the top left

        #title text of delete_user_page
        title_font = Font(family = "SF Compact Text", size=42)
        title_text = Label(delete_user_page, text="Command Lab", fg="navy blue", font=title_font)
        title_text.grid(row=0, column=0, padx=(0,50))

        user_text = Label(delete_user_page, text = "Enter user you wish to delete:")
        user_text.grid(row=1, column=0, pady=(100,0))

        user_entry=Entry(delete_user_page, width=30) #this is the entry in which the user enters which user they wish to delete.
        user_entry.grid(row=2, column=0, pady=(50,0))

        delete_button = Button(delete_user_page, text="Delete User", command=delete, padx=20) #this button calls the delete function above
        delete_button.grid(row=7, column=0, pady=10)

        delete_user_page.mainloop()
