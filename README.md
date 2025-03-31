# Parket Parking Management System

A backend for managing parking access for employees of clients.

## Features

- Client registration and authentication
- Bulk import of parking users via Excel or CSV
- Parking user management (list, bulk add, delete)
- License plate information and region 
- SQLite database for data storage
- Containerized deployment with Docker and Docker Compose

## Requirements

- Docker, Docker Compose,
- Optional: Postman

## Getting Started

1. Clone the repository:
```
git clone git@github.com:{username}/parking_management.git
```

2. Navigate to the cloned project repository:
```
cd parking_management
```

3. Create an `.env` file in the current repository with the following value:
```
DJANGO_SECRET_KEY={some_secure_string}
```

3. Build and start the Docker container:
```
docker-compose up --build
```

4. The backend server will be available at http://localhost:8080/

## API Endpoints

The `base_url` variable when running this application locally is: `http://127.0.0.1:8080`

### Authentication
- `POST {base_url}/register/` - Register a new client
- `POST {base_url}/login/` - Login and receive an authentication token

### Parking Users
- `GET {base_url}/parking-users/` - List all parking users for the authenticated client
- `POST {base_url}/parking-users/bulk_import/` - Import multiple parking users from a CSV/Excel file
- `DELETE {base_url}/parking-users/{id}/` - Delete a parking user

### Try It Out With A Postman Pack!
Download and import the following
[Parket API Postman Collection](https://gist.github.com/StephanVanBiljon/bb1300f3ec3bd092421cb40fabc90674).

### Usage Instructions
To use the system after deployment:

1. Register a new client (parking facility manager):
```
POST {base_url}/register/
{
  "username": "riverlands",
  "password": "password123",
  "email": "riverlands@gmail.com",
  "address": "51 Gogosoa St, Observatory, Cape Town, 7925, South Africa"
}
```

2. Login to get an auth token:
```
POST {base_url}/login/
{
  "username": "riverlands",
  "password": "password123"
}
```

3. Use the token for subsequent requests to `GET {base_url}/parking-users/`,
`POST {base_url}/parking-users/bulk_import/` and
`DELETE {base_url}/parking-users/{id}/` by setting the "Authorization" header:
```
Authorization: Token {auth_token}
```

4. Import parking users from a file:

```
POST {base_url}/parking-users/bulk_import/
Content-Type: form-data
file: [your_file.csv or your_file.xlsx]
```

5. List all parking users for the authenticated client:
```
GET {base_url}/parking-users/
```

6. Delete a parking user for the authenticated client:
```
DELETE {base_url}/parking-users/{user_id}/
```

## File Format for Bulk Import

Both CSV and Excel files should have the following columns:
- email
- first_name
- last_name
- license_plate
- region

### Examples

- [melrose_arch_users.csv](melrose_arch_users.csv)
- [melrose_arch_users.xlsx](melrose_arch_users.xlsx)
- [riverlands_users.csv](riverlands_users.csv)
- [riverlands_users.xlsx](riverlands_users.xlsx)

### Testing

Sample files for testing the bulk import feature are included in the above "Examples" section, and are present in the root `parking_management` directory. 

Postman: One file at a time can be added to the body of the `POST {{base_url}}/parking-users/bulk_import/` endpoint. 
