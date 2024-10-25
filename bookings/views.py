from django.http import JsonResponse
from django.views import View
from .models import MuseumInfo, TicketInfo
import json

# Helper function to create JSON response
def create_response(status, message, **kwargs):
    response_data = {"status": status, "message": message}
    response_data.update(kwargs)
    return JsonResponse(response_data)

class MuseumView(View):
    def get_museum_info(self, museum_name):
        try:
            museum = MuseumInfo.objects.get(museum_name=museum_name)
            return create_response('success', 'Museum info fetched successfully', museum_info={
                'museum_id': museum.museum_id,
                'museum_name': museum.museum_name,
                'museum_type': museum.museum_type,
                'address': museum.street_address,
                'city': museum.city,
                'state': museum.state,
                'phone': museum.phone_number,
                'latitude': museum.latitude,
                'longitude': museum.longitude,
            })
        except MuseumInfo.DoesNotExist:
            return create_response('error', 'Museum not found')

    def post(self, request):
        data = json.loads(request.body)
        museum_name = data.get("museum_name")
        return self.get_museum_info(museum_name)

class TicketBookingView(View):
    def book_ticket(self, user_id, museum_id, visit_date, number_of_tickets, ticket_type, price):
        ticket_info = TicketInfo(
            user_id=user_id,
            museum_id=museum_id,
            visit_date=visit_date,
            number_of_tickets=number_of_tickets,
            ticket_type=ticket_type,
            price=price,
        )
        ticket_info.save()
        return create_response('success', 'Ticket booked successfully', ticket_id=ticket_info.ticket_id)

    def post(self, request):
        data = json.loads(request.body)
        user_id = data.get("user_id", "some_user_id")  # Replace with actual user ID logic
        museum_id = data.get("museum_id")
        visit_date = data.get("visit_date")
        number_of_tickets = data.get("number_of_tickets")
        ticket_type = data.get("ticket_type", "adult")  # Default to adult ticket
        price = data.get("price", 0)  # Assuming price is passed in the request
        return self.book_ticket(user_id, museum_id, visit_date, number_of_tickets, ticket_type, price)

class TicketCancellationView(View):
    def cancel_ticket(self, ticket_id):
        try:
            ticket_info = TicketInfo.objects.get(ticket_id=ticket_id)
            ticket_info.delete()
            return create_response('success', 'Ticket cancelled successfully')
        except TicketInfo.DoesNotExist:
            return create_response('error', 'Ticket not found')

    def post(self, request):
        data = json.loads(request.body)
        ticket_id = data.get("ticket_id")
        return self.cancel_ticket(ticket_id)

class TicketReschedulingView(View):
    def reschedule_ticket(self, ticket_id, new_visit_date):
        try:
            ticket_info = TicketInfo.objects.get(ticket_id=ticket_id)
            ticket_info.visit_date = new_visit_date
            ticket_info.save()
            return create_response('success', 'Ticket rescheduled successfully')
        except TicketInfo.DoesNotExist:
            return create_response('error', 'Ticket not found')

    def post(self, request):
        data = json.loads(request.body)
        ticket_id = data.get("ticket_id")
        new_visit_date = data.get("new_visit_date")
        return self.reschedule_ticket(ticket_id, new_visit_date)

class TicketInfoView(View):
    def get_ticket_info(self, ticket_id):
        try:
            ticket = TicketInfo.objects.get(ticket_id=ticket_id)
            ticket_info = {
                "ticket_id": ticket.ticket_id,
                "museum_name": ticket.museum_name,
                "visit_date": ticket.visit_date,
                "number_of_tickets": ticket.number_of_tickets,
            }
            return create_response('success', 'Ticket info fetched successfully', ticket=ticket_info)
        except TicketInfo.DoesNotExist:
            return create_response('error', 'Ticket not found.')

    def get(self, request):
        ticket_id = request.GET.get('ticket_id')
        return self.get_ticket_info(ticket_id)

# URLs mapping
from django.urls import path

urlpatterns = [
    path('get_museum_info/', MuseumView.as_view(), name='get_museum_info'),
    path('book_ticket/', TicketBookingView.as_view(), name='book_ticket'),
    path('cancel_ticket/', TicketCancellationView.as_view(), name='cancel_ticket'),
    path('reschedule_ticket/', TicketReschedulingView.as_view(), name='reschedule_ticket'),
    path('get_ticket_info/', TicketInfoView.as_view(), name='get_ticket_info'),
]
