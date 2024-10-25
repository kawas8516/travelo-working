import qrcode
from PIL import Image
import requests
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher

DJANGO_BACKEND_URL = "http://127.0.0.1:8000"

class ActionGenerateTicket(Action):
    def name(self):
        return "action_generate_ticket"

    def run(self, dispatcher, tracker, domain):
        # Get the ticket ID from the user input
        ticket_id = tracker.get_slot("ticket_id")
        if not ticket_id:
            dispatcher.utter_message("Please provide a valid ticket ID.")
            return []

        # Fetch ticket details from the Django backend
        try:
            response = requests.get(f"{DJANGO_BACKEND_URL}/tickets/")
            response.raise_for_status()  # Check if the request was successful
            tickets = response.json()
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(f"Error fetching ticket data: {str(e)}")
            return []

        # Find the ticket with the matching ID
        ticket_data = next((ticket for ticket in tickets if ticket["ticket_id"].lower() == ticket_id.lower()), None)
        
        if not ticket_data:
            dispatcher.utter_message(f"No ticket found with ID: {ticket_id}")
            return []

        # Generate a QR code for the ticket
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(str(ticket_data))  # Add ticket details to the QR code
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Open the pre-designed ticket image
            ticket_design = Image.open("ticket_design.png")

            # Paste the QR code onto the ticket design
            ticket_design.paste(qr_img, (50, 50))  # Adjust coordinates as needed

            # Save the final ticket image with QR code
            ticket_design.save("ticket_with_qr.png")

            # Send the ticket image to the user
            dispatcher.utter_message("Your ticket is ready. Please find it attached below.")
            dispatcher.utter_attachment("ticket_with_qr.png")

        except Exception as e:
            dispatcher.utter_message(f"Error generating the ticket image: {str(e)}")
            return []

        return []
