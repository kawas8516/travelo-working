import datetime
import logging
import requests
from mongoengine import connect, StringField, Document, IntField, DateTimeField
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Configure logging
logging.basicConfig(
    filename='actions_log.log',  # Log file location
    filemode='a',  # Append to the log file
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# MongoDB connection setup
connect(db="museum_ticketing_system", host="localhost", port=27017)

# Django Backend URL
DJANGO_BACKEND_URL = "http://localhost:8000"

# MongoEngine model for ticket information
class TicketInfo(Document):
    ticket_id = StringField(required=True)
    user_id = StringField(required=True)
    museum_id = StringField(required=True)
    num_tickets = IntField(required=True)
    price = IntField(required=True)
    visit_date = DateTimeField(required=True)
    meta = {'collection': 'ticket_info'}

# Action to ask for museum details
class ActionAskMuseum(Action):
    def name(self):
        return "action_ask_museum"

    def run(self, dispatcher, tracker, domain):
        try:
            museum_name = tracker.get_slot("museum_name")
            if not museum_name:
                dispatcher.utter_message("Which museum would you like to visit?")
            else:
                dispatcher.utter_message(f"You have chosen {museum_name}.")
            return []
        except Exception as e:
            logger.error(f"Error in action_ask_museum: {e}")
            dispatcher.utter_message("An error occurred. Please try again later.")
            return []

# Action to book a ticket
class ActionBookTicket(Action):
    def name(self):
        return "action_book_ticket"

    def run(self, dispatcher, tracker, domain):
        museum_name = tracker.get_slot("museum_name")
        num_tickets = tracker.get_slot("number_of_tickets")
        visit_date = tracker.get_slot("visit_date")
        ticket_type = tracker.get_slot("ticket_type")

        if not museum_name or not num_tickets or not visit_date or not ticket_type:
            dispatcher.utter_message("Please provide all the required details.")
            return []

        try:
            # Fetch museum data from Django backend
            response = requests.get(f"{DJANGO_BACKEND_URL}/museums/")
            response.raise_for_status()
            museums = response.json()
            matched_museums = [m for m in museums if museum_name.lower() in m["name"].lower()]

            if not matched_museums:
                dispatcher.utter_message("Museum not found.")
                return []

            museum_id = matched_museums[0]["museum_id"]

            # Generate unique IDs
            ticket_id = str(uuid.uuid4())
            user_id = str(uuid.uuid4())

            # Calculate ticket price
            ticket_price = self.calculate_price(ticket_type, num_tickets)

            # Validate visit date
            try:
                visit_date_obj = datetime.datetime.strptime(visit_date, '%Y-%m-%d')
                if visit_date_obj < datetime.datetime.now():
                    dispatcher.utter_message("The visit date must be in the future.")
                    return []
            except ValueError:
                dispatcher.utter_message("Invalid date format. Please use YYYY-MM-DD.")
                return []

            # Store ticket information in MongoDB
            ticket = TicketInfo(
                ticket_id=ticket_id,
                user_id=user_id,
                museum_id=museum_id,
                num_tickets=int(num_tickets),
                price=ticket_price,
                visit_date=visit_date_obj
            )
            ticket.save()

            # Confirm booking
            dispatcher.utter_message(f"Ticket booked successfully! Ticket ID: {ticket_id}, Total: ${ticket_price}.")
            logger.info(f"Ticket {ticket_id} booked successfully for museum {museum_name}.")
            return []

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching museums: {e}")
            dispatcher.utter_message("Unable to fetch museum data. Please try again later.")
            return []

        except Exception as e:
            logger.error(f"Error in action_book_ticket: {e}")
            dispatcher.utter_message(f"An error occurred: {e}")
            return []

    def calculate_price(self, ticket_type, num_tickets):
        ticket_type_prices = {"adult": 10, "senior": 5, "child": 3}
        return ticket_type_prices.get(ticket_type, 0) * int(num_tickets)

# Action to cancel a ticket
class ActionCancelTicket(Action):
    def name(self):
        return "action_cancel_ticket"

    def run(self, dispatcher, tracker, domain):
        ticket_id = tracker.get_slot("ticket_id")
        if not ticket_id:
            dispatcher.utter_message("Please provide the ticket ID.")
            return []

        try:
            ticket = TicketInfo.objects(ticket_id=ticket_id).first()
            if ticket:
                ticket.delete()
                dispatcher.utter_message(f"Ticket {ticket_id} has been canceled.")
                logger.info(f"Ticket {ticket_id} canceled successfully.")
            else:
                dispatcher.utter_message(f"Ticket {ticket_id} not found.")
        except Exception as e:
            logger.error(f"Error canceling ticket: {e}")
            dispatcher.utter_message(f"Error canceling ticket: {e}")
        return []

# Action to reschedule a ticket
class ActionRescheduleTicket(Action):
    def name(self):
        return "action_reschedule_ticket"

    def run(self, dispatcher, tracker, domain):
        ticket_id = tracker.get_slot("ticket_id")
        new_date = tracker.get_slot("new_date")

        if not ticket_id or not new_date:
            dispatcher.utter_message("Please provide ticket ID and new date.")
            return []

        try:
            new_date_obj = datetime.datetime.strptime(new_date, '%Y-%m-%d')
            ticket = TicketInfo.objects(ticket_id=ticket_id).first()
            if ticket:
                ticket.update(visit_date=new_date_obj)
                dispatcher.utter_message(f"Ticket {ticket_id} rescheduled to {new_date}.")
                logger.info(f"Ticket {ticket_id} rescheduled to {new_date}.")
            else:
                dispatcher.utter_message(f"Ticket {ticket_id} not found.")
        except ValueError:
            dispatcher.utter_message("Invalid date format. Please use YYYY-MM-DD.")
        except Exception as e:
            logger.error(f"Error rescheduling ticket: {e}")
            dispatcher.utter_message(f"Error rescheduling ticket: {e}")
        return []
