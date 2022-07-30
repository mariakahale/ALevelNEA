from tkinter import * #imports tkinter library for GUI
import sqlite3 #imports database SQLite 3 library for SQL functions
import os #library for random number for salt
import hashlib #library for hashing
import re #this imports the regular expression module

#Data Processing    
#using OOP, we will prepare the login_page window below
class Login_Val_and_Conn: #this is the main parent class, which defines the variables that are common to all the children classes
    def __init__(self, username, password, salt, hash_key): #initialises parameters used in the login_page page
        self.username = username
        self.password = password
        self.salt = salt
        self.hash_key = hash_key

class login(Login_Val_and_Conn):
    def __init__(self, username, password, salt, hash_key, new_key, entered_password):
        super().__init__(username, password, salt, hash_key)
        self.new_key=new_key
        self.entered_password=entered_password

    def check_entered_password(self, entered_password, salt, hash_key):

        self.new_key = hashlib.pbkdf2_hmac(
        'sha256',
        self.entered_password.encode('utf-8'), # Convert the password to bytes
        self.salt, #uses the same salt that was passed in
        100000) #repeats the hashing 100,000 times

        if self.new_key == self.hash_key: #if the existing hash key (that was passed in) matches the hash key that the user just entered, then the login was successful
            Login_Successful = True
        else:
            Login_Successful = False

        return Login_Successful

    def check_entered_username(self, username):
        username_format = "^[a-zA-Z0-9\._-]{7,29}$" #ensures that the username format starts with an alphabet. The username can include all other characters, which can be alphabets, numbers or an underscore. The length constraint is {7,29}.

        if re.fullmatch(username_format, self.username): #checks if entered username matches the correct format
            Username_format_valid=True
        else:
            Username_format_valid=False #any other format, including an empty value, would be revoked
            
        return Username_format_valid


    def retrieve_salt_and_hashkey(self, username):
        conn = sqlite3.connect("Command_Lab.db") #creates or connects to the users database or connects to one
        c=conn.cursor() #creates cursor
        #query the database
        c.execute("SELECT salt FROM Users WHERE username=(?)", (self.username,)) #selects the salt that matches the username that was entered
        self.salt= (c.fetchone()[0]) #extracts from the tuple the first record, which can be used for processing later
        conn.commit() #commits changes
        conn.close() #closes connection to database

        conn = sqlite3.connect("Command_Lab.db") #creates or connects to the users database or connects to one
        d=conn.cursor() #creates cursor
        d.execute("SELECT hash_key FROM Users WHERE username=(?)", (self.username,)) #selects the hash key that matches the username that was entered
        self.hash_key= (d.fetchone()[0])
        conn.commit()
        conn.close()
        return self.salt, self.hash_key

    def check_teacher_or_technician(self, username):

        conn = sqlite3.connect("Command_Lab.db") #creates or connects to the users database or connects to one
        c=conn.cursor() #creates cursor
        #query the database
        c.execute("SELECT teacher_or_technician FROM Users WHERE username=(?)", (self.username,))
        self.teacher_or_technician=c.fetchone()[0] #extracts from the tuple the first record, which can be used for processing later
        conn.commit() #commits changes
        conn.close() #closes connection to database

        return self.teacher_or_technician      


class register(Login_Val_and_Conn):
    def __init__(self, username, email, teacher_or_technician, password, password_repeat, salt, hash_key): #initialises parameters used in the login_page page
        super().__init__(username, password, salt, hash_key)
        self.email = email
        self.teacher_or_technician = teacher_or_technician
        self.password_repeat = password_repeat

    def validate_email(self, email): #this subroutine is called to validate the email format

        email_format = "^[a-zA-Z0-9]+[\._]?[a-z0-9A-Z]+_gfs@gemsedu.com$" #ensures that the email format contains the gfs specification as well as the gemsedu (staff-only) domain

        if re.fullmatch(email_format, email): #checks if entered email matches the correct format
            Email_Format_Valid=True
        else:
            Email_Format_Valid=False #any other format, including an empty value, would be revoked
            
        return Email_Format_Valid

    def generate_username(self, email): #this function is called whenever a new username is being generated from the email that was entered
        email_length=len(self.email) #gets the length of the entire email address
        self.username=self.email[0:email_length-12] #truncates the end of the string that corresponds to the school email address
        return self.username

    def validate_password(self, password, password_repeat): #this overrides the validate_password function in the parent class

        password_format="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

        if re.fullmatch(password_format, self.password) and self.password==self.password_repeat: #checks if entered email matches the correct format
            Password_Valid=True
        else:
            Password_Valid=False #any other format, including an empty value, would be revoked
            
        return Password_Valid

    def hash_password(self, password): #for hashing, we will be using a salt as well as a hash key for improved security

        self.salt= os.urandom(32) #os.urandom will output 32 random bytes which will be used as the salt
        #every user will have their own salt, so that the same salt is not used for all users' passwords
        self.hash_key= hashlib.pbkdf2_hmac( #pbkdf2 is a function that derives the hash_key. HMAC will be used as the pseudorandom function.
            "sha256", #this is the hash digest, which states that the hash value will be 256 bits long, irrespective of the size of plaintext
            self.password.encode("utf-8"), #this will covert the password into bytes
            self.salt, #provides the salt
            100000 #100,000 iterations of SHA-256
            )
        return self.salt, self.hash_key


    def submit_to_db(self):

        conn = sqlite3.connect("Command_Lab.db") #creates or connects to the users database or connects to one
        c=conn.cursor() #creates cursor
        try:
            #inserts into table
            c.execute("INSERT INTO Users VALUES (:username, :salt, :hash_key, :email, :teacher_or_technician)",
                    { #through the use of python dictionaries, we are mapping the placeholder variables above to the specific instance
                        "username" : self.username,
                        "salt" : self.salt,
                        "hash_key" : self.hash_key,
                        "email" : self.email,
                        "teacher_or_technician" : self.teacher_or_technician
                    })
            submission_success = True
        except:
            submission_success = False

        conn.commit() #commits changes
        conn.close() #closes connection to database

        return submission_success

class Delete_User(Login_Val_and_Conn):
    def __init__(self, username):
        self.username=username

    def delete_record(self):
        conn = sqlite3.connect("Command_Lab.db") #creates or connects to the users database or connects to one
        c=conn.cursor() #creates cursor
        user_entry=self.username 
        check_to_see_if_username_exists = c.execute("SELECT username from Users WHERE username=(?)", (user_entry,)) #checks to see if a user with that username exists
        if len(check_to_see_if_username_exists.fetchall())==0: #if not, then the function returns false
            deletion_successful=False
        else:
            c.execute("DELETE FROM Users WHERE username = (?)", (user_entry,)) #deletes the record in the database that matches the username that the user entered
            deletion_successful=True


        conn.commit() #commits changes
        conn.close() #closes connection to database
        return deletion_successful