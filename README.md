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