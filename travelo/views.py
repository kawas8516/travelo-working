from django.shortcuts import render
def chatbot_response(request):
    return render(request, 'base.html')  # Ensure you have a chatbot.html file