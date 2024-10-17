import pandas as pd
from bookings.models import MuseumInfo, TicketInfo
from mongoengine import connect

# Connect to your MongoDB database
connect('museum_ticketing_system')

# Function to import MuseumInfo from CSV
def import_museum_info(csv_file_path="/travelo/museum_info.csv"):
    # Load the CSV file into a DataFrame
    data = pd.read_csv(csv_file_path).fillna('')  # Fill NaN with empty string to avoid errors
    
    # Loop through each row and create a MuseumInfo entry
    for _, row in data.iterrows():
        museum = MuseumInfo(
            museum_id=row['Museum ID'],
            museum_name=row['Museum Name'],
            museum_type=row['Museum Type'],
            administrative_state=row['State (Administrative Location)'],
            street_address=row['Street Address (Physical Location)'],
            city=row['City (Physical Location)'],
            state=row['State (Physical Location)'],
            zip_code=row['Zip Code (Physical Location)'],
            phone_number=row['Phone Number'],
            latitude=row['Latitude'] if row['Latitude'] != '' else None,  # Handle empty lat/lon values
            longitude=row['Longitude'] if row['Longitude'] != '' else None,
            income=row['Income'] if row['Income'] != '' else 0,  # Handle missing income/revenue
            revenue=row['Revenue'] if row['Revenue'] != '' else 0,
            opening_hours=row['Opening Hours'],
            wheelchair_accessible=bool(row['Wheelchair Accessible']) if row['Wheelchair Accessible'] != '' else False,
            amenities=row['Amenities'].split(',') if isinstance(row['Amenities'], str) else [],  # Split amenities if valid
            website_url=row['Website URL'],
            museum_summary=row['Museum Summary'],
            email_address=row['Email Address']
        )
        museum.save()
    print("MuseumInfo data imported successfully.")

# Function to import TicketInfo from CSV
def import_ticket_info(csv_file_path="/travelo/ticket_info.csv"):
    # Load the CSV file into a DataFrame
    data = pd.read_csv(csv_file_path).fillna('')  # Fill NaN with empty string to avoid errors
    
    # Loop through each row and create a TicketInfo entry
    for _, row in data.iterrows():
        ticket = TicketInfo(
            ticket_id=row['Ticket ID'],
            user_id=row['User ID'],
            museum_id=row['Museum ID'],
            booking_date=pd.to_datetime(row['Booking Date'], errors='coerce'),  # Handle date parsing
            visit_date=pd.to_datetime(row['Visit Date'], errors='coerce'),
            ticket_type=row['Ticket Type'],
            price=float(row['Price']) if row['Price'] != '' else 0.0,  # Convert to float or 0.0 if missing
            payment_status=row['Payment Status'],
            number_of_tickets=int(row['Number of Tickets']) if row['Number of Tickets'] != '' else 0,  # Convert to int
            total_amount=float(row['Total Amount']) if row['Total Amount'] != '' else 0.0,  # Convert to float
            payment_method=row['Payment Method'],
            booking_status=row['Booking Status']
        )
        ticket.save()
    print("TicketInfo data imported successfully.")

# Run the imports
import_museum_info('/travelo/museum_info.csv')
import_ticket_info('/travelo/ticket_info.csv')
