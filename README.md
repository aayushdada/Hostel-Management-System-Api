#Hostel Management System API
A RESTful API for managing hostels,rooms,users and bookings

##Features 
-User registration and login
-JWT-based authentication
-Role-based authorization
-Hostel management
-Room management
-Booking management
-PostgreSQL database
-Input validation and error handling
-RESTful API endpoints

#Tech Stack
-Python
-Flask
-PostgreSQL
-Flask-JWT-Extended
-Psycopg
-Postman
-Git & Github
-Render
## API Overview

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/login` | Login and receive JWT token |

### Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/users` | Register a new user |
| GET | `/api/users` | Get all users |
| GET | `/api/users/<id>` | Get a specific user |
| PUT | `/api/users/<id>` | Update user |
| PATCH | `/api/users/<id>` | Partially update user |
| DELETE | `/api/users/<id>` | Delete user |

### Hostels

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/hostels` | Create a hostel |
| GET | `/api/hostels` | Get all hostels |
| GET | `/api/hostels/<id>` | Get a specific hostel |
| PUT | `/api/hostels/<id>` | Update hostel |
| PATCH | `/api/hostels/<id>` | Partially update hostel |
| DELETE | `/api/hostels/<id>` | Delete hostel |

### Rooms

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/rooms` | Create a room |
| GET | `/api/rooms` | Get all rooms |
| GET | `/api/rooms/<id>` | Get a specific room |
| PUT | `/api/rooms/<id>` | Update room |
| PATCH | `/api/rooms/<id>` | Partially update room |
| DELETE | `/api/rooms/<id>` | Delete room |

### Bookings

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/bookings` | Create a booking |
| GET | `/api/bookings` | Get all bookings |
| GET | `/api/bookings/<id>` | Get a specific booking |
| PUT | `/api/bookings/<id>` | Update booking |
| PATCH | `/api/bookings/<id>` | Partially update booking |
| DELETE | `/api/bookings/<id>` | Delete booking |
## Authentication & Authorization

This API uses JWT (JSON Web Tokens) for authentication.

- Users receive a JWT access token after successful login.
- Protected endpoints require a valid JWT token.
- Role-based authorization is used to restrict admin-only operations.
- Admin users can manage users, hostels, rooms, and bookings.
- Unauthorized requests return appropriate HTTP status codes.

## Booking Rules

- A user must exist before creating a booking.
- A room must exist before creating a booking.
- A room cannot have multiple bookings on the same date.
- Duplicate room bookings return `409 Conflict`.
- Invalid booking dates return `400 Bad Request`.
- Booking status must be `pending`, `confirmed`, or `cancelled`.
- Booking management endpoints are restricted to administrators.


## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/aayushdada/Hostel-Management-System-Api.git
cd Hostel-Management-System-Api

2.Create a virtual environment
-> python -m venv venv
#activate it on windows
-> venv\Scripts\activate

3.Install dependencies
-> pip install -r requirements.txt

4.Configure environment variables
Create a .env file:
DB_HOST=your_database_host
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_PORT=5432
JWT_SECRET_KEY=your_secret_key

5.Run the application
-> python app.py
the api will be availabe at:
http://127.0.0.1:5000


⚠️ Keep the actual database password and JWT secret **out of GitHub**. Your `.env` should remain ignored by `.gitignore`.

