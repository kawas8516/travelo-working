# models.py
from mongoengine import Document, StringField, FloatField, BooleanField, IntField, ListField, DateTimeField

class MuseumInfo(Document):
    museum_id = StringField(required=True, unique=True)
    museum_name = StringField(required=True)
    museum_type = StringField()
    administrative_state = StringField()
    street_address = StringField()
    city = StringField()
    state = StringField()
    zip_code = StringField()
    phone_number = StringField()
    latitude = FloatField()
    longitude = FloatField()
    income = FloatField()
    revenue = FloatField()
    opening_hours = StringField()
    wheelchair_accessible = BooleanField()
    amenities = ListField(StringField())
    website_url = StringField()
    museum_summary = StringField()
    email_address = StringField()

class TicketInfo(Document):
    ticket_id = StringField(required=True, unique=True)
    user_id = StringField(required=True)  # You may want to link this to a User model
    museum_id = StringField(required=True)
    booking_date = DateTimeField()
    visit_date = DateTimeField()
    ticket_type = StringField()
    price = FloatField()
    payment_status = StringField()  # Could be "Paid", "Pending", "Failed"
    number_of_tickets = IntField()
    total_amount = FloatField()
    payment_method = StringField()
    booking_status = StringField()  # Could be "Confirmed", "Cancelled", "Rescheduled"
