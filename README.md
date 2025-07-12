# TaskMaster ProMarkdown Preview Enhanced

#### Video Demo: [https://www.youtube.com/watch?v=stsZTSPVnDM]

## Description

TaskMaster Pro is an advanced web-based To-Do List application built using Flask, SQLAlchemy, and SQLite. It demonstrates a range of full-stack development skills and incorporates several features that make it stand out in the realm of task management applications.

## Features

1. **User Authentication**:
   The app includes a secure login and registration system, ensuring that each user has their own private task list.

   ![Login Page](images/login.png)
   ![Registration Page](images/register.png)

2. **Task Dashboard**:
   After logging in, users are presented with their task dashboard. This is where users can view, add, complete, and delete tasks. Each task can have a due date and a category, allowing for better organization.

   ![Task Dashboard](images/task_management.png)

3. **Task Management**:
   Users can easily manage their tasks directly from the dashboard. This includes adding new tasks, marking tasks as complete, and deleting tasks.

   ![Mobile View](images/mobile_view.png)

4. **Responsive Design**:
   The frontend is built with Bootstrap, ensuring a mobile-friendly experience across various devices.

   ![Mobile View](images/mobile_view.png)

5. **RESTful API**:
   The application includes a RESTful API for task management, demonstrating the ability to create backend services.

   ![API Response](images/api_response.png)

## Project Components

1. `app.py`:
   The main Flask application file. It includes:
   - User authentication logic
   - Task CRUD operations
   - API endpoints
   - Database models for User and Task

2. `templates/`:
   - `base.html`: The base template that other templates extend from
   - `index.html`: The main page where tasks are displayed and can be added
   - `login.html` and `register.html`: Forms for user authentication

3. `static/`:
   - Contains CSS and JavaScript files for styling and client-side functionality

4. `taskmaster.db`:
   The SQLite database file

## Technical Skills Showcase

This project showcases several important skills for web development:

- **Backend Development**: Python, Flask, SQLAlchemy
- **Frontend Development**: HTML, CSS, Bootstrap, JavaScript
- **Database Management**: SQLite
- **Authentication**: User login and registration
- **API Development**: RESTful API endpoints
- **Security**: Password hashing, protected routes

## Setup and Installation

To run this project:

1. Clone the repository:
   ```
   git clone https://github.com/kelvinmendoza59/TaskMaster-Pro.git
   cd TaskMaster-Pro
   ```

2. Install the required packages:
   ```
   pip install flask flask-sqlalchemy flask-bcrypt flask-login flask-restful
   ```

3. Initialize the database:
   ```
   python
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

4. Run the Flask application:
   ```
   python app.py
   ```

5. Access the application at `http://localhost:5000`

## API Usage

The RESTful API provides endpoints for task management:

- GET /api/tasks: Retrieve all tasks
- POST /api/tasks: Create a new task
- PUT /api/tasks/<id>: Update a task
- DELETE /api/tasks/<id>: Delete a task

Example API request:

```python
import requests

response = requests.get('http://localhost:5000/api/tasks',
                        auth=('username', 'password'))
tasks = response.json()
```

## Future Enhancements

- Implement task sharing between users
- Add email notifications for upcoming due dates
- Integrate a calendar view for better task visualization

## Conclusion

TaskMaster Pro demonstrates a solid understanding of full-stack web development principles and practices, making it an impressive project for potential employers. It showcases the ability to create a fully functional web application with user authentication, database management, and API integration.

## Developer Information

- **edX Account**: kelvinmendoza309
- **GitHub Username**: kelvinmendoza59

Feel free to contact me for any questions or collaborations!
