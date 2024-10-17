# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

# Replace with the actual URL of your Django backend
DJANGO_BACKEND_URL = "http://127.0.0.1:8000"

class ActionBookTicket(Action):
    def name(self) -> str:
        return "action_book_ticket"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: dict) -> list:
        
        museum = tracker.get_slot('museum')
        date = tracker.get_slot('date')
        number_of_tickets = tracker.get_slot('number_of_tickets')
        price = tracker.get_slot('price')

        # Prepare data for booking ticket
        data = {
            "user_id": "some_user_id",  # You might want to get the real user ID
            "museum_id": museum,  # You might map the museum name to an ID
            "visit_date": date,
            "ticket_type": "adult",  # Customize as per slot or user choice
            "number_of_tickets": number_of_tickets,
            "price": price,
        }

        try:
            response = requests.post(f"{DJANGO_BACKEND_URL}/book_ticket/", json=data)
            response_data = response.json()
            if response_data.get('status') == 'success':
                ticket_id = response_data.get('ticket_id')
                dispatcher.utter_message(text=f"Your ticket to {museum} has been booked for {date}! Ticket ID: {ticket_id}")
            else:
                dispatcher.utter_message(text="Failed to book your ticket. Please try again.")
        except Exception as e:
            dispatcher.utter_message(text=f"Error: {str(e)}")

        return []

class ActionCancelTicket(Action):
    def name(self) -> str:
        return "action_cancel_ticket"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: dict) -> list:
        
        ticket_id = tracker.get_slot('ticket_id')

        # Prepare data for cancelling ticket
        data = {"ticket_id": ticket_id}

        try:
            response = requests.post(f"{DJANGO_BACKEND_URL}/cancel_ticket/", json=data)
            response_data = response.json()
            if response_data.get('status') == 'success':
                dispatcher.utter_message(text=f"Your ticket with ID {ticket_id} has been cancelled.")
            else:
                dispatcher.utter_message(text="Failed to cancel your ticket. Please try again.")
        except Exception as e:
            dispatcher.utter_message(text=f"Error: {str(e)}")

        return []

class ActionRescheduleTicket(Action):
    def name(self) -> str:
        return "action_reschedule_ticket"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: dict) -> list:
        
        ticket_id = tracker.get_slot('ticket_id')
        new_date = tracker.get_slot('new_date')

        # Prepare data for rescheduling ticket
        data = {
            "ticket_id": ticket_id,
            "new_visit_date": new_date
        }

        try:
            response = requests.post(f"{DJANGO_BACKEND_URL}/reschedule_ticket/", json=data)
            response_data = response.json()
            if response_data.get('status') == 'success':
                dispatcher.utter_message(text=f"Your ticket with ID {ticket_id} has been rescheduled to {new_date}.")
            else:
                dispatcher.utter_message(text="Failed to reschedule your ticket. Please try again.")
        except Exception as e:
            dispatcher.utter_message(text=f"Error: {str(e)}")

        return []

