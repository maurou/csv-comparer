import pandas as pd
import tkinter as tk
from tkinter import filedialog
from pandas.errors import ParserError
import time

# Variable to store the last browsed folder
last_browsed_folder = "/"

def browse_file(entry):
    global last_browsed_folder  # Declare as a global variable
    try:
        filename = filedialog.askopenfilename(initialdir=last_browsed_folder, title="Select a CSV file", filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
        
        if filename:
            last_browsed_folder = filename.rsplit('/', 1)[0]
            entry.delete(0, tk.END)
            entry.insert(0, filename)
    except Exception as e:
        show_error("File Selection Error", str(e))

def browse_folder(entry):
    global last_browsed_folder  # Declare as a global variable
    folder = filedialog.askdirectory(initialdir=last_browsed_folder, title="Select a Folder")
    if folder:
        last_browsed_folder = folder
        entry.config(state=tk.NORMAL)
        entry.delete(0, tk.END)
        entry.insert(0, folder)
        entry.config(state=tk.DISABLED)

def compare_csv(file1_entry, file2_entry, output_folder_entry, filename_entry):
    try:
        file1 = file1_entry.get()
        file2 = file2_entry.get()
        output_folder = output_folder_entry.get()
        filename = filename_entry.get()

        # If filename is not provided or empty, use the default format
        if not filename:
            timestamp = time.strftime("%Y%m%d%H%M%S")
            filename = f"export_{timestamp}.csv"
        else:
            # If a custom filename is provided, update the timestamp in the default format
            timestamp = time.strftime("%Y%m%d%H%M%S")
            filename_entry.delete(0, tk.END)
            filename_entry.insert(0, f"export_{timestamp}.csv")

        # Read CSV files into Pandas DataFrames
        df1 = pd.read_csv(file1, sep=';')
        df2 = pd.read_csv(file2, sep=';')

        # Merge the dataframes with indicator set to True
        merged_df = pd.merge(df1, df2, how='outer', indicator=True)

        # Select rows where the indicator is only in 'right_only'
        new_values = merged_df[merged_df['_merge'] == 'right_only'].drop(columns=['_merge'])

        # Display new values on the screen
        #result_text.config(state=tk.NORMAL)
        #result_text.delete(1.0, tk.END)
        #result_text.insert(tk.END, "Different values:\n")
        #result_text.insert(tk.END, new_values.to_string(index=False))
        #result_text.config(state=tk.DISABLED)

        # Construct the full output file path
        output_file = f"{output_folder}/{filename}"

        # Export new values to a new CSV file
        new_values.to_csv(output_file, index=False)
        result_text.config(state=tk.NORMAL)
        result_text.insert(tk.END, f"\nDifferent values exported to {output_file}")
        result_text.config(state=tk.DISABLED)
    except ParserError as pe:
        show_error("CSV Parsing Error", f"Error reading CSV file: {str(pe)}")
    except Exception as e:
        show_error("Comparison Error", str(e))

def show_error(title, message):
    tk.messagebox.showerror(title, message)

# GUI setup
root = tk.Tk()
root.title("CSV Comparer")

# File 1
file1_label = tk.Label(root, text="Old CSV:")
file1_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
file1_entry = tk.Entry(root, width=40)
file1_entry.grid(row=0, column=1, padx=5, pady=5)
file1_button = tk.Button(root, text="Browse", command=lambda: browse_file(file1_entry))
file1_button.grid(row=0, column=2, padx=5, pady=5)

# File 2
file2_label = tk.Label(root, text="New CSV:")
file2_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
file2_entry = tk.Entry(root, width=40)
file2_entry.grid(row=1, column=1, padx=5, pady=5)
file2_button = tk.Button(root, text="Browse", command=lambda: browse_file(file2_entry))
file2_button.grid(row=1, column=2, padx=5, pady=5)

# Output Folder
output_folder_label = tk.Label(root, text="Output Folder:")
output_folder_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
output_folder_entry = tk.Entry(root, width=40, state=tk.DISABLED)
output_folder_entry.grid(row=2, column=1, padx=5, pady=5)
output_folder_button = tk.Button(root, text="Browse", command=lambda: browse_folder(output_folder_entry))
output_folder_button.grid(row=2, column=2, padx=5, pady=5)

# Output Filename
filename_label = tk.Label(root, text="Filename:")
filename_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
filename_entry = tk.Entry(root, width=40)
filename_entry.grid(row=3, column=1, padx=5, pady=5)
filename_entry.insert(0, f"export_{time.strftime('%Y%m%d%H%M%S')}.csv")  # Default filename with timestamp

# Compare Button
compare_button = tk.Button(root, text="Compare and Export", command=lambda: compare_csv(file1_entry, file2_entry, output_folder_entry, filename_entry))
compare_button.grid(row=4, column=1, pady=10)

# Result Text
result_text = tk.Text(root, height=10, width=60, state=tk.DISABLED)
result_text.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
