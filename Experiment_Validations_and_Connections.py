import sqlite3 #imports database SQLite 3 library for SQL functions
import re #this imports the regular expression module

class Experiment_Database_Connections:
	def __init__(self, Entered_EquipmentName, Entered_ChemicalName, Entered_ExperimentName, Entered_NumberOfSets, Generated_ExperimentID, Entered_EquipmentAmount, Entered_ChemicalAmount):
		self.Entered_EquipmentName=Entered_EquipmentName
		self.Entered_ChemicalName=Entered_ChemicalName
		self.Entered_ExperimentName=Entered_ExperimentName
		self.Entered_NumberOfSets=Entered_NumberOfSets
		self.Generated_ExperimentID=Generated_ExperimentID
		self.Entered_EquipmentAmount=Entered_EquipmentAmount
		self.Entered_ChemicalAmount=Entered_ChemicalAmount

	def get_all_equipment_as_list(self):
		conn = sqlite3.connect("Command_Lab.db")
		conn.row_factory = lambda cursor, row: row[0] #configures it so that it is stored as a regular list in the form  [x,y,z] instead of [(x,),(y,),(z,)], which is easier to read by tkinter optionmenu
		c = conn.cursor()
		EquipmentList = c.execute("SELECT Equipment_Name FROM Equipment").fetchall() #gets all the names in the equipment table for the dropdown menu

		conn.commit() #commits changes
		conn.close() #closes connection to database		
		return EquipmentList

	def get_all_chemicals_as_list(self):
		conn = sqlite3.connect("Command_Lab.db")
		conn.row_factory = lambda cursor, row: row[0] #configures it so that it is stored as a regular list in the form  [x,y,z] instead of [(x,),(y,),(z,)], which is easier to read by tkinter optionmenu
		c = conn.cursor()
		ChemicalsList = c.execute("SELECT Chemical_Name FROM Chemicals").fetchall() #gets all the names in the chemicals table for the dropdown menu
		conn.commit() #commits changes
		conn.close() #closes connection to database				
		return ChemicalsList

	def get_equipment_stock(self, Entered_EquipmentName):
		conn = sqlite3.connect("Command_Lab.db")
		c=conn.cursor()

		c.execute("""
			SELECT Equipment_Location.Equipment_Stock FROM Equipment
			INNER JOIN Equipment_Location ON Equipment_Location.Equipment_ID = Equipment.Equipment_ID 
			WHERE Equipment.Equipment_Name=(?)
			""", (self.Entered_EquipmentName,)) #gets the information about the stock and location of the selected equipment.

		queriedStockvalue=(c.fetchall())
		equipmentStockvalue=0
		for i in range(0, len(queriedStockvalue)):
			equipmentStockvalue+=int(queriedStockvalue[i][0]) #adds them to a 2D array for easier manipulation

		conn.commit() #commits changes
		conn.close() #closes connection to database		
		return equipmentStockvalue

	def get_equipment_locations(self,Entered_EquipmentName):
		conn = sqlite3.connect("Command_Lab.db")
		c=conn.cursor()

		Equipment_Locations=c.execute("SELECT Equipment_Location.Location_ID, Equipment_Location.Equipment_Stock FROM Equipment INNER JOIN Equipment_Location ON Equipment_Location.Equipment_ID = Equipment.Equipment_ID WHERE Equipment_Name=(?) ORDER BY Equipment_Location.Location_ID ASC", (self.Entered_EquipmentName,)).fetchall() #selects the stock available in a specific location for the specified equipment
		
		conn.commit() #commits changes
		conn.close() #closes connection to database	

		return Equipment_Locations

	def get_chemical_stock(self, Entered_ChemicalName):
		conn = sqlite3.connect("Command_Lab.db")
		c=conn.cursor()

		Chemical_Stock=c.execute("SELECT Chemical_Stock FROM Chemicals WHERE Chemical_Name=(?)", (self.Entered_ChemicalName,)).fetchall() #gets the stock for the specified chemical
		
		conn.commit() #commits changes
		conn.close() #closes connection to database	

		return Chemical_Stock

	def SendTo_Experiment_Sets(self, Entered_ExperimentName, Entered_NumberOfSets):
		conn = sqlite3.connect("Command_Lab.db")
		c=conn.cursor()

		c.execute("INSERT INTO Experiment_Sets VALUES (NULL, :Experiment_Name, :Experiment_Sets)", {"Experiment_Name": self.Entered_ExperimentName, "Experiment_Sets": self.Entered_NumberOfSets}) #inserts the new attributes related to the experiment name and experiment sets for the new experiment to get a new experiment ID
		Generated_ExperimentID=c.execute("SELECT Experiment_ID FROM Experiment_Sets WHERE Experiment_Name=(?)", (self.Entered_ExperimentName,)).fetchone()[0]		#returns the new experiment ID
		conn.commit() #commits changes
		conn.close() #closes connection to database	
		return Generated_ExperimentID

	def SendTo_Experiment_Equipment(self, Entered_EquipmentName, Generated_ExperimentID, Entered_EquipmentAmount):
		conn = sqlite3.connect("Command_Lab.db")
		c=conn.cursor()

		self.Equipment_ID = c.execute("SELECT Equipment_ID FROM Equipment WHERE Equipment_Name = (?)", (self.Entered_EquipmentName,)).fetchone()[0]
		c.execute("INSERT INTO Experiment_Equipment VALUES (:Experiment_ID, :Equipment_ID, :Equipment_Amount)", {"Experiment_ID": self.Generated_ExperimentID, "Equipment_ID": self.Equipment_ID, "Equipment_Amount": self.Entered_EquipmentAmount}) #adds the new equipment and their amounts to the table
		
		conn.commit() #commits changes
		conn.close() #closes connection to database	

	def SendTo_Experiment_Chemicals(self, Entered_ChemicalName, Generated_ExperimentID, Entered_ChemicalAmount):
		conn = sqlite3.connect("Command_Lab.db")
		c=conn.cursor()

		self.Chemical_ID = c.execute("SELECT Chemical_ID FROM Chemicals WHERE Chemical_Name = (?)", (self.Entered_ChemicalName,)).fetchone()[0]
		c.execute("INSERT INTO Experiment_Chemicals VALUES (:Experiment_ID, :Chemical_ID, :Chemical_Amount)", {"Experiment_ID": self.Generated_ExperimentID, "Chemical_ID": self.Chemical_ID, "Chemical_Amount": self.Entered_ChemicalAmount}) #adds the new chemicals and their amounts to the table
		
		conn.commit() #commits changes
		conn.close() #closes connection to database	

	def delete_Selected_Experiment(self, Entered_ExperimentName):
		conn = sqlite3.connect("Command_Lab.db")
		c=conn.cursor()		

		c.execute('DELETE from Experiment_Sets WHERE Experiment_Name=?',(self.Entered_ExperimentName,))
		conn.commit() #commits changes
		conn.close() #closes connection to database	

class Experiments_Validations(Experiment_Database_Connections): #validation functions
	def __init__(self, Experiment_Name, Experiment_Sets):
		self.Experiment_Name=Experiment_Name
		self.Experiment_Sets=Experiment_Sets

	def validate_ExperimentName(self, Experiment_Name):
		experimentName_Format = "^[A-Za-z0-9 ]{1,50}$" #checks that experiment title is only alphabet or a space and is between 1 and 50 characters.

		if re.fullmatch(experimentName_Format, self.Experiment_Name): #checks if entered experiment name matches the correct format
			experimentName_format_valid=True
		else:
			experimentName_format_valid=False #any other format, including an empty value, would be revoked

		return experimentName_format_valid

	def validate_ExperimentSets(self, Experiment_Sets):
		experimentSets_Format = "^([1-9]|10|)$" #checks that the sets are between 0-10

		if re.fullmatch(experimentSets_Format, self.Experiment_Sets): #checks if matches the correct format
			experimentSets_Format_Valid=True
		else:
			experimentSets_Format_Valid=False #any other format, including an empty value, would be revoked

		return experimentSets_Format_Valid    	

class open_existing_experiment(Experiment_Database_Connections):

	def __init__(self, Selected_ExperimentName):
		self.Selected_ExperimentName=Selected_ExperimentName

	def get_experiment_names(self):
		conn = sqlite3.connect("Command_Lab.db")
		conn.row_factory = lambda cursor, row: row[0] #configures it so that it is stored as a regular list in the form  [x,y,z] instead of [(x,),(y,),(z,)], which is easier to read by tkinter optionmenu
		c=conn.cursor()

		ExperimentNames = c.execute("SELECT Experiment_Name FROM Experiment_Sets").fetchall() #gets all the existing experiments to be displayed for the user
		
		conn.commit() #commits changes
		conn.close() #closes connection to database	
		return ExperimentNames

	def get_all_existing_experiments(self, Selected_ExperimentName):
		conn=sqlite3.connect("Command_Lab.db")

		c=conn.cursor()
		ExperimentDetails_List = c.execute("SELECT Experiment_ID, Experiment_Sets FROM Experiment_Sets WHERE Experiment_Sets.Experiment_Name=(?)", (self.Selected_ExperimentName,)).fetchall()
		self.Experiment_ID=ExperimentDetails_List[0][0]
		ExperimentDetails_List.append(c.execute("SELECT Experiment_Chemicals.Chemical_Amount, Chemicals.Chemical_Name FROM Experiment_Chemicals INNER JOIN Chemicals ON Experiment_Chemicals.Chemical_ID = Chemicals.Chemical_ID WHERE Experiment_Chemicals.Experiment_ID=(?)", (self.Experiment_ID,)).fetchall())
		ExperimentDetails_List.append(c.execute("SELECT Experiment_Equipment.Equipment_Amount, Equipment.Equipment_Name FROM Experiment_Equipment INNER JOIN Equipment ON Experiment_Equipment.Equipment_ID = Equipment.Equipment_ID WHERE Experiment_Equipment.Experiment_ID=(?)", (self.Experiment_ID,)).fetchall())
		conn.commit()
		conn.close() #gets all the information about equipment and chemicals and their corresponding amounts for the passed in experiment Name from the dropdown menu.

		return ExperimentDetails_List