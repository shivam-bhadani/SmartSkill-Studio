# SmartSkill Studio

## Overview
This is a Django-based backend for a course app where students can enroll in courses, teachers can sell courses, and students within the same course can chat with each other.

## Features

- **Course Management**:
  - Teachers can create, update, and manage courses.
  - Students can browse and enroll in courses.
- **Chat Functionality**: Real-time chat for students enrolled in the same course.
- **Lecture Upload**: Lectures can be uploaded to AWS S3.
- **Video Processing**: FFmpeg is used in a separate Docker container for video processing.
- **Payment Integration**: Teachers can sell courses to students.
- **User Authentication**: Secure login and registration for students and teachers using JWT.

## Technologies Used

- **Backend**: Django
- **Database**: SQLite (default) / MySQL / PostgreSQL (configurable)
- **Real-time Communication**: Django Channels
- **Authentication**: JWT (JSON Web Tokens)
- **File Storage**: AWS S3
- **Video Processing**: FFmpeg in Docker
- **Containerization**: Docker

### Prerequisites

- Python 3.x
- Django
- AWS S3 bucket
- Redis
- Docker
- MySQL

### Installation Steps

1. **Clone the Repository**
   ```sh
   git clone https://github.com/your-username/course-website.git
   cd course-website
   ```
2. Create a Virtual Environment
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install Dependencies
   ```sh
   pip install -r requirements.txt
   ```
4. Configure Database
   - Update the DATABASES setting in settings.py to configure your database.
     
5. Run Migrations
   ```sh
   python manage.py migrate
   ```
6. Create a Superuser
   ```sh
   python manage.py createsuperuser
   ```
7. Run the Development Server
   ```sh
   daphne smartskill_studio.asgi:application
   ```

## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Push the branch and create a pull request.
