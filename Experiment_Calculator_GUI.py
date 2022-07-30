from tkinter import * #imports tkinter library for GUI
from PIL import ImageTk, Image #imports pillow to be able to handle png image files
from tkinter import ttk #this is used to use treeview, which can be used to visualize the database
from tkinter.font import Font

from Experiment_Validations_and_Connections import *




class Experiment_Calculator_Window:
	def __init__(self, parent):
		self.parent=parent #creates the tkinter root window, from which all the other tkinter components are managed
		self.experiment_page=Toplevel(self.parent) #creates an instance of the class using the root tkinter window that can be accessed throughout the class


	def configure_GUI(self):
		self.experiment_page.title("Command Lab - Experiment Page") #sets title of the window
		self.experiment_page.iconbitmap("logo.ico") #sets icon of the window
		self.experiment_page.geometry("910x607") #sets size of login_page window as that of background image

		#inserts image in background of main experiment_page window
		global img
		img=ImageTk.PhotoImage(file='img1.png') #defined the background image
		back_label = Label(self.experiment_page, image=img) #created a label for image
		back_label.place(x=0, y=0, relheight=1, relwidth=1) #positioned image at the top left

		#title text
		self.title_font = Font(family = "SF Compact Text", size=42)
		self.title_text = Label(self.experiment_page, text="Command Lab", fg="navy blue", font=self.title_font)
		self.title_text.grid(row=0, column=0)

		self.createNewExperiment_Button=Button(self.experiment_page, text="Create new Experiment", command=self.create_entries_frame) #when pressed, it calls the function to create the widgets to create a new experiment
		self.createNewExperiment_Button.grid(row=0, column=1)

		self.openExistingExperiment_Button=Button(self.experiment_page, text="Open existing Experiment", command=self.create_ExistingExperiment_frame) #when pressed, the button calls the function that opens the frame to view the details about an existing experiment
		self.openExistingExperiment_Button.grid(row=0, column=2)

		try:
			self.parent.mainloop()
		except:
			pass

	def create_ExistingExperiment_frame(self):
		self.existing_experiment_frame = LabelFrame(self.experiment_page, text="Open existing Experiment") 
		self.existing_experiment_frame.grid(row=1, column=0, pady=20)	

		u5=open_existing_experiment("")
		u5.experimentlist=u5.get_experiment_names() #gets all the experiment names to go into the dropdwon menu
		self.ExperimentOptions= StringVar(self.experiment_page) 
		self.ExperimentOptions.set("*Select Experiment*")
		self.experiment_menu=OptionMenu(self.existing_experiment_frame, self.ExperimentOptions, *u5.experimentlist) #dropdown menu with the contents of the experiment list as the options
		self.experiment_menu.grid(row=0, column=0)	

		self.submit_Experiment_Button=Button(self.existing_experiment_frame, text="submit", command=self.populate_ExistingExperiment_frame) #calls the function to get all the details about the selected experiment from the dropdown menu
		self.submit_Experiment_Button.grid(row=0, column=1)

	def populate_ExistingExperiment_frame(self):
		u2=open_existing_experiment(self.ExperimentOptions.get())
		self.existing_experiment_details=u2.get_all_existing_experiments(self.ExperimentOptions.get()) #populates the window with the information about the selected experiment  

		self.existing_experiment_output=("Number of sets: "+ str(self.existing_experiment_details[0][1])+"\nChemicals: "+str(self.existing_experiment_details[1])+"\nEquipment: "+str(self.existing_experiment_details[2])) #displays all the equipment and chemicals and their amounts associated with that specific experiment

		self.experiment_Label=Label(self.existing_experiment_frame, text=self.existing_experiment_output) #displays that information to the screen
		self.experiment_Label.grid(row=2, column=1)

		self.Delete_SelectedExperiment_Button=Button(self.existing_experiment_frame, text="Delete Selected Experiment", command=self.Delete_SelectedExperiment)
		self.Delete_SelectedExperiment_Button.grid(row=3, column=1)
	def Delete_SelectedExperiment(self):

		u2=Experiment_Database_Connections("","",self.ExperimentOptions.get(),"","","","")
		u2.delete_Selected_Experiment(self.ExperimentOptions.get())

	def create_entries_frame(self):
		self.new_experiment_frame = LabelFrame(self.experiment_page, text="Create new Experiment") #frame for the entry boxes
		self.new_experiment_frame.grid(row=1, column=0, pady=20)

		self.experimentTitle_Label = Label(self.new_experiment_frame, text="Experiment Name:") 
		self.experimentTitle_Label.grid(row=0, column=0, pady=(20,0))
		self.experimentTitle_Entry= Entry(self.new_experiment_frame) #user enters the experiment name
		self.experimentTitle_Entry.grid(row=0, column=0, columnspan=2, pady=(20,0))

		self.experimentSets_Label=Label(self.new_experiment_frame, text="Sets of Experiments:")
		self.experimentSets_Label.grid(row=1, column=0, pady=20)
		self.experimentSets_Entry=Spinbox(self.new_experiment_frame, from_=0, to=100) #user enters the number of sets of that experiment (how many groups of students are going to be doing the experiment)
		self.experimentSets_Entry.grid(row=2, column=0, columnspan=2)

		self.experimentEquipment_Label=Label(self.new_experiment_frame, text="Equipment:")
		self.experimentSets_Label.grid(row=2, column=0, pady=20)
		
		self.equipmentRow=4 #first equipment drop down menu is going to be placed in row 3
		self.equipment_entries_list=[] #this list is where the equipment amounts will be stored
		self.equipment_dropdown_list=[] #this list is where the equipment names will be stored
		self.numberOfEquipment_Label=Label(self.new_experiment_frame, text="Number of equipment:")
		self.numberOfEquipment_Label.grid(row=3, column=0, stick='w')
		self.numberOfEquipment_Entry=Entry(self.new_experiment_frame,  width=5) #number of equipment that are specific to that experiment
		self.numberOfEquipment_Entry.grid(row=3, column=0, padx=(150,0), stick='w')
		self.confirm_NumberofEquipment_Entry = Button(self.new_experiment_frame, bg="light green", text="Confirm", command=self.equipment_entry) #this will call the function to create an appropriate number of entries of equipment
		self.confirm_NumberofEquipment_Entry.grid(row=3, column=0, padx=(200,0), stick='w')
		
		self.chemicalRow=4
		self.chemicals_entries_list=[] #this list is where the chemical amounts will be stored
		self.chemicals_dropdown_list=[] #this list is where the chemical names will be stored
		self.numberOfChemicals_Label=Label(self.new_experiment_frame, text="Number of chemicals:")
		self.numberOfChemicals_Label.grid(row=3, column=1)
		self.numberOfChemicals_Entry=Entry(self.new_experiment_frame,  width=5) #number of chemicals that are specific to that experiment
		self.numberOfChemicals_Entry.grid(row=3, column=1, padx=(190,0))
		self.confirm_NumberofChemicals_Entry = Button(self.new_experiment_frame, bg="light green", text="Confirm", command=self.chemicals_entry) #this will call the function to create an appropriate number of entries of chemicals
		self.confirm_NumberofChemicals_Entry.grid(row=3, column=1, padx=(290,0))

		self.submitExperimenttoDb_Button = Button(self.experiment_page, bg="light green", text="Save Experiment", command=self.check_for_experiment_errors) #calls the function to submit these new details to the database to be stored
		self.submitExperimenttoDb_Button.grid(row=3, column=1)


	def equipment_entry(self):
		u2=Experiment_Database_Connections("","","","","","","")
		u2.equipmentlist=u2.get_all_equipment_as_list() #this is the list which will store all the equipment names in the entire database, from which the user can choose which one they wish to select for their experiment
		self.equipment_num=int(self.numberOfEquipment_Entry.get()) #this stores the number of equipments that is extracted from the entry
		for i in range (0, self.equipment_num): #creates as many equipment entry boxes for the number that was selected earlier
			self.EquipmentOptions = StringVar(self.experiment_page)
			self.EquipmentOptions.set("Equipment "+ str(i+1)) #makes the default selected value of the dropdown menu linked to the row
			self.equipment_dropdown=OptionMenu(self.new_experiment_frame, self.EquipmentOptions, *u2.equipmentlist) # Create and append to list
			self.equipment_dropdown.grid(row=i+4, column=0, sticky='w') # Place the just created widget
			self.equipment_dropdown_list.append(self.EquipmentOptions)
		for i in range(0, self.equipment_num):
			self.equipment_entries_list.append(Spinbox(self.new_experiment_frame, width=10, from_=0, to=1000)) # Create and append to list
			self.equipment_entries_list[-1].grid(row=i+4, column=0, padx=(180,0)) # Place the just created widget
		self.check_equipment_stock_Button = Button(self.new_experiment_frame, bg="light green", text="Show Stock", command=self.display_equipment_stock) #this will call the function to display the stock and location of the selected equipment
		self.check_equipment_stock_Button.grid(row=11, column=0, padx=(320,0))

	def display_equipment_stock(self):
		#makes the window to display the available locations and stocks for the corresponding equipment
		self.top_window=Toplevel()
		self.top_window.geometry("607x307")
		self.top_window.title("Equipment Stock")

		for val in range(0, (len(self.equipment_dropdown_list))): #for every value in the equipment name list...
			#displays all the equipment
			self.EquipmentName=self.equipment_dropdown_list.pop()
			self.EquipmentName=self.EquipmentName.get()
			self.EquipmentName_Label=Label(self.top_window, text=self.EquipmentName)
			self.EquipmentName_Label.grid(row=0, column=val, padx=20, pady=20)

			#places a column separator for visual separation between equipment
			self.ColumnSeparator=ttk.Separator(self.top_window, orient=VERTICAL).grid(column=val, row=0, rowspan=3, sticky='nse')

			#gets values of stock that are entered by the user earlier
			self.EnteredEquipmentStock_Label=Label(self.top_window, text="Entered Stock: "+(self.equipment_entries_list[val].get()))
			self.EnteredEquipmentStock_Label.grid(row=1, column=val, padx=20)

			# try:
			u2=Experiment_Database_Connections(self.EquipmentName, "","","","","","")
			u2.equipmentStockvalue=u2.get_equipment_stock(self.EquipmentName)

			if u2.equipmentStockvalue==0:	#if there is no recorded stock in the database, then an appropriate message is displayed
				self.EquipmentStockLookup_Label=Label(self.top_window, text="Located Stock: None", bg='red')
				self.EquipmentStockLookup_Label.grid(row=2, column=val, padx=20)
			else:

				self.EquipmentStockLookup_Label=Label(self.top_window, text="Located Total Stock: "+str(u2.equipmentStockvalue)) #displays the stock in the location
				self.EquipmentStockLookup_Label.grid(row=2, column=val, padx=20)

				self.LocationofStock_Label=Label(self.top_window, text="Stock is available in: ") #displays the location of the stock
				self.LocationofStock_Label.grid(row=3, column=val, pady=20)

				u2.Equipment_Locations=u2.get_equipment_locations(self.EquipmentName)

				for i in range (0, len(u2.Equipment_Locations)):
					self.EquipmentStock_Label=Label(self.top_window, text="Lab #" + str(u2.Equipment_Locations[i][0]) + ": " + str(u2.Equipment_Locations[i][1])) #Manipulates array and tuple in vector array to display corresponding values correctly
					self.EquipmentStock_Label.grid(row=i+5, column=val)

	def chemicals_entry(self):
		u2=Experiment_Database_Connections("","","","","","","")
		u2.chemicalList=u2.get_all_chemicals_as_list()  #this is the list which will store all the chemical names in the entire database, from which the user can choose which one they wish to select for their experiment
		self.chem_num=int(self.numberOfChemicals_Entry.get()) #this stores the number of chemicals that is extracted from the entry that the user selected

		for i in range (0, self.chem_num): #creates as many chemical entry boxes for the number that was selected earlier
			self.ChemicalOptions = StringVar(self.experiment_page)
			self.ChemicalOptions.set("Chemical "+ str(i+1)) #makes the default selected value of the dropdown menu linked to the row
			self.chemicals_dropdown=OptionMenu(self.new_experiment_frame, self.ChemicalOptions, *u2.chemicalList) # Create and append to list
			self.chemicals_dropdown.grid(row=i+4, column=1, sticky='w') # Place the just created widget
			self.chemicals_dropdown_list.append(self.ChemicalOptions)

		for i in range(0, self.chem_num):
			self.chemicals_entries_list.append(Spinbox(self.new_experiment_frame, width=8, from_=0, to=2000)) # Create and append to list
			self.chemicals_entries_list[-1].grid(row=i+4, column=1, padx=(180,0)) # Place the just created widget
		self.check_chemical_stock_Button = Button(self.new_experiment_frame, bg="light green", text="Show Stock", command=self.display_chemical_stock)#this will call the function to display the stock availability of the selected chemical
		self.check_chemical_stock_Button.grid(row=11, column=1, padx=(320,0))
	
	def display_chemical_stock(self):
		#makes the window to display the available stocks for the corresponding chemical
		self.top_window=Toplevel()
		self.top_window.geometry("607x307")
		self.top_window.title("Chemical Stock")

		for val in range(0, (len(self.chemicals_dropdown_list))): #for every value in the chemical name list...
			#displays all the equipment
			self.ChemicalName=self.chemicals_dropdown_list[val].get()
			self.ChemicalName_Label=Label(self.top_window, text=self.ChemicalName)
			self.ChemicalName_Label.grid(row=0, column=val, padx=20, pady=20)

			#places a column separator for visual separation between equipment
			self.ColumnSeparator=ttk.Separator(self.top_window, orient=VERTICAL).grid(column=val, row=0, rowspan=3, sticky='nse')

			#gets values of stock that are entered by the user earlier
			self.EnteredChemicalStock_Label=Label(self.top_window, text="Entered Chemical Stock: "+(self.chemicals_entries_list[val].get()))
			self.EnteredChemicalStock_Label.grid(row=1, column=val, padx=20)


			try:
				u2=Experiment_Database_Connections("",self.ChemicalName,"","","","","")
				u2.chemicalStockValue=u2.get_chemical_stock(self.ChemicalName)

				if u2.chemicalStockValue==0:	#if there is no recorded stock in the database, then an appropriate message is displayed
					self.ChemicalStockLookup_Label=Label(self.top_window, text="Located Stock: None", bg='red')
					self.ChemicalStockLookup_Label.grid(row=2, column=val, padx=20)
				
				else:
					self.ChemicalsStockLookup_Label=Label(self.top_window, text="Located Total Stock: "+str(u2.chemicalStockValue[0][0])) #displays the stock that was found for the chemical
					self.ChemicalsStockLookup_Label.grid(row=2, column=val, padx=20)

			except:
				self.ChemicalsStockLookup_Label=Label(self.top_window, text="Located Stock: None")
				self.ChemicalsStockLookup_Label.grid(row=2, column=val, padx=20)
				self.ChemicalName_Label.config(bg='red')

	def check_for_experiment_errors(self):
		#creates frame to add error messages
		self.ExperimentError_Frame=LabelFrame(self.experiment_page)
		self.ExperimentError_Frame.grid(row=2, column=0)
		self.ExperimentError_Label=Label(self.ExperimentError_Frame)
		self.ExperimentError_Label.grid(row=0, column=0)
		#sends the below values to the database

		#gets and checks the entered experiment title
		self.Entered_ExperimentName=self.experimentTitle_Entry.get()
		self.experimentName_Valid=self.Check_ExperimentName()

		#gets and checks the entered experiment sets
		self.Entered_NumberOfSets=self.experimentSets_Entry.get()
		self.experimentSets_Valid=self.Check_ExperimentSets()

		if self.experimentName_Valid == True and self.experimentSets_Valid==True:
			self.save_experiment_details()

	def Check_ExperimentName(self):
		#performs validation on the experiment name
		u2=Experiments_Validations(self.Entered_ExperimentName,"")
		u2.experimentName_format_valid=u2.validate_ExperimentName(self.Entered_ExperimentName)
		if u2.experimentName_format_valid==False: #if it is invalid...
			self.ExperimentError_Label.configure(text="Experiment Name Invalid")
		else:
			pass
		return u2.experimentName_format_valid

	def Check_ExperimentSets(self): #performs validation on the number of equipment sets
		u2=Experiments_Validations("",self.Entered_NumberOfSets)
		u2.experimentSets_format_valid=u2.validate_ExperimentSets(self.Entered_NumberOfSets)
		if u2.experimentSets_format_valid==False: #if it is invalid...
			self.ExperimentError_Label.configure(text="Experiment Sets Invalid")
		else:
			pass
		return u2.experimentSets_format_valid
	
	def save_experiment_details(self):

		u2=Experiment_Database_Connections("","", self.Entered_ExperimentName, self.Entered_NumberOfSets,"","","") #creates an instance of the class Experiment_Database_Connections
		self.Generated_ExperimentID= u2.SendTo_Experiment_Sets(self.Entered_ExperimentName, self.Entered_NumberOfSets) #sends off the experiment name and number of sets to be added to the database
		

		for i in range(0, (len(self.equipment_dropdown_list))):
			u3=Experiment_Database_Connections(self.equipment_dropdown_list[i].get(),"","","",self.Generated_ExperimentID,self.equipment_entries_list[i].get(),"")
			u3.SendTo_Experiment_Equipment(self.equipment_dropdown_list[i].get(), self.Generated_ExperimentID, self.equipment_entries_list[i].get()) #sends off the equipment ID's and their amounts that were selected for the experiment

		for i in range(0, (len(self.chemicals_dropdown_list))):
			u4=Experiment_Database_Connections("",self.chemicals_dropdown_list[i].get(),"","",self.Generated_ExperimentID,"",self.chemicals_entries_list[i].get())
			u4.SendTo_Experiment_Chemicals(self.chemicals_dropdown_list[i].get(),self.Generated_ExperimentID,self.chemicals_entries_list[i].get()) #sends off the chemical ID's and the amounts that were selected for the experiment to be sent off for storage


