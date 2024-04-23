import tkinter as tk
from tkinter import messagebox, Toplevel
import mysql.connector
from prettytable import PrettyTable

class InsertDataWindow:
    def __init__(self, parent, table_name, columns):
        self.parent = parent
        self.table_name = table_name
        self.columns = columns
        
        self.window = Toplevel(parent)
        self.window.title("Insert Data")
        
        self.entry_vars = {}
        self.labels = {}
        
        for idx, column in enumerate(columns):
            label = tk.Label(self.window, text=column)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky="w")
            self.labels[column] = label
            
            entry_var = tk.StringVar()
            entry = tk.Entry(self.window, textvariable=entry_var)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="e")
            self.entry_vars[column] = entry_var
        
        insert_button = tk.Button(self.window, text="Insert", command=self.insert_data)
        insert_button.grid(row=len(columns), columnspan=2, padx=5, pady=10)
    
    def insert_data(self):
        data = {column: entry_var.get() for column, entry_var in self.entry_vars.items()}
        try:
            query = f"INSERT INTO {self.table_name} ({', '.join(self.columns)}) VALUES ({', '.join(['%s']*len(self.columns))})"
            self.parent.cursor.execute(query, tuple(data.values()))
            self.parent.connection.commit()
            messagebox.showinfo("Success", "Data inserted successfully")
            self.window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to insert data: {err}")

class DeleteDataWindow:
    def __init__(self, parent, table_name, columns):
        self.parent = parent
        self.table_name = table_name
        self.columns = columns
        
        self.window = Toplevel(parent)
        self.window.title("Delete Data")
        
        self.entry_vars = {}
        self.labels = {}
        
        for idx, column in enumerate(columns):
            label = tk.Label(self.window, text=column)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky="w")
            self.labels[column] = label
            
            entry_var = tk.StringVar()
            entry = tk.Entry(self.window, textvariable=entry_var)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="e")
            self.entry_vars[column] = entry_var
        
        delete_button = tk.Button(self.window, text="Delete", command=self.delete_data)
        delete_button.grid(row=len(columns), columnspan=2, padx=5, pady=10)
    
    def delete_data(self):
        conditions = {column: entry_var.get() for column, entry_var in self.entry_vars.items()}
        try:
            condition_str = ' AND '.join([f"{column} = %s" for column in conditions.keys()])
            query = f"DELETE FROM {self.table_name} WHERE {condition_str}"
            self.parent.cursor.execute(query, tuple(conditions.values()))
            self.parent.connection.commit()
            messagebox.showinfo("Success", "Data deleted successfully")
            self.window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to delete data: {err}")

class DatabaseManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Manager")
        self.root.geometry("400x300")
        self.root.resizable(True, True)  # Allow resizing in both directions
        
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
        
        # Table name entry
        self.table_name_label = tk.Label(self.main_frame, text="Table Name:")
        self.table_name_label.grid(row=0, column=0)
        self.table_name_entry = tk.Entry(self.main_frame)
        self.table_name_entry.grid(row=0, column=1)
        
        # Column name entry
        self.column_name_label = tk.Label(self.main_frame, text="Column Name:")
        self.column_name_label.grid(row=1, column=0)
        self.column_name_entry = tk.Entry(self.main_frame)
        self.column_name_entry.grid(row=1, column=1)
        
        # Button to retrieve all data
        self.retrieve_button = tk.Button(self.main_frame, text="Retrieve All Data", command=self.retrieve_data)
        self.retrieve_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Button to calculate average
        self.average_button = tk.Button(self.main_frame, text="Calculate Average", command=self.calculate_average)
        self.average_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Button to insert data
        self.insert_button = tk.Button(self.main_frame, text="Insert Data", command=self.open_insert_window)
        self.insert_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Button to delete data
        self.delete_button = tk.Button(self.main_frame, text="Delete Data", command=self.open_delete_window)
        self.delete_button.grid(row=5, column=0, columnspan=2, pady=10)

    
    def retrieve_data(self):
        table_name = self.table_name_entry.get()
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.show_output("Data Retrieved", self.format_output(data))
    
    def calculate_average(self):
        table_name = self.table_name_entry.get()
        column_name = self.column_name_entry.get()
        query = f"SELECT AVG({column_name}) FROM {table_name}"
        self.cursor.execute(query)
        average = self.cursor.fetchone()[0]
        self.show_output("Average", f"The average of {column_name} is {average:.2f}")
    
    def open_insert_window(self):
        table_name = self.table_name_entry.get()
        query = f"DESCRIBE {table_name}"
        print("Insert Query:", query)  # Add this line for debugging
        self.cursor.execute(query)
        columns = [column[0] for column in self.cursor.fetchall()]
        InsertDataWindow(self, table_name, columns)

    def open_delete_window(self):
        table_name = self.table_name_entry.get()
        query = f"DESCRIBE {table_name}"
        print("Delete Query:", query)  # Add this line for debugging
        self.cursor.execute(query)
        columns = [column[0] for column in self.cursor.fetchall()]
        DeleteDataWindow(self, table_name, columns)

    
    def show_output(self, title, message):
        output_window = Toplevel(self.root)
        output_window.title(title)
        output_window.geometry("400x300")
        output_window.resizable(True, True)  # Allow resizing in both directions
        
        output_label = tk.Label(output_window, text=message)
        output_label.pack(expand=True, fill=tk.BOTH)
    
    def format_output(self, data):
        if not data:
            return "No data found."
        
        table = PrettyTable()
        table.field_names = [desc[0] for desc in self.cursor.description]
        table.add_rows(data)
        return str(table)

# Create the main window
root = tk.Tk()
app = DatabaseManagerApp(root)
root.mainloop()
