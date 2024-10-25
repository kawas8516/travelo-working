
# Travelo: Museum Ticketing Chatbot

### Project Overview
Travelo is an online museum ticketing system that uses a chatbot to facilitate user interaction. The system allows users to search for museums, book tickets, manage bookings, and view relevant information about museums, such as location, accessibility, amenities, and more. The project is developed using **Django** for the backend, **MongoDB** for the database, and **Rasa** for chatbot integration.

### Features
- Museum search by name, location, or type
- Ticket booking and management (rescheduling and cancellation)
- Provides museum information like amenities, accessibility, and opening hours
- Displays museum location links (Google Maps)
- Chatbot-based interaction using Rasa
- Payment integration (currently UPI/QR support planned with zero payment option)

### Project Structure
- **Django Backend**: Manages the APIs for booking, museum information, and user interaction.
- **MongoDB**: Stores museum details and ticketing information.
- **Rasa Chatbot**: Interacts with the user and processes bookings and queries.

### Installation and Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/your-username/travelo.git
cd travelo
```

#### 2. Create and Activate a Virtual Environment
```bash
python -m venv myenv
source myenv/bin/activate     # On Windows: myenv\Scripts\activate
```

#### 3. Install the Required Packages
```bash
pip install -r requirements.txt
```

#### 4. Set Up the Database
- Install and configure MongoDB.
- Add your connection details in the Django settings.

#### 5. Migrate the Database
```bash
python manage.py migrate
```

#### 6. Collect Static Files
```bash
python manage.py collectstatic
```

#### 7. Run the Server
```bash
python manage.py runserver
```

#### 8. Run the Rasa Bot
Ensure Rasa is installed, and then run:
```bash
rasa run actions
rasa shell
```

### Usage
1. Access the web interface via `http://127.0.0.1:8000`.
2. Use the chatbot to book tickets, ask about museum information, or manage your bookings.

### API Endpoints
- **GET /api/museums/**: Retrieve list of museums
- **POST /api/book_ticket/**: Book a museum ticket
- **PUT /api/reschedule_ticket/**: Reschedule an existing booking
- **DELETE /api/cancel_ticket/**: Cancel a booking

### Technologies Used
- **Backend**: Django 4.2.16
- **Chatbot**: Rasa
- **Database**: MongoDB (with MongoEngine)
- **Frontend**: HTML, CSS
- **Payment**: UPI/QR integration (under development)

### Contributing
1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Description of feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Contact
For any issues, feel free to reach out at **your-email@example.com**.
