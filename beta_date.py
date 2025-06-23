from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
import os

# Initialize GUI
root = tk.Tk()
root.title("Pokémon R/S Live Battery Seed Searcher")

# Set window icon if available
try:
    icon_path = os.path.join("icon", "icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
except Exception as e:
    print(f"Couldn't set window icon: {e}")

def calculate_multiple_seeds():
    try:
        # Get inputs
        year = int(year_entry.get())
        month = int(month_entry.get())
        day = int(day_entry.get())
        hour = int(hour_entry.get())
        minute = int(minute_entry.get())

        # Clear previous results
        for row in result_tree.get_children():
            result_tree.delete(row)

        # Create base datetime
        base_datetime = datetime(year, month, day, hour, minute)
        
        # Generate 10 consecutive minutes
        datetimes = [base_datetime + timedelta(minutes=i) for i in range(10)]
        
        # Calculate and display seeds
        for dt in datetimes:
            reference_date = datetime(1999, 12, 31)
            if dt.year > 2000:
                days_difference = (dt - reference_date).days - 366
            else:
                days_difference = (dt - reference_date).days
            
            h = int(dt.strftime("%H"), 16)
            m = int(dt.strftime("%M"), 16)
            
            total = (24 * 60 * days_difference) + (60 * h) + m
            seed = (total >> 16) ^ (total & 0xFFFF)
            
            result_tree.insert("", "end", values=(dt.strftime("%H:%M"), f"{seed:04X}"))

    except ValueError as e:
        result_label.config(text=f"Error: {str(e)}")

# Input frame
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack()

# Input fields
tk.Label(input_frame, text="Year:").grid(row=0, column=0, sticky="e")
year_entry = tk.Entry(input_frame, width=5)
year_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Month:").grid(row=1, column=0, sticky="e")
month_entry = tk.Entry(input_frame, width=5)
month_entry.grid(row=1, column=1)

tk.Label(input_frame, text="Day:").grid(row=2, column=0, sticky="e")
day_entry = tk.Entry(input_frame, width=5)
day_entry.grid(row=2, column=1)

tk.Label(input_frame, text="Hour (0-23):").grid(row=0, column=2, sticky="e")
hour_entry = tk.Entry(input_frame, width=5)
hour_entry.grid(row=0, column=3)

tk.Label(input_frame, text="Minute (0-59):").grid(row=1, column=2, sticky="e")
minute_entry = tk.Entry(input_frame, width=5)
minute_entry.grid(row=1, column=3)

# Calculate button
tk.Button(input_frame, text="Generate Seeds", command=calculate_multiple_seeds).grid(row=2, column=2, columnspan=2)

# Results frame
results_frame = tk.Frame(root, padx=10, pady=10)
results_frame.pack(fill="both", expand=True)

# Results treeview
result_tree = ttk.Treeview(results_frame, columns=("Time", "Seed"), show="headings", height=10)
result_tree.heading("Time", text="Time (HH:MM)")
result_tree.heading("Seed", text="Seed")
result_tree.column("Time", width=100, anchor="center")
result_tree.column("Seed", width=100, anchor="center")
result_tree.pack(fill="both", expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=result_tree.yview)
scrollbar.pack(side="right", fill="y")
result_tree.configure(yscrollcommand=scrollbar.set)

root.mainloop()