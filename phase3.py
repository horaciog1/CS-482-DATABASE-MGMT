# Horacio Gonzalez 
# Project Phase 3
# Accesing databases through an app
# CS 482 Database Mgmt

import tkinter as tk
from tkinter import simpledialog
import mysql.connector

class DatabaseManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Manager")
        
        # Database connection parameters
        self.host = '127.0.0.1'
        self.user = 'root'
        self.database = 'Project'
        self.password = '1436352Hg'
        
        # Connect to the database
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            database=self.database,
            password=self.password
        )
        self.cursor = self.connection.cursor()
        
        # Create main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=20, pady=20)
        
        # Table name field
        self.table_name_label = tk.Label(self.main_frame, text="Table Name:")
        self.table_name_label.grid(row=0, column=0)
        self.table_name_entry = tk.Entry(self.main_frame)
        self.table_name_entry.grid(row=0, column=1)
        
        # Buttons
        self.retrieve_button = tk.Button(self.main_frame, text="Retrieve All Data", command=self.retrieve_data)
        self.retrieve_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.average_button = tk.Button(self.main_frame, text="Calculate Average", command=self.calculate_average)
        self.average_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.insert_button = tk.Button(self.main_frame, text="Insert Data", command=self.insert_data)
        self.insert_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.delete_button = tk.Button(self.main_frame, text="Delete Data", command=self.delete_data)
        self.delete_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    def retrieve_data(self):
        table_name = self.table_name_entry.get()
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.show_output("Data Retrieved", self.format_output(data))
    
    def calculate_average(self):
        table_name = self.table_name_entry.get()
        column_name = simpledialog.askstring("Input", f"Enter column name for table '{table_name}':")
        if column_name:
            query = f"SELECT AVG({column_name}) FROM {table_name}"
            self.cursor.execute(query)
            average = self.cursor.fetchone()[0]
            self.show_output("Average", f"The average of {column_name} is {average:.2f}")
    
    def insert_data(self):
        table_name = self.table_name_entry.get()
        query = f"DESCRIBE {table_name}"
        self.cursor.execute(query)
        columns = [column[0] for column in self.cursor.fetchall()]
        
        data = {}
        for column in columns:
            value = simpledialog.askstring("Input", f"Enter value for column '{column}':")
            if value:
                data[column] = value
        
        try:
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(columns))})"
            self.cursor.execute(query, tuple(data.values()))
            self.connection.commit()
            self.show_output("Success", "Data inserted successfully")
        except mysql.connector.Error as err:
            self.show_output("Error", f"Failed to insert data: {err}")
    
    def delete_data(self):
        table_name = self.table_name_entry.get()
        query = f"DESCRIBE {table_name}"
        self.cursor.execute(query)
        columns = [column[0] for column in self.cursor.fetchall()]
        
        conditions = {}
        for column in columns:
            value = simpledialog.askstring("Input", f"Enter value for column '{column}' to delete:")
            if value:
                conditions[column] = value
        
        try:
            condition_str = ' AND '.join([f"{column} = %s" for column in conditions.keys()])
            query = f"DELETE FROM {table_name} WHERE {condition_str}"
            self.cursor.execute(query, tuple(conditions.values()))
            self.connection.commit()
            self.show_output("Success", "Data deleted successfully")
        except mysql.connector.Error as err:
            self.show_output("Error", f"Failed to delete data: {err}")
    
    def show_output(self, title, message):
        output_window = tk.Toplevel(self.root)
        output_window.title(title)
        
        output_text = tk.Text(output_window, font=("Courier", 15))
        output_text.pack(expand=True, fill=tk.BOTH)
        
        # Insert formatted output into the text widget
        output_text.insert(tk.END, message)
        
        # Disable editing
        output_text.configure(state=tk.DISABLED)
        
        # Split the message into rows
        rows = message.split('\n')
        
        # Calculate the number of characters in the x-axis
        num_chars_x = max(len(row) for row in rows)
        
        # Set minimum window size
        min_width = 500
        min_height = 200
        
        # Calculate window size based on the number of characters
        xfactor = 9
        window_width = max(min_width, num_chars_x * xfactor)
        window_height = min_height
        
        output_window.geometry(f"{window_width}x{window_height}")
    
    def format_output(self, data):
        if not data:
            return "No data found."

        # Get column names
        column_names = [desc[0] for desc in self.cursor.description]

        # Find maximum width for each column
        column_widths = [max(len(str(value)) for value in column) for column in zip(*data, column_names)]

        # Create separator
        separator = "+"
        for width in column_widths:
            separator += "-" * (width + 2) + "+"
        separator += "\n"

        # Format header
        header = "| "
        for name, width in zip(column_names, column_widths):
            header += f"{name.ljust(width)} | "
        header += "\n"

        # Format data rows
        rows = ""
        for row in data:
            rows += "| "
            for value, width in zip(row, column_widths):
                rows += f"{str(value):<{width}} | "
            rows += "\n"

        return separator + header + separator + rows + separator

# Create the main window
root = tk.Tk()
app = DatabaseManagerApp(root)
root.mainloop()
