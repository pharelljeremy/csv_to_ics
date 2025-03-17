import openai
import os
import pandas as pd
from icalendar import Calendar, Event
from datetime import datetime
import pytz
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def generate_csv_from_prompt(prompt, csv_filename):
    """Generates a CSV file using GPT-4 API with the correct format."""
    client = openai.OpenAI(api_key=api_key)

    csv_format = """Your response must be a CSV with these exact column headers:
Start Date,Start Time,End Date,End Time,Subject,Location,Description
- Start Date & End Date: YYYY-MM-DD format
- Start Time & End Time: HH:MM (24-hour format)
- Subject: Event title
- Location: Where the event happens
- Description: A short summary"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"{prompt}\n\n{csv_format}"}
        ],
        response_format={"type": "text"}
    )

    csv_data = response.choices[0].message.content.strip()

    # Save CSV file
    with open(csv_filename, "w") as f:
        f.write(csv_data)

    print(f"✅ CSV file saved: {csv_filename}")

def convert_csv_to_ics(csv_filename, ics_filename, timezone="Europe/London"):
    """Converts a CSV file into an ICS file."""
    df = pd.read_csv(csv_filename)
    cal = Calendar()
    tz = pytz.timezone(timezone)

    for _, row in df.iterrows():
        event = Event()
        start_dt = datetime.strptime(f"{row['Start Date']} {row['Start Time']}", "%Y-%m-%d %H:%M").replace(tzinfo=tz)
        end_dt = datetime.strptime(f"{row['End Date']} {row['End Time']}", "%Y-%m-%d %H:%M").replace(tzinfo=tz)

        event.add("summary", row["Subject"])
        event.add("dtstart", start_dt)
        event.add("dtend", end_dt)
        event.add("description", row.get("Description", ""))
        
        cal.add_component(event)

    with open(ics_filename, "wb") as f:
        f.write(cal.to_ical())

    print(f"✅ ICS file saved: {ics_filename}")

def main():
    """Main function to run AI-powered CSV to ICS conversion."""
    prompt = input("📌 Enter event schedule prompt: ")
    csv_filename = "events.csv"
    ics_filename = "events.ics"

    generate_csv_from_prompt(prompt, csv_filename)
    convert_csv_to_ics(csv_filename, ics_filename)

if __name__ == "__main__":
    main()