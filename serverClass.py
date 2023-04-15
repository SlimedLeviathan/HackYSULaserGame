# this is the start of the class, most things for the server will be stored here

import sqlite3

class Server:

    # This creates and or connects to the server specified
    def __init__(self, database):

        self.connection = None

        try:
            self.connection = sqlite3.connect(database = database)
            
            # This only prints if there aren't any errors, since it is after the possible error causing line
            print("Connection to server successful.")

        # If any errors arise they will be printed
        except sqlite3.Error as e:
            print(f"A {e} error was encountered.")

    # This connects to a different server, incase you want to use an instance of a server for a different server
    def connect(self, database):

        # Closes the previous connection
        self.connection.close

        self.connection = None

        try:
            self.connection = sqlite3.connect(database = database)

            print("Connection to server successful.")

        except sqlite3.Error as e:
            print(f"A {e} error was encountered.")

    
    # Executes whatever is put into it, is normally not accessed but can be to manually execute queries
    def executeQuery(self, query):

        self.cursor = self.connection.cursor()

        try:
            self.cursor.execute(query)
            self.connection.commit()

            return "Query executed successfully."

        except sqlite3.Error as e:
            print(e)

    def createTable(self, name, valueNames, types, constraints):

        for num in range(len(valueNames)):
            try:
                int(valueNames[num])
                valueNames[num] = int(valueNames[num])

            except:
                valueNames[num] = f"{valueNames[num]}"

        columns = [f"{valueNames[num]} {types[num]} {constraints[num]}, " for num in range(len(valueNames))]

        columns[-1] = columns[-1][:-2]

        columntext = ''

        for column in columns:
            columntext += column

        try:

            self.executeQuery(f"""create table if not exists {name} (
                {columntext}
                );""")

            return "Created Table successfully."

        except sqlite3.Error:
            pass

    # Creates a row from the tables name, any columns affected and the values themselves
    def createRow(self, table, columns, values):

        insertColumns = ""

        for column in columns:
            insertColumns += f'{column},'

        insertColumns = insertColumns[:-1]

        insertValues = ""

        for value in values:
            try:
                int(value)
                value = int(value)

            except:
                value = f"\'{value}\'"

            insertValues += f"{value},"

        insertValues = insertValues[:-1]

        try:
            self.executeQuery(f"""
            insert into {table} ({insertColumns})
            values ({insertValues});
            """)

            return 'Created row successfully.'

        except sqlite3.Error:
            pass

    # This method alters some information inside of a table based on information inside a specified column
    def alterRow(self, table, selectedColumn, selectedColumnValue, changeColumn, changeColumnValue):

        try:
            
            # This code allows us to change wether or not somehting is an string into a string if it is
            try:
                int(selectedColumnValue)
                selectedColumnValue = int(selectedColumnValue)

            except:
                selectedColumnValue = f"\'{selectedColumnValue}\'"

            try:
                int(changeColumnValue)
                changeColumnValue = int(changeColumnValue)

            except:
                changeColumnValue = f"\'{changeColumnValue}\'"

            self.executeQuery(f"""
            update {table} set {changeColumn} = {changeColumnValue} where {selectedColumn} = {selectedColumnValue};
            """)

            return "Table changed successfully"

        except sqlite3.Error:
            pass

    # deletes a row with the table name, column and the value
    def deleteRow(self, table, column, value):

        try:
            self.executeQuery(f"""
            delete from {table} where {column} = {value}
            """)

            return "Deleted row successfully."

        except sqlite3.Error:
            pass

    # if needed, the user can delete the table
    def deleteTable(self, table):
        
        try:
            self.executeQuery(f"""
            drop table {table}
            """)

            return 'Deleted table successfully.'

        except sqlite3.Error:
            pass
    
    # Gets all of the info from a sqecified table, if you want more specific searches you can put them into the execute query thing
    def getTable(self, table):
        
        self.cursor = self.connection.cursor()

        self.cursor.execute(f"SELECT * FROM {table};")
        return self.cursor.fetchall()