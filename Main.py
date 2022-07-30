from Login_GUI import *					
from Login_Validations_and_Connections import *	
from Inventory_System_GUI import *

def main(): #the program begins here
	#preparing login window
	login_page=None
	u1=Login_GUI(login_page) #creates an instance of the class Login_GUI under the object u1

	#different aspects of the login window	
	u1.create_login_page(login_page) #configures GUI
	u1.Login_Successful = u1.login_entries(login_page) #places text boxes for login window
	u1.login_buttons(login_page) #places buttons for login window
			
	
if __name__ == "__main__":
	main()


