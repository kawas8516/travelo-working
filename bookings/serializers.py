from rest_framework import serializers
from .models import TicketInfo  # Adjust based on your model

class TicketInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketInfo
        fields = '__all__'
