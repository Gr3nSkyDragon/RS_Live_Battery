import tkinter as tk
from tkinter import ttk
from datetime import datetime

def calculate_seed_hex():
    year = int(year_entry.get())
    month = int(month_entry.get())
    day = int(day_entry.get())
    hours = hour_entry.get()
    minutes = minute_entry.get()

    # Reference date (Dec 31, 1999)
    reference_date = datetime(1999, 12, 31)

    # Convert input date to a datetime object
    input_date = datetime(year, month, day)

    # Calculate the difference in days
    if year > 2000:
        # If the year is greater than 2000, subtract the days in that year
        days_difference = (input_date - reference_date).days - 366
    else:
        # If the year is 2000 or earlier, use the regular difference
        days_difference = (input_date - reference_date).days

    # Calculate the seed
    seed = (24 * 60 * days_difference + 60 * int(hours, 16) + int(minutes, 16))

    # Apply the bitwise operations
    seed = (seed >> 16) ^ (seed & 0xFFFF)

    # Convert the result to hex and remove the '0x' prefix
    result_hex = hex(seed)[2:]

    result_label.config(text=f"Seed: {result_hex}")

# GUI setup
root = tk.Tk()
root.title("Live Battery Seed Searcher")

# Year input
year_label = tk.Label(root, text="Year:")
year_label.grid(row=0, column=0, padx=10, pady=10)
year_entry = tk.Entry(root)
year_entry.grid(row=0, column=1, padx=10, pady=10)

# Month input
month_label = tk.Label(root, text="Month:")
month_label.grid(row=1, column=0, padx=10, pady=10)
month_entry = tk.Entry(root)
month_entry.grid(row=1, column=1, padx=10, pady=10)

# Day input
day_label = tk.Label(root, text="Day:")
day_label.grid(row=2, column=0, padx=10, pady=10)
day_entry = tk.Entry(root)
day_entry.grid(row=2, column=1, padx=10, pady=10)

# Hour input
hour_label = tk.Label(root, text="Hour (24-hr):")
hour_label.grid(row=3, column=0, padx=10, pady=10)
hour_entry = tk.Entry(root)
hour_entry.grid(row=3, column=1, padx=10, pady=10)

# Minute input
minute_label = tk.Label(root, text="Minute:")
minute_label.grid(row=4, column=0, padx=10, pady=10)
minute_entry = tk.Entry(root)
minute_entry.grid(row=4, column=1, padx=10, pady=10)

# Search button
search_button = tk.Button(root, text="Search", command=calculate_seed_hex)
search_button.grid(row=5, column=0, columnspan=2, pady=20)

# Result label
result_label = tk.Label(root, text="Seed: ")
result_label.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
