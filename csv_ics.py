import pandas as pd
from icalendar import Calendar, Event
from datetime import datetime
import pytz
import tkinter as tk
from tkinter import filedialog, messagebox

def convert_csv_to_ics(csv_file, timezone="Africa/Johannesburg"):
    try:
        df = pd.read_csv(csv_file)

        required_columns = ["Subject", "Start Date", "Start Time", "End Date", "End Time", "Description"]
        if not all(col in df.columns for col in required_columns):
            messagebox.showerror("Error", f"CSV file must have these columns: {', '.join(required_columns)}")
            return
        
        cal = Calendar()
        tz = pytz.timezone(timezone)

        for _, row in df.iterrows():
            event = Event()
            start_str = f"{row['Start Date']} {row['Start Time']}"
            end_str = f"{row['End Date']} {row['End Time']}"
            
            start_dt = datetime.strptime(start_str, "%d/%m/%Y %H:%M").replace(tzinfo=tz)
            end_dt = datetime.strptime(end_str, "%d/%m/%Y %H:%M").replace(tzinfo=tz)

            event.add("summary", row["Subject"])
            event.add("dtstart", start_dt)
            event.add("dtend", end_dt)
            event.add("description", row["Description"])
            
            cal.add_component(event)

        ics_file = csv_file.replace(".csv", ".ics")
        with open(ics_file, "wb") as f:
            f.write(cal.to_ical())

        messagebox.showinfo("Success", f"ICS file saved:\n{ics_file}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        convert_csv_to_ics(file_path)

# GUI Setup
root = tk.Tk()
root.title("CSV to ICS Converter")
root.geometry("400x200")

label = tk.Label(root, text="Select a CSV file to convert to ICS", font=("Arial", 12))
label.pack(pady=20)

btn_select = tk.Button(root, text="Choose CSV File", command=select_file, font=("Arial", 12), padx=10, pady=5)
btn_select.pack()

root.mainloop()