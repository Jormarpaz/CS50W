# Student Organization Platform

## Distinctiveness and Complexity

This project, the **Student Organization Platform**, is distinct from the other projects in the CS50 course due to its comprehensive approach to solving common problems faced by students. While other projects in the course typically focus on a single functionality (e.g., a social network, an e-commerce site, or a search engine), this platform combines **multiple functionalities** into one cohesive application, making it a versatile tool for students. Specifically, it integrates:

1. **File and Folder Management**: Students can upload, organize, and delete files and folders, similar to a cloud storage system but tailored for academic use.
2. **Study Timer**: A Pomodoro-style timer helps students manage their study and break times effectively.
3. **Event Calendar**: A dynamic calendar allows students to schedule and manage their academic and personal events.
4. **Contact Form**: A fully functional contact form enables users to send messages, which are delivered via email.

The **complexity** of this project lies in the integration of these diverse functionalities into a single platform. Each feature requires a different set of skills and technologies:

- **Backend Logic**: Django handles user authentication, file storage, event management, and email sending.
- **Frontend Interactivity**: JavaScript and Bootstrap are used to create a responsive and dynamic user interface, including the interactive study timer and calendar.
- **Database Management**: SQLite (by default in Django) stores user data, files, folders, and events, requiring careful design of models and relationships.
- **Third-Party Libraries**: The project uses external libraries like FullCalendar for the calendar functionality, demonstrating the ability to integrate and customize third-party tools.

Moreover, the project goes beyond the basic CRUD (Create, Read, Update, Delete) operations seen in many other projects. For example:
- The **file management system** supports nested folders and recursive deletion, which adds complexity to the backend logic.
- The **study timer** includes sound notifications and customizable study/break cycles, requiring precise timing and event handling in JavaScript.
- The **calendar** allows for dynamic event creation, editing, and deletion, with real-time updates to the UI.

In summary, this project is **distinct** because it addresses multiple needs of students in one platform, and it is **complex** due to the integration of various technologies and the advanced features implemented in each functionality.

---

## Project Structure

### Main Files and Their Contents

- **`README.md`**: This file, providing an overview of the project, its distinctiveness, complexity, and instructions for running it.
- **`requirements.txt`**: Lists all Python packages required to run the application.
- **`manage.py`**: The Django command-line utility for administrative tasks.
- **`fproject/`**: The main Django application directory.
  - **`settings.py`**: Configuration settings for the Django project, including database, static files, and email settings.
  - **`urls.py`**: URL routing for the entire project.
- **`Capstone/templates/`**: Contains HTML templates for the application.
  - **`layout.html`**: The base template that other templates extend.
  - **`index.html`**: The homepage, displaying recent files and upcoming events.
  - **`files.html`**: The file management interface.
  - **`folder_files.html`**: The interface for viewing files within a specific folder.
  - **`clock.html`**: The study timer interface.
  - **`calendar.html`**: The event calendar interface.
  - **`contact.html`**: The contact form and FAQ section.
  - **`login.html`**, **`register.html`**: Authentication pages.
- **`Capstone/static/`**: Contains static files such as CSS, JavaScript, and sounds.
  - **`styles.css`**: Custom CSS for styling the application.
  - **`clock.js`**: JavaScript logic for the study timer.
  - **`functions.js`**: JavaScript functions for file and folder management.
  - **`sounds/`**: Audio files for timer notifications.
- **`Capstone/models.py`**: Defines the database models for users, files, folders, and events.
- **`Capstone/views.py`**: Contains the view functions for handling requests and rendering templates.
- **`Capstone/forms.py`**: Defines forms for file uploads, event creation, and user registration.
- **`Capstone/urls.py`**: URL routing for the Capstone application.

---

## How to Run the Application

### Prerequisites
1. **Python**: Ensure Python 3.x is installed on your system.
2. **Pip**: Ensure Pip is installed to manage Python packages.

### Installation Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/student-organization-platform.git
   cd student-organization-platform
   ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up the database**:
    ```bash
    python manage.py migrate
    ```

4. **Create a superuser** (optional, for admin access):
    ```bash
    python manage.py createsuperuser
    ```

5. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

6. **Access the application**:
    ```bash
    Open your browser and navigate to http://127.0.0.1:8000/
    ```

## Additional Information

### Email Configuration

To enable the contact form to send emails, you need to configure the email settings in settings.py. For example:
```bash
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_password'
```

### Security Considerations

Environment Variables: Sensitive information like email credentials should be stored in environment variables using python-decouple.

CSRF Protection: Django's built-in CSRF protection is enabled to secure forms.

## Conclusion

This project is a comprehensive platform designed to help students organize their academic lives. It combines file management, time management, and event planning into a single application, making it a unique and valuable tool. The integration of multiple functionalities, along with the use of diverse technologies, demonstrates both the distinctiveness and complexity of the project. I hope you enjoy using it as much as I enjoyed building it!