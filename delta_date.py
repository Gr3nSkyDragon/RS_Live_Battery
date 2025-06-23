from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
import os
import sys
import tempfile

# UI Color Variables
main_background_color = '#5D4A8F'     # Main background
button_color = '#7761AB'              # Color for button
button_text_color = 'white'           # Button text color
input_field_text_color = 'white'      # Input field label text color
results_background = '#5D4A8F'          # Results area background

# Style Configuration
placeholder_style = {
    'foreground': '#a0a0a0',  # Medium gray
    'font': ('Helvetica', 10, 'italic'),
    'relief': 'flat',
    'borderwidth': 1
}

normal_style = {
    'foreground': 'black',
    'font': ('Helvetica', 10),
    'relief': 'flat',
    'borderwidth': 1
}

def create_entry_with_placeholder(parent, row, col, default='0'):
    entry = tk.Entry(parent, width=5)
    entry.insert(0, default)
    entry.config(**placeholder_style)
    
    def on_focus_in(event):
        if entry.get() == default and entry.cget('foreground') == placeholder_style['foreground']:
            entry.delete(0, tk.END)
            entry.config(**normal_style)
    
    def on_focus_out(event):
        if not entry.get().strip():
            entry.insert(0, default)
            entry.config(**placeholder_style)
    
    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)
    entry.grid(row=row, column=col, padx=2, pady=2)
    return entry

def set_window_icon(root):
    """Handle icon setting for both development and compiled EXE"""
    try:
        if getattr(sys, 'frozen', False):
            with open(os.path.join(sys._MEIPASS, "icon", "icon.ico"), "rb") as icon_file:
                icon_data = icon_file.read()
            temp_icon = os.path.join(tempfile.gettempdir(), "temp_icon.ico")
            with open(temp_icon, "wb") as f:
                f.write(icon_data)
            root.iconbitmap(temp_icon)
        else:
            icon_path = os.path.join("icon", "icon.ico")
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
    except Exception as e:
        print(f"Couldn't set window icon: {e}")

def calculate_multiple_seeds(event=None):
    # Dictionary of all entry fields and their validation ranges
    entries = {
        'year': {'widget': year_entry, 'min': 0, 'max': 9999},
        'month': {'widget': month_entry, 'min': 1, 'max': 12},
        'day': {'widget': day_entry, 'min': 1, 'max': 31},
        'hour': {'widget': hour_entry, 'min': 0, 'max': 23},
        'minute': {'widget': minute_entry, 'min': 0, 'max': 59},
        'seeds': {'widget': seeds_entry, 'min': 1, 'max': 1000}
    }
    
    # Auto-fill empty fields with defaults and validate
    values = {}
    for field, config in entries.items():
        entry = config['widget']
        current_text = entry.get()
        
        # If field has placeholder styling but non-default value
        if entry.cget('foreground') == placeholder_style['foreground'] and current_text != '0':
            entry.config(foreground='black', font=('Helvetica', 10))  # Convert to real input
        
        # Get and validate value
        try:
            value = int(entry.get())
            if not (config['min'] <= value <= config['max']):
                raise ValueError(f"{field} must be between {config['min']} and {config['max']}")
            values[field] = value
        except ValueError as e:
            # Highlight invalid field
            entry.config(background='#ffdddd')
            entry.after(1000, lambda e=entry: e.config(background='white'))
            result_tree.delete(*result_tree.get_children())  # Clear previous results
            result_tree.insert("", "end", values=("Error:", str(e)))
            return
    
    try:
        # Clear previous results and errors
        result_tree.delete(*result_tree.get_children())
        
        # Create base datetime with proper validation
        try:
            base_datetime = datetime(
                values['year'],
                values['month'],
                values['day'],
                values['hour'],
                values['minute']
            )
        except ValueError:
            # Handle invalid dates by using the last valid day of the month
            import calendar
            last_day = calendar.monthrange(values['year'], values['month'])[1]
            base_datetime = datetime(
                values['year'],
                values['month'],
                min(values['day'], last_day),
                values['hour'],
                values['minute']
            )
            day_entry.delete(0, tk.END)
            day_entry.insert(0, str(last_day))
            day_entry.config(foreground='black')
        
        # Generate requested number of consecutive minutes
        num_seeds = values['seeds']
        datetimes = [base_datetime + timedelta(minutes=i) for i in range(num_seeds)]
        
        # Calculate and display seeds
        for i, dt in enumerate(datetimes):
            reference_date = datetime(1999, 12, 31)
            if dt.year > 2000:
                days_difference = (dt - reference_date).days - 366
            else:
                days_difference = (dt - reference_date).days
            
            # Convert hours/minutes to hexadecimal values (this is key)
            h = int(dt.strftime("%H"), 16)
            m = int(dt.strftime("%M"), 16)
            
            # Calculate total minutes and seed
            total = (24 * 60 * days_difference) + (60 * h) + m
            seed = (total >> 16) ^ (total & 0xFFFF)
            
            # Alternate row colors
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            result_tree.insert("", "end", 
                            values=(dt.strftime("%H:%M"), f"{seed:04X}"), 
                            tags=(tag,))
    
    except Exception as e:
        result_tree.insert("", "end", values=("Error:", str(e)))
        
# Initialize GUI
root = tk.Tk()
root.title("Pokémon R/S Live Battery Seed Searcher")

# Set background color using variable
root.configure(bg=main_background_color)

# Input frame with matching background
input_frame = tk.Frame(root, padx=10, pady=10, bg=main_background_color)
input_frame.pack()

# Create entry fields with proper placeholders
tk.Label(input_frame, text="Year:", bg=main_background_color, fg=input_field_text_color).grid(row=0, column=0, sticky="e")
year_entry = create_entry_with_placeholder(input_frame, 0, 1, '2000')

tk.Label(input_frame, text="Month:", bg=main_background_color, fg=input_field_text_color).grid(row=1, column=0, sticky="e")
month_entry = create_entry_with_placeholder(input_frame, 1, 1, '1')

tk.Label(input_frame, text="Day:", bg=main_background_color, fg=input_field_text_color).grid(row=2, column=0, sticky="e")
day_entry = create_entry_with_placeholder(input_frame, 2, 1, '1')

tk.Label(input_frame, text="Hour (0-23):", bg=main_background_color, fg=input_field_text_color).grid(row=0, column=2, sticky="e")
hour_entry = create_entry_with_placeholder(input_frame, 0, 3, '0')

tk.Label(input_frame, text="Minute (0-59):", bg=main_background_color, fg=input_field_text_color).grid(row=1, column=2, sticky="e")
minute_entry = create_entry_with_placeholder(input_frame, 1, 3, '0')

# New Seeds Count field
tk.Label(input_frame, text="Seeds (1+):", bg=main_background_color, fg=input_field_text_color).grid(row=2, column=2, sticky="e")
seeds_entry = create_entry_with_placeholder(input_frame, 2, 3, '10')

# Calculate button with theme colors
calculate_button = tk.Button(
    input_frame, 
    text="Generate Seeds", 
    command=calculate_multiple_seeds,
    bg=button_color,
    fg=button_text_color,
    activebackground='#6E5BA8',
    activeforeground=button_text_color,
    relief='flat'
)
calculate_button.grid(row=3, column=2, columnspan=2, pady=5)

# Results frame with specified background
results_frame = tk.Frame(root, padx=10, pady=10, bg=results_background)
results_frame.pack(fill="both", expand=True)

# Create style for Treeview
style = ttk.Style()
style.theme_use('default')

# Configure Treeview
style.configure("Treeview",
    background="#ffffff",
    foreground="#000000",
    rowheight=25,
    fieldbackground="#ffffff",
    bordercolor="#d3d3d3",
    borderwidth=1,
    font=('Helvetica', 10)
)
style.configure("Treeview.Heading",
    font=('Helvetica', 10, 'bold'),
    background="#f0f0f0",
    relief="flat"
)
style.map('Treeview',
    background=[('selected', '#0078d7')],
    foreground=[('selected', 'white')]
)

# Create Treeview
result_tree = ttk.Treeview(
    results_frame,
    columns=("Time", "Seed"),
    show="headings",
    height=10,
    style="Treeview",
    selectmode="browse"
)

# Configure tags for alternating row colors
result_tree.tag_configure('oddrow', background='#f0f0f0')
result_tree.tag_configure('evenrow', background='#ffffff')

# Configure columns
result_tree.heading("Time", text="Time (HH:MM)")
result_tree.heading("Seed", text="Seed")
result_tree.column("Time", width=100, anchor="center")
result_tree.column("Seed", width=100, anchor="center")

# Display results with scrollbar
scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=result_tree.yview)
scrollbar.pack(side="right", fill="y")
result_tree.configure(yscrollcommand=scrollbar.set)
result_tree.pack(fill="both", expand=True)

# Set window icon and final UI adjustments
set_window_icon(root)
root.after(100, lambda: [e.config(bg='white') for e in 
                       [year_entry, month_entry, day_entry, hour_entry, minute_entry, seeds_entry]])

# Bind Enter keys
root.bind('<Return>', calculate_multiple_seeds)
root.bind('<KP_Enter>', calculate_multiple_seeds)
year_entry.focus_set()

root.mainloop()