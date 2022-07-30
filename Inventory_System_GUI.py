from tkinter import * #imports tkinter library for GUI
import sqlite3 #imports database SQLite 3 library for SQL functions
from PIL import ImageTk, Image #imports pillow to be able to handle png image files
from tkinter import ttk #this is used to use treeview, which can be used to visualize the database
from tkinter.font import Font
from Inventory_System_Validations_and_Connections import *
from Experiment_Calculator_GUI import *


class Inventory_GUI:

	def __init__(self, parent, permissions):
		self.parent=parent
		self.inventory_page=Toplevel(self.parent) #creates a top level window over the withdrawn root login window
		self.permissions = permissions #receives the permissions associated with the user that is logged in

	def configure_GUI(self):
		self.inventory_page.title("Command Lab - Inventory Page") #title of window
		self.inventory_page.iconbitmap("logo.ico") #icon of window
		self.inventory_page.geometry("910x607") #size of window

		#inserts image in background of main inventory_page window
		global img
		img=ImageTk.PhotoImage(file='img1.png') #defined the background image
		back_label = Label(self.inventory_page, image=img) #created a label for image
		back_label.place(x=0, y=0, relheight=1, relwidth=1) #positioned image at the top left

		#title text
		self.title_font = Font(family = "SF Compact Text", size=42)
		self.title_text = Label(self.inventory_page, text="Command Lab", fg="navy blue", font=self.title_font)
		self.title_text.grid(row=0, column=0)

		self.openExperiments_Button=Button(self.inventory_page, text="Open experiments", command=self.open_experiments_page) #when the button is pressed, it opens the experiment window
		self.openExperiments_Button.grid(row=0, column=2)

		if self.permissions == True: #only users with the technician permissions can view information about suppliers
			self.checkRestockForSuppliers_Button=Button(self.inventory_page, text="Open suppliers", command=self.open_supplierChart) #when the button is pressed, it opens the supplier window
			self.checkRestockForSuppliers_Button.grid(row=0, column=1)
		else:
			pass

	def create_base_chart(self): #function that creates the treeview to display stock
		self.style=ttk.Style() #initialises style
		self.style.theme_use('default') #uses default ttk style
		
		self.style.configure("Treeview", background="light blue", foreground="black", rowheight=25, fieldbackground="grey")# configures the colors
		self.style.map('Treeview', background=[('selected', "dark blue")]) #uses a python tuple. when we select a record, this is the color that is used
		
		#creating the frame
		self.table_frame = Frame(self.inventory_page) #the table will be in its own frame, which makes adding a scrollbar easier to program
		self.table_frame.grid(row=2, column=1, padx=(30,0))

		self.table_scroll = Scrollbar(self.table_frame) 
		self.table_scroll.pack(fill=Y ,side=RIGHT) # this will allow us to scroll up and down the table

		self.table_tree = ttk.Treeview(self.table_frame, yscrollcommand=self.table_scroll.set, selectmode="extended")
		self.table_tree.pack() #creates the treeview
		
		# Configure the Scrollbar
		self.table_scroll.config(command=self.table_tree.yview)

		return self.table_tree
	
	def run_show_Equipment_Location(self): #this opens the menu for the user to input which location the user wishes to view the inventory for
		self.clear_Everything()

		self.LocationLabel = Label(self.tables_buttons_frame, text="Enter which location you wish to view")
		self.LocationLabel.grid(row=3, column=1, padx=10)
		self.LocationEntry = Entry(self.tables_buttons_frame) #this is the entry to enter the location ID
		self.LocationEntry.grid(row=4, column=1, padx=10)

		self.LocationConfirmButton = Button(self.tables_buttons_frame, text="Submit", command=self.Launch_Equipment_Location) #calls the equipment_location function to launch the table for the stock specific to locations
		self.LocationConfirmButton.grid(row=5, column=1)

		self.LocationWidgetsclearButton=Button(self.tables_buttons_frame, text="Close", command=self.clearLocationWidgets) #closes the menu for the equipment location
		self.LocationWidgetsclearButton.grid(row=6, column=1)

	def Launch_Equipment_Location(self):
		self.LocationConfirm = self.LocationEntry.get() #gets the location ID entered by the user
		self.LocationFormat_Valid=self.validateLocationConfirm() #validates the format of the location by calling validateLocationConfirm in the Inventory_Systems_Validations_and_Connections file

		if self.LocationFormat_Valid==True:
			u1=Equipment_Location(self.inventory_page, self.LocationConfirm, self.permissions) #if it is true, an instance of the class Equipment_location below
			u1.show_Equipment_Location(self.inventory_page, self.LocationConfirm) #calls the function to create the table for the equipment location
		else:
			self.LocationError_Label=Label(self.tables_buttons_frame, text="Invalid Location Format.\nMust be in labs 1-7") #if the formatting is incorrect, an appropriate error message is displayed
			self.LocationError_Label.grid(row=7, column=0)

	def validateLocationConfirm(self):
		u3=Equipment_Location_Validate(self.LocationConfirm,"","","","") #creates an instance of the class Equipment_Location_Validate to validate the format of the location entered by the user
		self.LocationFormat_Valid=u3.validate_Location(self.LocationConfirm)
		return self.LocationFormat_Valid #returns true if the format of the location is valid

	def clearLocationWidgets(self): 
		self.LocationLabel.destroy() #clears all the widgets associated with the Equipment_Location table
		self.LocationEntry.destroy()
		self.LocationConfirmButton.destroy()
		self.LocationWidgetsclearButton.destroy()
		try:
			self.LocationError_Label.destroy() #it will try and delete an error message if one exists
		except:
			pass

	def chart_buttons(self): #this function displays the buttons to call the different tables
		self.tables_buttons_frame = LabelFrame(self.inventory_page) #the table will be in its own frame, which makes adding a scrollbar easier to program
		self.tables_buttons_frame.grid(row=2, column=0)

		self.buttons_explanation = Label(self.tables_buttons_frame, text="Select Table to Display")
		self.buttons_explanation.grid(row=0, column=0, padx=20)

		self.equipment_button = Button(self.tables_buttons_frame, text="Equipment", command = self.run_Equipment_Chart) #when clicked, it calls the function to run the equipment chart
		self.equipment_button.grid(row=1, column=0, pady=10, padx=20)

		self.chemical_button = Button(self.tables_buttons_frame, text="Chemicals", command = self.run_Chemical_Chart) #when clicked, it calls the function to run the chemicals chart
		self.chemical_button.grid(row=2, column=0, pady=10, padx=20)

		self.show_Location_button=Button(self.tables_buttons_frame, text="Equipment Location", command = self.run_show_Equipment_Location) #when clicked, it calls the function to run the equipment location chart
		self.show_Location_button.grid(row=3, column=0, pady=10, padx=20)

		try:
			self.parent.mainloop()
		except:
			pass


	def run_Equipment_Chart(self): #when called, this function creates an instance of the Equipment_Chart child class below
		u1=Equipment_Chart(self.inventory_page, self.permissions, "", self.tables_buttons_frame)
		u1.columns() #columns for the equipment chart table

	def run_Chemical_Chart(self): #when called, this function creates an instance of the Chemical_Chart child class below
		u1=Chemical_Chart(self.inventory_page, self.permissions)	

	def clear_Everything(self):
		#clears any existing Equipment-related widgets
		u1=Equipment_Chart("","","","")
		u1.clear_Equipment_page()

	def open_experiments_page(self): #when called, this function will run the experiments window and withdraw the inventory window
		self.inventory_page.withdraw()
		u1=Experiment_Calculator_Window(self.parent)
		u1.configure_GUI()

	def open_supplierChart(self): #creates an instance of the supplier chart class
		u1=supplier_Chart()


class Equipment_Chart(Inventory_GUI):

	def __init__(self, inventory_page, permissions, LocationConfirm, tables_buttons_frame):
		self.inventory_page=inventory_page
		self.permissions=permissions
		self.LocationConfirm=LocationConfirm
		self.tables_buttons_frame=tables_buttons_frame

		self.table_tree=self.create_base_chart() #calls function from inventory_page class.
		self.columns() #sets the columns for the Equipment table. This will be repeated for all the other required tables.
		self.values=self.connect_db_to_treeview() 
		self.check_permissions_edit_Equipment_Chart() #will run the associated functions that are reserved for users with technician permissions only if true
		self.search_frame() #calls the function that creates the frame for the user to search in the equipment table

		self.stats_button=Button(self.search_frame, text="View equipment stock stats", command=self.view_stock_stats) #this button, when pressed, will call the function that allows the user to view the equipment stock stats based on decreasing number of stock
		self.stats_button.grid(row=0, column=5)

	def columns(self):
		self.table_tree['columns'] = ("Equipment_ID", "Equipment_Name", "Consumable") #sets the titles of the columns in the tree

		#formats the columns
		self.table_tree.column("#0", width=0, stretch=NO)
		self.table_tree.column("Equipment_ID", anchor=CENTER, width=80)
		self.table_tree.column("Equipment_Name", anchor=W, width=210)
		self.table_tree.column("Consumable", anchor=W, width=90)

		#creates headings for the equipment table
		self.table_tree.heading("#0", text="", anchor=W)
		self.table_tree.heading("Equipment_ID", text="Equipment ID", anchor=CENTER)
		self.table_tree.heading("Equipment_Name", text="Equipment Name", anchor=W)
		self.table_tree.heading("Consumable", text="Consumable", anchor=W)

	def connect_db_to_treeview(self):
		u2=Equipment_get_values("", "", "", "","") #creates an instance of the class get_values under the object self
		u2.records = u2.query_Equipment_db() #gets everything from the equipment table
		global count # Add our data to the screen
		count = 0

		#we will alternate the colors of the rows for improved visibility
		self.table_tree.tag_configure('oddrow', background="white")
		self.table_tree.tag_configure('evenrow', background="lightblue")

		for record in u2.records:
			if count % 2 == 0:
				self.table_tree.insert(parent='', index='end', iid=count, text='', values=(record[2], record[0], record[1]), tags=('evenrow',)) #passes in the values that were brought over from the database to populate the treeview
			else:
				self.table_tree.insert(parent='', index='end', iid=count, text='', values=(record[2], record[0], record[1]), tags=('oddrow',))
			
			# increment counter
			count += 1

		self.selected = self.table_tree.focus()# record Number
		self.values = self.table_tree.item(self.selected, 'values')# record values

		return self.values

	def search_frame(self):
		# Create label frame
		self.search_frame = LabelFrame(self.inventory_page, text="Search")
		self.search_frame.grid(row=4,column=1, pady=10)

		# Add entry box
		self.search_entry = Entry(self.search_frame)
		self.search_entry.grid(row=0, column=0, pady=20, padx=20)

		# Add button
		self.search_button = Button(self.search_frame, text="Search Equipment", command=self.search_Equipment_Chart)
		self.search_button.grid(row=0, column=1, padx=20, pady=20)

		self.searchByScience_Button=Button(self.search_frame, text="Search by Science", command=self.search_by_science)
		self.searchByScience_Button.grid(row=1, column=1, padx=20, pady=20) #this button allows you to filter the equipment table to equipment by science
		
		self.ScienceOptions= StringVar(self.search_frame) #this is a dropdown menu to filter by science
		self.ScienceOptions.set("*Select Science*")
		self.ScienceArray=["Physics", "Biology", "Chemistry"]
		self.searchScience_Menu=OptionMenu(self.search_frame, self.ScienceOptions, *self.ScienceArray)
		self.searchScience_Menu.grid(row=1, column=0)

	def get_selected_science(self): #returns the numerical value associated with the selection of the user from the dropdown menu
		self.Selected_Science=self.ScienceOptions.get()
		if self.Selected_Science=="Physics":
			self.Selected_Science=1
		elif self.Selected_Science=="Chemistry":
			self.Selected_Science=2
		else: self.Selected_Science=3

		return self.Selected_Science

	def search_by_science(self):
		self.Selected_Science=self.get_selected_science()

		u3=Equipment_get_values("", "", "", "", self.Selected_Science) #creates an instance of the class get_values under the object self
		u3.records = u3.search_by_science_table(self.Selected_Science) #gets the equipment properties that match the selected science
		self.science_columns()
		# Clears the Treeview from any existing records
		for record in self.table_tree.get_children():
			self.table_tree.delete(record)
		
		global count 
		count = 0

		#we will alternate the colors of the rows for improved visibility
		self.table_tree.tag_configure('oddrow', background="white")
		self.table_tree.tag_configure('evenrow', background="lightblue")
		for record in u3.records:
			if count % 2 == 0:
				self.table_tree.insert(parent='', index='end',  text='', values=(record[0], record[1], record[2]), tags=('evenrow',))
			else:
				self.table_tree.insert(parent='', index='end',  text='', values=(record[0], record[1], record[2]), tags=('oddrow',))
			
			# increment counter
			count += 1

	def science_columns(self):
		self.table_tree['columns'] = ("Equipment_Name", "Science", "Consumable") #sets the titles of the columns in the tree

		#formats the columns
		self.table_tree.column("#0", width=0, stretch=NO)
		self.table_tree.column("Equipment_Name", anchor=CENTER, width=230)
		self.table_tree.column("Science", anchor=W, width=50)
		self.table_tree.column("Consumable", anchor=W, width=90)

		#creates headings for the equipment table
		self.table_tree.heading("#0", text="", anchor=W)
		self.table_tree.heading("Equipment_Name", text="Equipment Name", anchor=CENTER)
		self.table_tree.heading("Science", text="Science", anchor=W)
		self.table_tree.heading("Consumable", text="Consumable", anchor=W)

	def search_Equipment_Chart(self):
		self.EquipmentName_Lookup = self.search_entry.get() #gets the value that was entered by the user to search for the equipment
		self.search_entry.delete(0, END) #clears it

		# Clear the Treeview
		for record in self.table_tree.get_children():
			self.table_tree.delete(record)

		u2=Equipment_get_values(self.EquipmentName_Lookup, "", "", "","") #creates an instance of the class get_values under the object self
		u2.records = u2.search_Equipment_db() #gets everything from the equipment table

		global count # Add our data to the screen that matches the searched entry
		count = 0
		
		for record in u2.records:
			if count % 2 == 0:
				self.table_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]), tags=('evenrow',))
			else:
				self.table_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]), tags=('oddrow',))

	def check_permissions_edit_Equipment_Chart(self): 
		if self.permissions == True:
			self = edit_Equipment_Chart(self.inventory_page, self.table_tree, self.values) #creates an instance of the edit_Equipment_Chart only if the permissions of the user that is logged in allows it
			
		else:
			pass

	def clear_Equipment_page(self):
		try:
			#deletes all the buttons
			self.updateButton.destroy()
			self.newrecordButton.destroy()
			self.deleterecordButton.destroy()
			self.edit_button_frame.destroy()
			#deletes the record frame
			self.EquipmentID_Label.destroy()
			self.EquipmentID_Entry.destroy()
			self.EquipmentName_Label.destroy()
			self.EquipmentName_Entry.destroy()
			self.Consumable_Label.destroy()
			self.Consumable_Entry.destroy()
			self.data_frame.destroy()
		except:
			pass
		try:
			#deletes the search frame
			self.search_entry.destroy()
			self.search_button.destroy()
			self.search_frame.destroy()
		except:
			pass

	def view_stock_stats(self): #this function outputs the equipment statistics in order of decreasing stock
		self.EquipmentStatsText=""
		u3=Location_get_values("","","","","")
		u3.stats=u3.get_equipment_stats()
		self.top_window=Toplevel()
		self.top_window.geometry("607x307")
		self.top_window.title("Equipment Stats")
		self.stats_frame=Frame(self.top_window)
		self.stats_frame.grid(row=2, column=0)
		self.table_scroll = Scrollbar(self.stats_frame, orient='horizontal')
		self.table_scroll.pack(fill=X ,side=BOTTOM ) # this will allow us to scroll up and down the table

		for i in range (len(u3.stats)-1,0,-1):
			self.EquipmentStatsText=self.EquipmentStatsText+str(u3.stats[i])+"\n"
		self.explanationtext=Label(self.stats_frame, text="These values below include all the equipment in order of decreasing stock. \nEquipment with large stocks may mean you can consider distributing them in several storage locations to accomodate them\n"+self.EquipmentStatsText)
		self.explanationtext.pack()


class supplier_Chart(Inventory_GUI):
	def __init__(self):
		self.supplier_window=Toplevel()
		self.supplier_window.geometry("900x500")
		self.supplier_window.title("Suppliers") #creates the suppliers window
		self.configure_GUI()

	def configure_GUI(self):
		#title text
		self.title_font = Font(family = "SF Compact Text", size=42)
		self.title_text = Label(self.supplier_window, text="Command Lab", fg="navy blue", font=self.title_font) 
		self.title_text.grid(row=0, column=0)

		self.stockEntry_Label=Label(self.supplier_window, text="Enter threshold stock")
		self.stockEntry_Label.grid(row=1, column=0)
		self.stock_Entry=Entry(self.supplier_window) #this is the entry to enter the stock that the user wishes to see for equipment below this stock threshold
		self.stock_Entry.grid(row=1, column=1)

		self.submit_StockEntry_Button=Button(self.supplier_window, text="Submit", command=self.Populate_EquipmentSupplier_Chart) #calls the Populate_EquipmentSupplier_Chart function when pressed
		self.submit_StockEntry_Button.grid(row=1, column=2)

		self.create_base_chart() #creates the treeview for the supplier chart
		self.Equipment_supplier_columns() #sets the columns for the supplier table
		self.add_Supplier() #calls the function to allow the user to add new suppliers to the table

	def create_base_chart(self):
		self.style=ttk.Style() #initialises style
		self.style.theme_use('default') #uses default ttk style
		
		self.style.configure("Treeview", background="light blue", foreground="black", rowheight=25, fieldbackground="grey")# configures the colors
		self.style.map('Treeview', background=[('selected', "dark blue")]) #uses a python tuple. when we select a record, this is the color that is used
		
		#creating the frame
		self.table_frame = Frame(self.supplier_window) #the table will be in its own frame, which makes adding a scrollbar easier to program
		self.table_frame.grid(row=2, column=0, columnspan=2, padx=(30,0))

		self.table_scroll = Scrollbar(self.table_frame)
		self.table_scroll.pack(fill=Y ,side=RIGHT) # this will allow us to scroll up and down the table

		self.supplier_table_tree = ttk.Treeview(self.table_frame, yscrollcommand=self.table_scroll.set, selectmode="extended")
		self.supplier_table_tree.pack() #creates the treeview
		
		# Configure the Scrollbar
		self.table_scroll.config(command=self.supplier_table_tree.yview)

		return self.supplier_table_tree

	def Equipment_supplier_columns(self):
		self.supplier_table_tree['columns'] = ("Equipment_Name", "Supplier_Email", "Equipment_Stock") #sets the titles of the columns in the tree

		#formatting the columns
		self.supplier_table_tree.column("#0", width=0, stretch=NO)
		self.supplier_table_tree.column("Equipment_Name", anchor=CENTER, width=150)
		self.supplier_table_tree.column("Supplier_Email", anchor=W, width=150)
		self.supplier_table_tree.column("Equipment_Stock", anchor=W, width=150)


		#creates headings for the treeview
		self.supplier_table_tree.heading("#0", text="", anchor=W)
		self.supplier_table_tree.heading("Equipment_Name", text="Equipment Name", anchor=CENTER)
		self.supplier_table_tree.heading("Supplier_Email", text="Supplier", anchor=W)
		self.supplier_table_tree.heading("Equipment_Stock", text="Equipment Stock", anchor=W)


	def Populate_EquipmentSupplier_Chart(self):
		self.Requested_Stock=self.stock_Entry.get() #gets the value for the entered threshold stock

		u1=Supplier(self.Requested_Stock,"","","") #creates an instance of the class Supplier in the Inventory_System_Validations_and_Connections file
		self.EquipmentStock_format_valid=u1.validate_Requested_Stock(self.Requested_Stock) #calls the function that validates whether the stock format is valid
		if self.EquipmentStock_format_valid==True:
			u1.records=u1.select_Supplies(self.Requested_Stock)

			global count #populates the treeview
			count = 0
			
			for record in u1.records:
				if count % 2 == 0:
					self.supplier_table_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]), tags=('evenrow',))
				else:
					self.supplier_table_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]), tags=('oddrow',))
				count+=1
		else:
			self.errorLabel=Label(self.supplier_window, text="Invalid stock input") #if the formatting is incorrect, an appropriate error message is displayed
			self.errorLabel.grid(row=3, column=0)

	def add_Supplier(self):
		#frame for adding a new supplier's details to the table
		self.SupplierFrame=LabelFrame(self.supplier_window, text="Suppliers")
		self.SupplierFrame.grid(row=4, column=0, columnspan=2)

		self.SupplierEmail_Label=Label(self.SupplierFrame, text="Supplier email")
		self.SupplierEmail_Label.grid(row=0, column=0)
		self.SupplierEmail_Entry=Entry(self.SupplierFrame)
		self.SupplierEmail_Entry.grid(row=0, column=1)

		self.EquipmentID_Label=Label(self.SupplierFrame, text="Equipment ID") #equipment associated with the new supplier
		self.EquipmentID_Label.grid(row=0, column=2)
		self.EquipmentID_Entry=Entry(self.SupplierFrame)
		self.EquipmentID_Entry.grid(row=0, column=3)

		self.SupplierName_Label=Label(self.SupplierFrame, text="Supplier Name")
		self.SupplierName_Label.grid(row=0, column=4)
		self.SupplierName_Entry=Entry(self.SupplierFrame)
		self.SupplierName_Entry.grid(row=0, column=5)	

		self.Submit_NewSupplier_Button=Button(self.SupplierFrame, text="Submit new Supplier and Corresponding Equipment", command=self.Submit_New_Supplier)
		self.Submit_NewSupplier_Button.grid(row=1, column=0)

	def Submit_New_Supplier(self):
		self.Entered_SupplierEmail=self.SupplierEmail_Entry.get()
		self.Entered_EquipmentID=self.EquipmentID_Entry.get()
		self.Entered_SupplierName=self.SupplierEmail_Entry.get()
		u1=Supplier("",self.Entered_SupplierEmail, self.Entered_EquipmentID, self.Entered_SupplierName)
		self.SupplierEmail_Format_Valid=u1.validate_supplier_email(self.Entered_SupplierEmail) #validates the format of the supplier's email
		self.EquipmentID_Valid=u1.validate_equipmentID(self.Entered_EquipmentID) #validates the format of the equipment ID
		self.SupplierName_Valid=u1.validate_SupplierName(self.Entered_SupplierName) #validates the format of the supplier's name

		if self.SupplierEmail_Format_Valid==True and self.EquipmentID_Valid==True and self.SupplierName_Valid==True:
			u1.insert_new_Supplier(self.Entered_SupplierEmail, self.Entered_EquipmentID,self.Entered_SupplierName) #calls the function to insert the validated values to the database
			self.Supplier_errorLabel=Label(self.supplier_window, text="Supplier Added!")
			self.Supplier_errorLabel.grid(row=6, column=0)

			# Clear The Treeview Table
			self.supplier_table_tree.delete(*self.supplier_table_tree.get_children())

			# Run to pull data from database on start
			self.Populate_EquipmentSupplier_Chart()

		else:
			self.Supplier_errorLabel=Label(self.supplier_window, text="Invalid supplier info") #if the formatting is incorrect, an appropriate error message is displayed
			self.Supplier_errorLabel.grid(row=6, column=0)


class edit_Equipment_Chart(Equipment_Chart):
	def __init__(self, inventory_page, table_tree, values):
		self.values=values
		self.table_tree=table_tree
		self.inventory_page=inventory_page
		self.record_entries()
		self.edit_table_buttons()

	def edit_table_buttons(self): #displays the buttons that edit the equipment records
		self.edit_button_frame = LabelFrame(self.inventory_page, text="Commands")
		self.edit_button_frame.grid(row=4, column=0)

		self.updateButton = Button(self.edit_button_frame, text="Update Record", command=self.update_record) #calls the function to update existing record
		self.updateButton.grid(row=0, column=0, padx=10, pady=10)

		self.newrecordButton = Button(self.edit_button_frame, text="New Equipment", command=self.add_record) #calls the function to add a new equipment
		self.newrecordButton.grid(row=0, column=1, padx=10, pady=10)

		self.deleterecordButton = Button(self.edit_button_frame, text="Delete Equipment", command=self.delete_record) #calls the function to delete the record
		self.deleterecordButton.grid(row=0, column=2, padx=10, pady=10)

		self.errorLabel = Label(self.edit_button_frame) 
		self.errorLabel.grid(row=1, column=0)

	def record_entries(self):
		#creates frame to hold entries for records
		self.data_frame = LabelFrame(self.inventory_page, text="Record")
		self.data_frame.grid(row=3, column=0, columnspan=5, padx=20, pady=20, ipadx=100)

		self.EquipmentID_Label = Label(self.data_frame, text="Equipment ID")
		self.EquipmentID_Label.grid(row=0, column=0, padx=10, pady=10)
		self.EquipmentID_Entry = Entry(self.data_frame, width=7) #entry for the equipment ID
		self.EquipmentID_Entry.grid(row=0, column=1, padx=10, pady=10)

		self.EquipmentName_Label = Label(self.data_frame, text="Equipment Name")
		self.EquipmentName_Label.grid(row=0, column=2, padx=10, pady=10)
		self.EquipmentName_Entry = Entry(self.data_frame, width=30) #entry for the equipment name
		self.EquipmentName_Entry.grid(row=0, column=3, padx=10, pady=10)

		self.Consumable_Label = Label(self.data_frame, text="Consumable")
		self.Consumable_Label.grid(row=0, column=4, padx=10, pady=10)
		self.Consumable_Entry = Entry(self.data_frame, width=7) #entry for the consumable variable value
		self.Consumable_Entry.grid(row=0, column=5, padx=10, pady=10)

		self.table_tree.bind("<ButtonRelease-1>", self.select_record) #whenever the user clicks on a row in the treeview, it will call the function select_record
	
	def clear_entries(self):
		# Clear entry boxes
		self.EquipmentID_Entry.delete(0, END)
		self.EquipmentName_Entry.delete(0, END)
		self.Consumable_Entry.delete(0, END)
	
	# Select Record
	def select_record(self, event):

		self.selected = self.table_tree.focus()# record Number
		self.values = self.table_tree.item(self.selected, 'values')# record values

		self.clear_entries()
		# outputs to entry boxes
		self.EquipmentID_Entry.insert(0, self.values[0])
		self.EquipmentName_Entry.insert(0, self.values[1])
		self.Consumable_Entry.insert(0, self.values[2])

	def update_record(self):

		self.selected = self.table_tree.focus() #grabs the record number from the selected line on the treeview

		#gets the values in the entries
		self.Entered_EquipmentName = self.EquipmentName_Entry.get()
		self.Entered_Consumable = self.Consumable_Entry.get()
		self.Entered_EquipmentID = self.EquipmentID_Entry.get()


		u2=Equipment_Location_Validate("",self.Entered_EquipmentName,"",self.Entered_Consumable,"")
		self.equipmentName_format_valid=u2.validate_EquipmentName(self.Entered_EquipmentName) #validates the entered equipment name
		self.Consumable_format_valid=u2.validate_Consumable(self.Entered_Consumable) #validates the entered consumable variable 
		if self.equipmentName_format_valid==True and self.Consumable_format_valid==True:
			u2=Equipment_get_values("", self.Entered_EquipmentName, self.Entered_Consumable, self.Entered_EquipmentID,"") #creates an instance of the class get_values under the object self
			u2.update_Equipment_db() #gets everything from the equipment table
			self.table_tree.item(self.selected, text="", values=(self.EquipmentID_Entry.get(), self.EquipmentName_Entry.get(), self.Consumable_Entry.get(),)) # Update record

		else:
			self.errorLabel.configure(text="Invalid input")

	def add_record(self):
		self.Entered_EquipmentName = self.EquipmentName_Entry.get()
		self.Entered_Consumable = self.Consumable_Entry.get()

		u2=Equipment_Location_Validate("",self.Entered_EquipmentName,"",self.Entered_Consumable,"")
		self.equipmentName_format_valid=u2.validate_EquipmentName(self.Entered_EquipmentName) #validates the entered equipment name
		self.Consumable_format_valid=u2.validate_Consumable(self.Entered_Consumable) #validates the entered consumable variable 

		if self.equipmentName_format_valid==True and self.Consumable_format_valid==True:
			u2=Equipment_get_values("", self.Entered_EquipmentName, self.Entered_Consumable, "","")
			u2.add_Equipment_db() #if the entered values are valid, they are added to the database
		else:
			self.errorLabel.configure(text="Invalid input")
		#clears entries
		self.clear_entries()

		# Clear The Treeview Table
		self.table_tree.delete(*self.table_tree.get_children())

		# Run to pull data from database on start
		self.connect_db_to_treeview()


	def delete_record(self):
		#deletes the record from the selected record in the treeview
		self.x = self.table_tree.selection()[0]
		self.table_tree.delete(self.x)
		
		self.Entered_EquipmentID = self.EquipmentID_Entry.get()		
		u2=Equipment_get_values("", "", "", self.Entered_EquipmentID,"")
		u2.delete_Equipment_db()

		# Clear The Entry Boxes
		self.clear_entries()


class Equipment_Location(Inventory_GUI):

	def __init__(self, inventory_page, LocationConfirm, permissions):
		self.LocationConfirm=LocationConfirm
		self.inventory_page=inventory_page
		self.permissions=permissions
		self.table_tree=self.create_base_chart() #calls function from parent class.

		if self.permissions == True:
			self.record_entries()
			self.edit_table_buttons()
		else:
			pass

	def show_Equipment_Location(self, inventory_page, LocationConfirm):

		#new columns
		self.table_tree['columns'] = ("Equipment_Name", "Equipment_Stock", "Equipment_ID") #sets the titles of the columns in the tree

		# Format Our Columns
		self.table_tree.column("#0", width=0, stretch=NO)
		self.table_tree.column("Equipment_Name", anchor=CENTER, width=280)
		self.table_tree.column("Equipment_Stock", anchor=W, width=50)
		self.table_tree.column("Equipment_ID", anchor=W, width=50)


		# Create Headings
		self.table_tree.heading("#0", text="", anchor=W)
		self.table_tree.heading("Equipment_Name", text="Equipment\nname", anchor=CENTER)
		self.table_tree.heading("Equipment_Stock", text="Stock", anchor=W)
		self.table_tree.heading("Equipment_ID", text="ID", anchor=W)

		u2=Location_get_values(self.LocationConfirm, "", "", "", "") #creates an instance of the class get_values under the object self
		u2.records = u2.add_in_location() #grabs values from location and equipment tables
		global count # Add our data to the screen
		count = 0

		#we will alternate the colors of the rows for improved visibility
		self.table_tree.tag_configure('oddrow', background="white")
		self.table_tree.tag_configure('evenrow', background="lightblue")

		for record in u2.records:
			if count % 2 == 0:
				self.table_tree.insert(parent='', index='end', text='', values=(record[0], record[1], record[2]), tags=('evenrow',))
			else:
				self.table_tree.insert(parent='', index='end',  text='', values=(record[0], record[1], record[2]), tags=('oddrow',))
			
			# increment counter
			count += 1	

	def record_entries(self):
		#creates frame to hold entries for records
		self.data_frame = LabelFrame(self.inventory_page, text="Record")
		self.data_frame.grid(row=3, column=0, columnspan=5, padx=20, pady=20, ipadx=100)

		self.EquipmentName_Label = Label(self.data_frame, text="Equipment Name")
		self.EquipmentName_Label.grid(row=0, column=2, padx=10, pady=10)
		self.EquipmentName_Entry = Entry(self.data_frame, width=30)
		self.EquipmentName_Entry.grid(row=0, column=3, padx=10, pady=10)

		self.Stock_Label = Label(self.data_frame, text="Stock")
		self.Stock_Label.grid(row=0, column=4, padx=10, pady=10)
		self.Stock_Entry = Entry(self.data_frame, width=7)
		self.Stock_Entry.grid(row=0, column=5, padx=10, pady=10)

		self.EquipmentID_Label = Label(self.data_frame, text="Equipment ID")
		self.EquipmentID_Label.grid(row=0, column=6, padx=10, pady=10)
		self.EquipmentID_Entry = Entry(self.data_frame, width=7)
		self.EquipmentID_Entry.grid(row=0, column=7, padx=10, pady=10)

		self.Location_Label= Label(self.data_frame, text="Location")
		self.Location_Label.grid(row=0, column=8, padx=10, pady=10)
		self.Location_Entry = Entry(self.data_frame, width=7)
		self.Location_Entry.grid(row=0, column=9, padx=10, pady=10)

		self.errorLabel = Label(self.data_frame)
		self.errorLabel.grid(row=1, column=0)

		self.table_tree.bind("<ButtonRelease-1>", self.select_record) #whenever the user clicks on a row in the treeview, it will call the function select_record
	
	# Select Record
	def select_record(self, event):
		self.selected = self.table_tree.focus()# record Number
		self.values = self.table_tree.item(self.selected, 'values')# record values

		self.clear_entries()
		# outputs to entry boxes
		self.EquipmentName_Entry.insert(0, self.values[0])
		self.Stock_Entry.insert(0, self.values[1])
		self.EquipmentID_Entry.insert(0, self.values[2])

	def clear_entries(self):
		# Clear entry boxes
		self.EquipmentName_Entry.delete(0, END)
		self.EquipmentID_Entry.delete(0, END)
		self.Stock_Entry.delete(0, END)

	def update_record(self):
		self.selected = self.table_tree.focus() #grabs the record number from the selected line on the treeview
		self.table_tree.item(self.selected, text="", values=(self.EquipmentName_Entry.get(), self.Stock_Entry.get(),)) # Update record

		#before the record is updated, the entries must first be validated
		self.Entered_EquipmentName = self.EquipmentName_Entry.get()
		self.Entered_Stock = self.Stock_Entry.get()
		self.Entered_EquipmentID = self.EquipmentID_Entry.get()

		self.error_status=self.validate_LocationEntries()
		if self.error_status ==True:
			u2=Location_get_values(self.LocationConfirm, "", self.Entered_Stock, self.Entered_EquipmentID, "") #creates an instance of the class get_values under the object self
			u2.update_Location_db() #updates the selected record with the entered validated values
		else:
			self.errorLabel.configure(text="Invalid input")

	def validate_LocationEntries(self):
		u2=Equipment_Location_Validate("",self.Entered_EquipmentName, self.Entered_Stock,"","")
		self.equipmentName_format_valid=u2.validate_EquipmentName(self.Entered_EquipmentName)
		self.EquipmentStock_format_valid=u2.validate_EquipmentStock(self.Entered_Stock)
		if self.equipmentName_format_valid==True and self.EquipmentStock_format_valid==True:
			self.error_status=True
		else:
			self.error_status=False
		return self.error_status


	def add_to_location(self):

		self.Entered_Stock = self.Stock_Entry.get()
		self.Entered_EquipmentID = self.EquipmentID_Entry.get()
		self.Entered_Location = self.Location_Entry.get()

		self.error_status=self.validate_newItemInLocation()
		if self.error_status ==True:
			u2=Location_get_values("", "", self.Entered_Stock, self.Entered_EquipmentID, self.Entered_Location)
			u2.add_to_Location_db()
			# Clear The Treeview Table
			self.table_tree.delete(*self.table_tree.get_children())

			# Run to pull data from database on start
			self.show_Equipment_Location(self.inventory_page, self.LocationConfirm)
		else:
			self.errorLabel.configure(text="Invalid input")

	def validate_newItemInLocation(self):
		u2=Equipment_Location_Validate(self.Entered_Location,"",self.Entered_Stock,"","")
		#validation of entries
		self.EquipmentStock_format_valid=u2.validate_EquipmentStock(self.Entered_Stock)
		self.LocationFormat_Valid=u2.validate_Location(self.LocationConfirm)
		if self.LocationFormat_Valid==True and self.EquipmentStock_format_valid==True:
			self.error_status=True
		else:
			self.error_status=False
		return self.error_status

	def delete_from_location(self):

		self.Entered_Stock = self.Stock_Entry.get()
		self.Entered_EquipmentID = self.EquipmentID_Entry.get()
		self.Entered_Location = self.Location_Entry.get()
		
		u3=Equipment_Location_Validate(self.Entered_Location,"","","",self.Entered_EquipmentID)
		self.Location_Valid=u3.validate_Location(self.Entered_Location)
		self.EquipmentID_Valid=u3.validate_equipmentID(self.Entered_EquipmentID)
		if self.Location_Valid==True and self.EquipmentID_Valid==True:
			u2=Location_get_values("", "", "", self.Entered_EquipmentID, self.Entered_Location)
			u2.delete_from_Location_db()
			# Clear The Treeview Table
			self.table_tree.delete(*self.table_tree.get_children())

			# Run to pull data from database on start
			self.show_Equipment_Location(self.inventory_page, self.LocationConfirm)
		else:
			self.errorLabel.configure(text="Invalid input")

	def edit_table_buttons(self):
		#buttons associated with editing the equipment table
		self.edit_button_frame = LabelFrame(self.inventory_page, text="Commands")
		self.edit_button_frame.grid(row=4, column=0)

		self.updateButton = Button(self.edit_button_frame, text="Update Record", command=self.update_record)
		self.updateButton.grid(row=0, column=0, padx=10, pady=10)

		self.addButton = Button(self.edit_button_frame, text="Add New Equipment to this Location", command=self.add_to_location)
		self.addButton.grid(row=0, column=1, padx=10, pady=10)

		self.deleteButton=Button(self.edit_button_frame, text="Delete Equipment from this Location", command=self.delete_from_location)
		self.deleteButton.grid(row=1, column=0, padx=10, pady=10)


class Chemical_Chart(Inventory_GUI):
	def __init__(self, inventory_page, permissions):
		self.inventory_page=inventory_page
		self.permissions=permissions
		self.table_tree=self.create_base_chart() #calls function from parent class.
		self.columns()
		self.connect_db_to_treeview()
		self.columns() #sets the columns for the Chemicals table. This will be repeated for all the other required tables.

		self.check_permissions_edit_Chemicals_Chart()
		self.search_frame()

	def columns(self): #columns for chemical table
		self.table_tree['columns'] = ("Chemical_ID", "Chemical_Name", "Chemical_Stock") #sets the titles of the columns in the tree

		# Format Our Columns
		self.table_tree.column("#0", width=0, stretch=NO)
		self.table_tree.column("Chemical_ID", anchor=CENTER, width=80)
		self.table_tree.column("Chemical_Name", anchor=W, width=210)
		self.table_tree.column("Chemical_Stock", anchor=W, width=90)

		# Create Headings
		self.table_tree.heading("#0", text="", anchor=W)
		self.table_tree.heading("Chemical_ID", text="Chemical ID", anchor=CENTER)
		self.table_tree.heading("Chemical_Name", text="Chemical Name", anchor=W)
		self.table_tree.heading("Chemical_Stock", text="Chemical Stock", anchor=W)

	def connect_db_to_treeview(self):
		u2=Chemicals_get_values("","","","") #creates an instance of the class get_values under the object self
		u2.records = u2.query_Chemicals_table() #gets everything from the chemicals table
		global count # Add our data to the screen
		count = 0

		#we will alternate the colors of the rows for improved visibility
		self.table_tree.tag_configure('oddrow', background="white")
		self.table_tree.tag_configure('evenrow', background="lightblue")

		#populates the treeview
		for record in u2.records:
			if count % 2 == 0:
				self.table_tree.insert(parent='', index='end', iid=count, text='', values=(record[2], record[0], record[1]), tags=('evenrow',))
			else:
				self.table_tree.insert(parent='', index='end', iid=count, text='', values=(record[2], record[0], record[1]), tags=('oddrow',))
			
			# increment counter
			count += 1

		self.selected = self.table_tree.focus()# record Number
		self.values = self.table_tree.item(self.selected, 'values')# record values

		return self.values

	def search_frame(self):
		# Create label frame
		self.search_frame = LabelFrame(self.inventory_page, text="Search")
		self.search_frame.grid(row=4,column=1, pady=10)

		# Search entry box
		self.search_entry = Entry(self.search_frame)
		self.search_entry.grid(row=0, column=0, pady=20, padx=20)

		# Search button
		self.search_button = Button(self.search_frame, text="Search Chemicals", command=self.search_Chemicals_Chart)
		self.search_button.grid(row=0, column=1, padx=20, pady=20)


	def search_Chemicals_Chart(self):
		self.ChemicalName_Lookup = self.search_entry.get()
		self.search_entry.delete(0, END)

		# Clear the Treeview
		for record in self.table_tree.get_children():
			self.table_tree.delete(record)

		u2=Chemicals_get_values(self.ChemicalName_Lookup,"","","") #creates an instance of the class Chemicals_get_values under the object self
		u2.records = u2.search_Chemicals_db(self.ChemicalName_Lookup) #gets everything from the equipment table that matches the searched value

		global count # Add our data to the screen
		count = 0
		
		for record in u2.records:
			if count % 2 == 0:
				self.table_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]), tags=('evenrow',))
			else:
				self.table_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]), tags=('oddrow',))

	def check_permissions_edit_Chemicals_Chart(self):
		if self.permissions == True: #if the logged in user has technician permissions, then an instance of the edit_Chemicals_Chart is made.
			self = edit_Chemicals_Chart(self.inventory_page, self.table_tree, self.values)
			
		else:
			pass


class edit_Chemicals_Chart(Chemical_Chart):

	def __init__(self, inventory_page, table_tree, values):
		self.values=values
		self.table_tree=table_tree
		self.inventory_page=inventory_page
		self.record_entries()
		self.edit_table_buttons()
		
	def record_entries(self):
		#creates frame to hold entries for records
		self.data_frame = LabelFrame(self.inventory_page, text="Record")
		self.data_frame.grid(row=3, column=0, columnspan=5, padx=20, pady=20, ipadx=100)

		self.ChemicalID_Label = Label(self.data_frame, text="Chemical ID")
		self.ChemicalID_Label.grid(row=0, column=0, padx=10, pady=10)
		self.ChemicalID_Entry = Entry(self.data_frame, width=7)
		self.ChemicalID_Entry.grid(row=0, column=1, padx=10, pady=10)

		self.ChemicalName_Label = Label(self.data_frame, text="Chemical Name")
		self.ChemicalName_Label.grid(row=0, column=2, padx=10, pady=10)
		self.ChemicalName_Entry = Entry(self.data_frame, width=30)
		self.ChemicalName_Entry.grid(row=0, column=3, padx=10, pady=10)

		self.ChemicalStock_Label = Label(self.data_frame, text="Chemical Stock")
		self.ChemicalStock_Label.grid(row=0, column=4, padx=10, pady=10)
		self.ChemicalStock_Entry = Entry(self.data_frame, width=7)
		self.ChemicalStock_Entry.grid(row=0, column=5, padx=10, pady=10)

		self.table_tree.bind("<ButtonRelease-1>", self.select_record) #whenever the user clicks on a row in the treeview, it will call the function 

	
	def edit_table_buttons(self):
		#buttons to edit the chemicals table
		self.edit_button_frame = LabelFrame(self.inventory_page, text="Commands")
		self.edit_button_frame.grid(row=4, column=0)

		self.updateButton = Button(self.edit_button_frame, text="Update Record", command=self.update_record)
		self.updateButton.grid(row=0, column=0, padx=10, pady=10)

		self.newrecordButton = Button(self.edit_button_frame, text="New Chemical", command=self.add_record)
		self.newrecordButton.grid(row=0, column=1, padx=10, pady=10)

		self.deleterecordButton = Button(self.edit_button_frame, text="Delete Chemical", command=self.delete_record)
		self.deleterecordButton.grid(row=0, column=2, padx=10, pady=10)

		self.errorLabel = Label(self.edit_button_frame)
		self.errorLabel.grid(row=2, column=0)

	def clear_entries(self):
		# Clear entry boxes
		self.ChemicalID_Entry.delete(0, END)
		self.ChemicalName_Entry.delete(0, END)
		self.ChemicalStock_Entry.delete(0, END)
	
	# Select Record
	def select_record(self, event):
		self.selected = self.table_tree.focus()# record Number
		self.values = self.table_tree.item(self.selected, 'values')# record values

		self.clear_entries()
		# outputs to entry boxes
		self.ChemicalID_Entry.insert(0, self.values[0])
		self.ChemicalName_Entry.insert(0, self.values[1])
		self.ChemicalStock_Entry.insert(0, self.values[2])

	def update_record(self):

		self.selected = self.table_tree.focus() #grabs the record number from the selected line on the treeview
		self.Entered_ChemicalName = self.ChemicalName_Entry.get()
		self.Entered_ChemicalStock = self.ChemicalStock_Entry.get()
		self.Entered_ChemicalID = self.ChemicalID_Entry.get()

		#validate the entries
		u2=Chemicals_Validate(self.Entered_ChemicalName, self.Entered_ChemicalStock)
		self.chemicalName_format_valid=u2.Validate_ChemicalName(self.Entered_ChemicalName)
		self.ChemicalStock_format_valid=u2.validate_ChemicalStock(self.Entered_ChemicalStock)

		if self.chemicalName_format_valid==True and self.ChemicalStock_format_valid==True:
			u2=Chemicals_get_values("", self.Entered_ChemicalName, self.Entered_ChemicalStock, self.Entered_ChemicalID)
			u2.update_Chemicals_db() #updates the chemicals table
			self.table_tree.item(self.selected, text="", values=(self.ChemicalID_Entry.get(), self.ChemicalName_Entry.get(), self.ChemicalStock_Entry.get(),)) # Update record

		else:
			self.errorLabel.configure(text="Invalid input")


	
	def add_record(self):
		self.Entered_ChemicalName = self.ChemicalName_Entry.get()
		self.Entered_ChemicalStock = self.ChemicalStock_Entry.get()

		#validate the entries
		u2=Chemicals_Validate(self.Entered_ChemicalName, self.Entered_ChemicalStock)
		self.chemicalName_format_valid=u2.Validate_ChemicalName(self.Entered_ChemicalName)
		self.ChemicalStock_format_valid=u2.validate_ChemicalStock(self.Entered_ChemicalStock)

		if self.chemicalName_format_valid==True and self.ChemicalStock_format_valid==True:
			u2=Chemicals_get_values("", self.Entered_ChemicalName, self.Entered_ChemicalStock, "")
			u2.add_Chemicals_db()
		else:
			self.errorLabel.configure(text="Invalid input")

		#clears entries
		self.clear_entries()

		# Clear The Treeview Table
		self.table_tree.delete(*self.table_tree.get_children())

		# Run to pull data from database on start
		self.connect_db_to_treeview()

	def delete_record(self):

		self.x = self.table_tree.selection()[0]
		self.table_tree.delete(self.x)
		
		#deletes the selected value
		self.Entered_ChemicalID = self.ChemicalID_Entry.get()		
		u2=Chemicals_get_values("", "", "", self.Entered_ChemicalID)
		u2.delete_Chemicals_db()

		# Clear The Entry Boxes
		self.clear_entries()