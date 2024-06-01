# Dance Academy Management System

This repository contains the source code for a Dance Academy Management System. This system is designed to efficiently manage all aspects of a dance academy, including storing student data, managing fees, detecting due dates, and accepting payments.

## Features

- **Student Management**: Store and manage student data, including personal information, contact details, and class enrollment.
- **Fee Management**: Automatically generate fee invoices for each student based on their enrolled classes and track fee payments.
- **Due Date Detection**: Automatically detect and notify students about upcoming fee due dates to ensure timely payments.
- **Performance Analysis**: Generate reports and analytics to analyze student performance, class popularity, revenue trends, etc.
- **User Authentication**: Secure access to the system with user authentication and authorization mechanisms to ensure data privacy and integrity.
- **Customization**: Customize the system according to the specific needs and requirements of the dance academy.

## Technologies Used

- **Programming Language**: Python
- **Web Framework**: Django
- **Database**: SQLite (or any other supported by Django)
- **Frontend**: HTML, CSS, JavaScript

## Installation

1. Clone the repository to your local machine:

```
https://github.com/psrawat23/dance-academy.git
```

2. Navigate to the project directory:

```
cd dance-academy
```

3. Install the required dependencies:

```
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

4. Set up the database and perform migrations:

```
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser account to access the admin panel:

```
python manage.py createsuperuser
```

6. Start the development server:

```
python manage.py runserver
```

7. Access the application at [http://localhost:8000](http://localhost:8000)

## Usage

- Log in to the admin panel using the superuser credentials created during installation.
- Add students in the portal.
- Generate fee invoices for students based on their enrolled classes and fee structures.
- Track fee payments for upcoming due dates.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/improvement`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/improvement`).
5. Create a new pull request.
## Contact

For any inquiries or support, please contact [Purushottam Singh](mailto:psrawat23.pr@gmail.com).
