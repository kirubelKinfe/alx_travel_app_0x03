# ALX Travel App (0x00)

A Django-based travel application with REST API, Swagger documentation, and database seeding.

## Setup Instructions

# alx_travel_app_0x02

## Payment Integration
This project integrates Chapa API for payment processing:
- **Payment Model**: Stores booking reference, amount, transaction ID, and status.
- **API Endpoints**:
  - `POST /api/payments/initiate/`: Initiates payment and returns Chapa checkout URL.
  - `GET /api/payments/verify/?tx_ref=<transaction_id>`: Verifies payment and updates status.
- **Email Notifications**: Sends confirmation emails using Celery on successful payment.
- **Testing**: Use Chapa sandbox environment with test cards.

## Setup
1. Install dependencies: `pip install django-chapa python-decouple celery`
2. Configure `.env` with `CHAPA_SECRET_KEY`, `EMAIL_HOST_USER`, and `EMAIL_HOST_PASSWORD`.
3. Run migrations: `python manage.py migrate`
4. Start Celery: `celery -A alx_travel_app worker -l info`
5. Test payment flow using Chapa sandbox credentials.

# ALX Travel App (0x01)

A Django-based travel application with REST API, Swagger documentation, and database seeding.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Muse-Semu/alx_travel_app_0x01.git
   cd alx_travel_app_0x01
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   Install MySQL dependencies:
   ```bash
   sudo apt-get update
   sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
   ```
   Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**:
   Create a `.env` file in the project root with:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_NAME=alx_travel_db
   DB_USER=your-mysql-user
   DB_PASSWORD=your-mysql-password
   DB_HOST=localhost
   DB_PORT=3306
   ```

5. **Set Up MySQL Database**:
   ```bash
   mysql -u root -p -e "CREATE DATABASE alx_travel_db;"
   ```

6. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Seed the Database**:
   ```bash
   python manage.py seed
   ```

8. **Run the Server**:
   ```bash
   python manage.py runserver
   ```
   Access the API documentation at `http://localhost:8000/swagger/`.

## Project Structure
- `listings/models.py`: Defines `Listing`, `Booking`, and `Review` models.
- `listings/serializers.py`: Serializers for `Listing` and `Booking` models.
- `listings/management/commands/seed.py`: Management command to seed the database.

## Database Seeding
Run `python manage.py seed` to populate the database with sample users, listings, bookings, and reviews.

## Celery & RabbitMQ Setup

1. **Install RabbitMQ**
   - Download and install RabbitMQ from https://www.rabbitmq.com/download.html
   - Start the RabbitMQ server.

2. **Install Celery**
   - Run: `pip install celery`

3. **Start Celery Worker**
   - In the project root, run:
     ```bash
     celery -A alx_travel_app worker -l info
     ```

4. **Test Background Email Task**
   - Create a booking via the API.
   - Check the Celery worker logs to confirm the email task is executed.
   - The user should receive a booking confirmation email (check your SMTP/email settings in `settings.py`).