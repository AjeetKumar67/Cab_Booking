# Cab Booking Application (Rapido Clone)

A complete cab booking application similar to Rapido built with Django, SQLite, and Bootstrap UI.

## Features

- **Multiple User Roles**: Admin, Rider, and Driver roles with specific functionalities
- **Ride Booking**: Search locations, choose cab type, and book rides
- **Driver Management**: Driver registration, approval, and availability tracking
- **Real-time Location**: Driver location tracking and ride status updates
- **Fare Calculation**: Dynamic fare calculation based on distance and cab type
- **Payment System**: Multiple payment methods and invoice generation
- **Ride History**: Complete history of all rides for users and drivers
- **Rating System**: Feedback and rating system for rides
- **Notifications**: Real-time notifications for ride updates and alerts

## Tech Stack

- **Backend**: Django
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Maps**: Google Maps API for location services
- **Payment Gateway**: Mock implementation (can be replaced with actual payment gateway)

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (optional but recommended)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd CabBooking
   ```

2. Set up a virtual environment (optional):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser for admin access:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

### Alternative Setup

You can also use the provided scripts:

1. Make the scripts executable:
   ```
   chmod +x run.sh create_admin.sh
   ```

2. Create an admin user:
   ```
   ./create_admin.sh
   ```

3. Run the application:
   ```
   ./run.sh
   ```

## Google Maps API Setup

1. Get a Google Maps API key from the [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the following APIs:
   - Maps JavaScript API
   - Places API
   - Directions API
   - Geocoding API
3. Replace `YOUR_API_KEY` in the templates with your actual API key

## Application Structure

- **users**: User authentication and profile management
- **drivers**: Driver profiles and location management
- **rides**: Ride booking and management
- **payments**: Payment processing and invoices
- **feedback**: Rating and review system
- **notifications**: User notifications system

## Default User Credentials

After setup, you can use the following default credentials:

- **Admin**: The superuser you created during setup
- **Rider**: Create a new user with the "Rider" role
- **Driver**: Create a new user with the "Driver" role and complete driver registration

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Bootstrap for the UI components
- Font Awesome for icons
- Google Maps for location services
