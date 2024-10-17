
from django.urls import path
from . import views
from .views import cancel_ticket, reschedule_ticket, book_ticket, chatbot_response

urlpatterns = [
    path('', views.index, name='index'),  # Welcome page
    # path('book_ticket/', book_ticket, name='book_ticket'),  # Booking form
    path('cancel_ticket/', cancel_ticket, name='cancel_ticket'),  # Cancel ticket
    path('reschedule_ticket/', reschedule_ticket, name='reschedule_ticket'),  # Reschedule ticket
    path('api/book_ticket/', book_ticket, name='api_book_ticket'),
    path('api/cancel_ticket/<int:ticket_id>/', cancel_ticket, name='api_cancel_ticket'),
    # Add additional paths for rescheduling and payment
    path('chatbot-response/', chatbot_response, name='chatbot_response'),
    
]
