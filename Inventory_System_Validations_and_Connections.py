import sqlite3 #imports database SQLite 3 library for SQL functions
import numpy as np
import re #this imports the regular expression module

class Equipment_get_values():

	def __init__(self, EquipmentName_Lookup, Entered_EquipmentName, Entered_Consumable, Entered_EquipmentID, selected_science):
		self.EquipmentName_Lookup=EquipmentName_Lookup
		self.Entered_EquipmentName=Entered_EquipmentName
		self.Entered_Consumable=Entered_Consumable
		self.Entered_EquipmentID=Entered_EquipmentID
		self.selected_science=selected_science

	def query_Equipment_db(self):
		conn = sqlite3.connect("Command_Lab.db") #creates or connects to the database
		c=conn.cursor() #creates cursor

		c.execute("SELECT * FROM Equipment") #selects all the records in the equipment table to populate the treeview
		records = c.fetchall()

		conn.commit() #commits changes
		conn.close() #closes connection to database

		return records

	def search_Equipment_db(self):
		conn = sqlite3.connect("Command_Lab.db") #creates or connects to the database
		c=conn.cursor() #creates cursor

		c.execute("SELECT Equipment_ID, * FROM Equipment WHERE Equipment_Name like ?", (self.EquipmentName_Lookup,)) #this returns all the matches to the equipment search query of the user
		records = c.fetchall()
		
		conn.commit() #commits changes
		conn.close() #closes connection to database
		return records

	def update_Equipment_db(self):
		# Update the database
		conn = sqlite3.connect("Command_Lab.db") #creates or connects to the database
		c=conn.cursor() #creates cursor

		c.execute('UPDATE Equipment SET Equipment_Name=?, Consumable=? WHERE Equipment_ID=?', (self.Entered_EquipmentName, self.Entered_Consumable, self.Entered_EquipmentID)) #passes in the new values for the updated equipment name and consumable property, based on the passed-in equipment ID
		
		conn.commit() #commits changes
		conn.close() #closes connection to database

	def add_Equipment_db(self):

		conn = sqlite3.connect("Command_Lab.db") #creates or connects to the database
		c=conn.cursor() #creates cursor
		print(self.Entered_EquipmentName)
		# Add New Record
		c.execute("INSERT INTO Equipment VALUES (:Equipment_Name, :Consumable, NULL)", #inserts a new record into the equipment table using the validated values
			{
				"Equipment_Name" : self.Entered_EquipmentName,
				"Consumable" : self.Entered_Consumable
			})

		conn.commit() #commits changes
		conn.close() #closes connection to database
	
	def delete_Equipment_db(self):

		conn = sqlite3.connect("Command_Lab.db") #creates or connects to the database
		c=conn.cursor() #creates cursor

		c.execute("DELETE from Equipment WHERE oid=" + self.Entered_EquipmentID)# Delete From Database with the provided equipment ID

		conn.commit() #commits changes
		conn.close() #closes connection to database

	def search_by_science_table(self, selected_science):

		conn = sqlite3.connect("Command_Lab.db") #creates or connects to the database
		c=conn.cursor() #creates cursor

		c.execute("""
			SELECT Equipment.Equipment_Name, Equipment_Science.Science, Equipment.Consumable FROM Equipment
			INNER JOIN Equipment_Science ON Equipment.Equipment_ID = Equipment_Science.Equipment_ID
			WHERE Science=(?)
			""", (self.selected_science,)) #this is to filter all the equipment names that match the selected science based on the foreign key Equipment_ID

		records=c.fetchall()
		conn.commit() #commits changes
		conn.close() #closes connection to database

		return records

class Chemicals_get_values:
	def __init__(self, ChemicalName_Lookup, Entered_ChemicalName, Entered_ChemicalStock, Entered_ChemicalID):
		self.ChemicalName_Lookup=ChemicalName_Lookup
		self.Entered_ChemicalName=Entered_ChemicalName
		self.Entered_ChemicalStock=Entered_ChemicalStock
		self.Entered_ChemicalID=Entered_ChemicalID

	def query_Chemicals_table(self):
		conn = sqlite3.connect("Command_Lab.db") #creates or connects to the database
		c=conn.cursor() #creates cursor

		c.execute("SELECT * FROM Chemicals") #gets everything from the chemicals table to populate the treeview
		records = c.fetchall()


		conn.commit() #commits changes
		conn.close() #closes connection to database

		return records

	def search_Chemicals_db(self, ChemicalName_Lookup):
		conn = sqlite3.connect("Command_Lab.db")#creates or connects to the database
		c=conn.cursor() #creates cursor

		c.execute("SELECT Chemical_ID, * FROM Chemicals WHERE Chemical_Name like ?", (self.ChemicalName_Lookup,))  #this returns all the matches to the chemical search query of the user
		records = c.fetchall()
		

		conn.commit() #commits changes
		conn.close() #closes connection to database
		return records

	def update_Chemicals_db(self):
		# Update the database
		conn = sqlite3.connect("Command_Lab.db") ##creates or connects to the database
		c=conn.cursor() #creates cursor

		c.execute('UPDATE Chemicals SET Chemical_Name=?, Chemical_Stock=? WHERE Chemical_ID=?', (self.Entered_ChemicalName, self.Entered_ChemicalStock, self.Entered_ChemicalID)) #passes in the new values for the updated chemical name and stock property, based on the passed-in chemical ID
		
		conn.commit() #commits changes
		conn.close() #closes connection to database
	
	def add_Chemicals_db(self):

		conn = sqlite3.connect("Command_Lab.db") ##creates or connects to the database
		c=conn.cursor() #creates cursor

		# Add New Record
		c.execute("INSERT INTO Chemicals VALUES (:Chemical_Name, :Chemical_Stock, NULL)", #inserts a new record into the chemicals table using the validated values
			{
				"Chemical_Name" : self.Entered_ChemicalName,
				"Chemical_Stock" : self.Entered_ChemicalStock
			})

		conn.commit() #commits changes
		conn.close() #closes connection to database

	def delete_Chemicals_db(self):

		conn = sqlite3.connect("Command_Lab.db") ##creates or connects to the database
		c=conn.cursor() #creates cursor

		c.execute("DELETE from Chemicals WHERE oid=" + self.Entered_ChemicalID)# Delete From Database with the provided chemical ID

		conn.commit() #commits changes
		conn.close() #closes connection to database

class Chemicals_Validate(Chemicals_get_values):
	def __init__(self, Entered_ChemicalName, Entered_ChemicalStock):
		self.Entered_ChemicalName=Entered_ChemicalName
		self.Entered_ChemicalStock=Entered_ChemicalStock

	def Validate_ChemicalName(self, Entered_ChemicalName):
		ChemicalName_Format = "^[A-Za-z0-9\)\(\- ]{1,50}$" #checks that chemical name includes alphabet, numbers, and brackets or a space and is between 1 and 50 characters.
		if re.fullmatch(ChemicalName_Format, self.Entered_ChemicalName): #checks if entered chemical name matches the correct format
			chemicalName_format_valid=True
		else:
			chemicalName_format_valid=False #any other format, including an empty value, would be revoked

		return chemicalName_format_valid

	def validate_ChemicalStock(self, Entered_ChemicalStock):
		try:
			if int(self.Entered_ChemicalStock) >=1 and int(self.Entered_ChemicalStock) <=2000: #checks if passed in chemical stock value is between 1 and 2000
				ChemicalStock_format_valid=True
		except:				
			ChemicalStock_format_valid=False #any other format, including an empty value, would be revoked

		return ChemicalStock_format_valid
	

class Location_get_values():
	def __init__(self, LocationConfirm, Entered_EquipmentName, Entered_Stock, Entered_EquipmentID, Entered_Location):
		self.LocationConfirm=LocationConfirm
		self.Entered_EquipmentName=Entered_EquipmentName
		self.Entered_Stock=Entered_Stock
		self.Entered_EquipmentID=Entered_EquipmentID
		self.Entered_Location=Entered_Location

	def add_in_location(self):
		conn = sqlite3.connect("Command_Lab.db") #creates or connects to the database
		c=conn.cursor() #creates cursor

		c.execute("""
			SELECT Equipment.Equipment_Name, Equipment_Location.Equipment_Stock, Equipment.Equipment_ID FROM Equipment
			INNER JOIN Equipment_Location ON Equipment_Location.Equipment_ID = Equipment.Equipment_ID
			WHERE Location_ID=(?)
			""", (self.LocationConfirm)) #gets all the values that exist in the passed-in LocationID as well as the corresponding stock in that location

		records=c.fetchall()

		conn.commit() #commits changes
		conn.close() #closes connection to database	
		return records
	
	def update_Location_db(self):
		conn = sqlite3.connect("Command_Lab.db") #creates or connects to the database
		c=conn.cursor() #creates cursor

		c.execute('UPDATE Equipment_Location SET Equipment_Stock=? WHERE Location_ID=? AND Equipment_ID=?', (self.Entered_Stock, self.Entered_Location, self.Entered_EquipmentID)) #passes in the new equipment stock value based on the passed-in equipment ID, Location_ID

		conn.commit() #commits changes
		conn.close() #closes connection to database

	def delete_from_Location_db(self):

		conn = sqlite3.connect("Command_Lab.db") #creates or connects to the database
		c=conn.cursor() #creates cursor
		
		c.execute('DELETE from Equipment_Location WHERE Location_ID=? AND Equipment_ID=?', (self.Entered_Location, self.Entered_EquipmentID)) #passes in the new equipment stock value based on the passed-in equipment ID, Location_ID

		conn.commit() #commits changes
		conn.close() #closes connection to database	

	def add_to_Location_db(self):

		conn = sqlite3.connect("Command_Lab.db") ##creates or connects to the database
		c=conn.cursor() #creates cursor

		# Add New Record
		c.execute("INSERT INTO Equipment_Location VALUES (:Location_ID, :Equipment_ID, :Equipment_Stock)", #inserts a new record into the equipment location table using the validated values
			{
				"Location_ID" : self.Entered_Location,
				"Equipment_ID" : self.Entered_EquipmentID,
				"Equipment_Stock" : self.Entered_Stock
			})

		conn.commit() #commits changes
		conn.close() #closes connection to database		

	def get_equipment_inventory(self):

		conn = sqlite3.connect("Command_Lab.db") ##creates or connects to the database
		c=conn.cursor() #creates cursor

		c.execute("""
			SELECT Equipment.Equipment_Name, Equipment_Location.Equipment_Stock FROM Equipment
			INNER JOIN Equipment_Location ON Equipment_Location.Equipment_ID = Equipment.Equipment_ID""") #gets all the inventory in all locations for the purpose of equipment statistics

		records=c.fetchall()

		conn.commit() #commits changes
		conn.close() #closes connection to database	
		return records


	def get_equipment_stats(self):
		def merge_sort(data):
			if len(data) > 1:
				half = len(data) // 2 #splits the list in two until the list is completely split into single units
				left = data[:half]
				right = data[half:]
				if isinstance(data, np.ndarray):
					left = left.copy() #because data is a numpy array, we will use copies of the data
					right = right.copy()
				merge_sort(left) #passes the left side of the split table back into the merge_sort function to be split again
				merge_sort(right) #same here, but for the right side of the list this time

				a = 0 # 'a' and 'b' tracks the two halves
				b = 0
				c = 0 # 'c' tracks through the main list
		        
				while a < len(left) and b < len(right): 
					if left[a][1] <= right[b][1]: #if the value on the left is smaller than the value on the right, the left one moves up one.
						data[c][1] = left[a][1]
						a=a+ 1 #increments 'a'
					else:
						data[c][1] = right[b][1]
						b=b+1 
					c=c+1 #moves on in the main list

				while a < len(left): #continues on for the rest of the list on the left side
					data[c][1] = left[a][1]
					a=a+ 1
					c=c+1

				while b < len(right): #continues on for the rest of the list on the right side
					data[c][1]=right[b][1]
					b=b+1 
					c=c+1



		u2=Location_get_values("", "", "", "", "") #creates an instance of the class get_values under the object self
		u2.records = u2.get_equipment_inventory() #grabs values from location and equipment tables
		for idx, (x,y) in enumerate(u2.records):
			u2.records[idx]=(x, int(y)) #changes the stock value to an integer
		array=[list(item) for item in u2.records] #turns the list of tuples into a 2d list

		merge_sort(array) #passes it into merge sort recursive algorithm until it is fully sorted by inventory

		return array

class Equipment_Location_Validate(Location_get_values):
	def __init__(self, Entered_EquipmentLocation, Entered_EquipmentName, Entered_EquipmentStock,Entered_Consumable, Entered_EquipmentID):
		self.Entered_EquipmentLocation=Entered_EquipmentLocation
		self.Entered_EquipmentName=Entered_EquipmentName
		self.Entered_EquipmentStock=Entered_EquipmentStock
		self.Entered_Consumable=Entered_Consumable
		self.Entered_EquipmentID=Entered_EquipmentID

	def validate_Location(self, Entered_EquipmentLocation):
		Location_Format = "^[1-7]$" #checks that location is included in the seven science labs

		if re.fullmatch(Location_Format, self.Entered_EquipmentLocation): #checks if entered location matches the correct format
			LocationFormat_Valid=True
		else:
			LocationFormat_Valid=False #any other format, including an empty value, would be revoked

		return LocationFormat_Valid

	def validate_EquipmentName(self, Entered_EquipmentName):
		equipmentName_Format = "^[A-Za-z0-9\._\-\)\( )]{1,50}$" #checks that equipment name includes alphabet, numbers, and brackets or a space and is between 1 and 50 characters.

		if re.fullmatch(equipmentName_Format, self.Entered_EquipmentName): #checks if entered equipment name matches the correct format
			equipmentName_format_valid=True
		else:
			equipmentName_format_valid=False #any other format, including an empty value, would be revoked

		return equipmentName_format_valid

	def validate_EquipmentStock(self,Entered_EquipmentStock):
		if int(Entered_EquipmentStock) >=1 and int(Entered_EquipmentStock) <=1000: #checks that the entered stock is between 1 and 100
			EquipmentStock_format_valid=True
		else:
			EquipmentStock_format_valid=False #any other format, including an empty value, would be revoked


		return EquipmentStock_format_valid

	def validate_Consumable(self,Entered_Consumable):
		Consumable_Format="^[1|0]$"

		if re.fullmatch(Consumable_Format, self.Entered_Consumable): #checks if entered Consumable value matches the correct format
			Consumable_format_valid=True
		else:
			Consumable_format_valid=False #any other format, including an empty value, would be revoked

		return Consumable_format_valid

	def validate_equipmentID(self, Entered_EquipmentID):
		conn = sqlite3.connect("Command_Lab.db") ##creates or connects to the database
		c=conn.cursor() #creates cursor

		records=c.execute("SELECT * FROM Equipment WHERE Equipment_ID=(?)", (self.Entered_EquipmentID,)) #selects any record that matches the provided equipment ID. If this fails, that means that the equipment does not exist

		if len(records.fetchall())>0: 
			EquipmentID_Valid=True
		else:
			EquipmentID_Valid=False

		conn.commit() #commits changes
		conn.close() #closes connection to database	

		return EquipmentID_Valid



class Supplier():
	def __init__(self,Requested_Stock,Supplier_Email, Entered_EquipmentID, Entered_SupplierName):
		self.Requested_Stock=Requested_Stock
		self.Supplier_Email=Supplier_Email
		self.Entered_EquipmentID=Entered_EquipmentID
		self.Entered_SupplierName=Entered_SupplierName
		
	def validate_Requested_Stock(self, Requested_Stock):
		try:
			if int(self.Requested_Stock) >=1 and int(self.Requested_Stock) <=100: #checks that the entered stock is between 1 and 100
				EquipmentStock_format_valid=True
		except:				
			EquipmentStock_format_valid=False #any other format, including an empty value, would be revoked

		return EquipmentStock_format_valid

	def validate_supplier_email(self, Supplier_Email):
		SupplierEmail_Format="([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
	#checks that the supplier email has a certain set of alphanumeric characters, followed by (possibly) a full stop, then another series of alphanumeric characters (for the email domain), followed by the ending of the email address. It must have an '@'
		if re.fullmatch(SupplierEmail_Format, self.Supplier_Email): #checks if entered value matches the correct format
			SupplierEmail_Format_Valid=True
		else:
			SupplierEmail_Format_Valid=False #any other format, including an empty value, would be revoked

		return SupplierEmail_Format_Valid

	def validate_equipmentID(self, Entered_EquipmentID):
		conn = sqlite3.connect("Command_Lab.db") ##creates or connects to the database
		c=conn.cursor() #creates cursor

		records=c.execute("SELECT * FROM Equipment WHERE Equipment_ID=(?)", (self.Entered_EquipmentID,)) #selects any record that matches the provided equipment ID. If this fails, that means that the equipment does not exist

		if len(records.fetchall())>0: 
			EquipmentID_Valid=True
		else:
			EquipmentID_Valid=False

		conn.commit() #commits changes
		conn.close() #closes connection to database	

		return EquipmentID_Valid

	def validate_SupplierName(self, Entered_SupplierName):
		if len(self.Entered_SupplierName)>0 and len(self.Entered_SupplierName)<=40: #checks that the length of the supplier name is greater than 0 but less than or equal to 40 characters
			SupplierName_Valid=True
		else:
			SupplierName_Valid=False

		return SupplierName_Valid

	def select_Supplies(self, Requested_Stock):

		conn = sqlite3.connect("Command_Lab.db") ##creates or connects to the database
		c=conn.cursor() #creates cursor

		c.execute("""
			SELECT Equipment.Equipment_Name, Equipment_Supplier.Supplier_Email, Equipment_Location.Equipment_Stock FROM Equipment
			INNER JOIN Equipment_Supplier, Equipment_Location ON Equipment.Equipment_ID = Equipment_Supplier.Equipment_ID = Equipment_Location.Equipment_Stock
			WHERE Equipment_Location.Equipment_Stock<=(?) 
			""", (int(self.Requested_Stock),)) #returns all the equiment that have a stock at or below the threshold number

		records=c.fetchall()
		conn.commit() #commits changes
		conn.close() #closes connection to database	
		return records

	def insert_new_Supplier(self,Supplier_Email, Entered_EquipmentID, Entered_SupplierName):
		conn = sqlite3.connect("Command_Lab.db") ##creates or connects to the database
		c=conn.cursor() #creates cursor

		# Add New Record
		c.execute("INSERT INTO Supplier_Details VALUES (:Supplier_Email, :Supplier_Name)", #inserts the new record of a supplier with the validated supplier values
			{
				"Supplier_Email" : self.Supplier_Email,
				"Supplier_Name" : self.Entered_SupplierName
			})

		# Add New Record
		c.execute("INSERT INTO Equipment_Supplier VALUES (:Equipment_ID, :Supplier_Email)", #adds the new equipment linked to the supplier
			{
				"Equipment_ID" : self.Entered_EquipmentID,
				"Supplier_Email" : self.Supplier_Email
			})


		conn.commit() #commits changes
		conn.close() #closes connection to database		