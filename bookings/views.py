# from django.http import HttpResponse

# def index(request):
#     return HttpResponse("Welcome to the Ticket Booking App!")

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from .models import TicketInfo
from datetime import datetime
from django.http import JsonResponse
from .models import TicketInfo, MuseumInfo
from django.views.decorators.csrf import csrf_exempt
import json
from bookings.models import TicketInfo  # Ensure correct import path

def index(request):
    return HttpResponse("Welcome to the Ticket Booking App!")

def book_ticket(request):
    if request.method == "POST":
        # Extract data from the form
        user_id = request.POST.get('user_id')
        museum_id = request.POST.get('museum_id')
        visit_date = request.POST.get('visit_date')
        ticket_type = request.POST.get('ticket_type')
        price = float(request.POST.get('price'))
        number_of_tickets = int(request.POST.get('number_of_tickets'))

        # Create a new TicketInfo object
        ticket = TicketInfo(
            user_id=user_id,
            museum_id=museum_id,
            booking_date=datetime.now(),
            visit_date=visit_date,
            ticket_type=ticket_type,
            price=price,
            number_of_tickets=number_of_tickets,
            total_amount=price * number_of_tickets,
            payment_status="Pending",
            booking_status="Confirmed"  # or other initial status
        )
        ticket.save()
        return redirect('booking_success')  # Redirect to a success page

    return render(request, 'bookings/book_ticket.html')

def cancel_ticket(request):
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        try:
            ticket = TicketInfo.objects.get(ticket_id=ticket_id)
            ticket.booking_status = 'Cancelled'
            ticket.save()
            return JsonResponse({'message': 'Ticket cancelled successfully.'})
        except TicketInfo.DoesNotExist:
            return JsonResponse({'error': 'Ticket not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def reschedule_ticket(request):
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        new_visit_date = request.POST.get('new_visit_date')
        try:
            ticket = TicketInfo.objects.get(ticket_id=ticket_id)
            ticket.visit_date = new_visit_date
            ticket.save()
            return JsonResponse({'message': 'Ticket rescheduled successfully.'})
        except TicketInfo.DoesNotExist:
            return JsonResponse({'error': 'Ticket not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def book_ticket(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            museum_id = data.get('museum_id')
            visit_date = data.get('visit_date')
            ticket_type = data.get('ticket_type')
            number_of_tickets = int(data.get('number_of_tickets'))
            price_per_ticket = float(data.get('price'))

            total_amount = number_of_tickets * price_per_ticket

            # Create a new ticket entry
            ticket = TicketInfo.objects.create(
                user_id=data.get('user_id'),
                museum_id=museum_id,
                booking_date=datetime.now(),
                visit_date=datetime.strptime(visit_date, '%Y-%m-%d'),
                ticket_type=ticket_type,
                number_of_tickets=number_of_tickets,
                total_amount=total_amount,
                price=price_per_ticket,
                payment_status='Pending',
                booking_status='Confirmed'
            )

            return JsonResponse({'status': 'success', 'ticket_id': ticket.ticket_id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return HttpResponse(status=405)

@csrf_exempt
def cancel_ticket(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ticket_id = data.get('ticket_id')

            # Find the ticket and cancel it
            ticket = TicketInfo.objects.get(ticket_id=ticket_id)
            ticket.booking_status = 'Cancelled'
            ticket.save()

            return JsonResponse({'status': 'success', 'message': 'Ticket cancelled successfully'})
        except TicketInfo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Ticket not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return HttpResponse(status=405)

@csrf_exempt
def reschedule_ticket(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ticket_id = data.get('ticket_id')
            new_visit_date = data.get('new_visit_date')

            # Find the ticket and reschedule it
            ticket = TicketInfo.objects.get(ticket_id=ticket_id)
            ticket.visit_date = datetime.strptime(new_visit_date, '%Y-%m-%d')
            ticket.booking_status = 'Rescheduled'
            ticket.save()

            return JsonResponse({'status': 'success', 'message': 'Ticket rescheduled successfully'})
        except TicketInfo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Ticket not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return HttpResponse(status=405)
    
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TicketInfo
from .serializers import TicketInfoSerializer

@api_view(['POST'])
def book_ticket(request):
    if request.method == 'POST':
        serializer = TicketInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def cancel_ticket(request, ticket_id):
    try:
        ticket = TicketInfo.objects.get(id=ticket_id)
    except TicketInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Add additional views for rescheduling and payment processing


from django.http import JsonResponse

def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')

        # Call the Rasa server to get the chatbot response
        bot_response = process_message(user_message)

        return JsonResponse({'message': bot_response})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def process_message(user_message):
    url = "http://localhost:5005/webhooks/rest/webhook"  # Rasa's REST webhook
    

    payload = {
        "sender": "user",  # Identifier for the user
        "message": user_message
    }

    response = requests.post(url=url, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        if response_data:  # Check if there's a response
            bot_reply = response_data[0].get('text', 'I didn’t understand that.')
            return bot_reply
        else:
            return "Sorry, I didn't understand that."
    else:
        return "Error: Unable to connect to the chatbot service."
