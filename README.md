# Bulan Boarding House Management System

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Jaypee2705/boarding-house-management-system.git .
```

2. Create a Virtual Environment:

```bash
python -m venv venv
```

3. Activate the Virtual Environment:

```bash
venv\Scripts\activate
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

5. Run the application:

```bash
python manage.py runserver
```

6. Open the application in your browser:

```bash
http://127:0.0.1:8000/auth/login/
```

7. Migrate the database, cancel the runserver command and run the following command:

```bash
python manage.py migrate
```


8. Create a superuser:

```bash
python manage.py createsuperuser
``` 

```bash
Username: admin
Email address:
Password:
Password (again):
Superuser created successfully.
```

8. Run the application again:

```bash
python manage.py runserver
```
