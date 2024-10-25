

from . import views


# urlpatterns = [
#     path('', views.index, name='index'),  # Welcome page
#     # path('book_ticket/', book_ticket, name='book_ticket'),  # Booking form
#     path('cancel_ticket/', cancel_ticket, name='cancel_ticket'),  # Cancel ticket
#     path('reschedule_ticket/', reschedule_ticket, name='reschedule_ticket'),  # Reschedule ticket
#     path('api/book_ticket/', book_ticket, name='api_book_ticket'),
#     path('api/cancel_ticket/<int:ticket_id>/', cancel_ticket, name='api_cancel_ticket'),
#     # Add additional paths for rescheduling and payment
#     path('chatbot-response/', chatbot_response, name='chatbot_response'),
    
# ]
# bookings/urls.py
from django.urls import path
from .views import MuseumView, TicketBookingView, TicketCancellationView, TicketReschedulingView

urlpatterns = [
    path('get_museum_info/', MuseumView.as_view(), name='get_museum_info'),
    path('book_ticket/', TicketBookingView.as_view(), name='book_ticket'),
    path('cancel_ticket/', TicketCancellationView.as_view(), name='cancel_ticket'),
    path('reschedule_ticket/', TicketReschedulingView.as_view(), name='reschedule_ticket'),
]

