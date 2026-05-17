# ConnectX — Campus Collaboration & Student Networking Platform

ConnectX is a production-ready campus collaboration and networking platform designed specifically for college students to connect, form teams, and showcase their technical achievements. 

## Features
- **User Authentication:** Secure registration and login using Flask-Login and Werkzeug hashing.
- **Student Profiles:** Customizable profiles with avatars, bio, skills, and social links.
- **Social Feed:** Share updates, projects, and achievements. Like and save posts.
- **Collaboration Module:** Find teammates for your next hackathon or academic project. Create requests specifying project details and required skills.
- **Communities:** Join or create clubs/groups for focused technical discussions.
- **Messaging:** Direct messaging between users.
- **Notifications:** Real-time feedback for likes, comments, and collaboration applications.
- **Premium UI:** Glassmorphism design, gradient backgrounds, and responsive layout without relying on heavy frontend frameworks.

## Tech Stack
- **Backend:** Flask, Flask-SQLAlchemy, Flask-Login, Flask-Migrate
- **Database:** MySQL
- **Frontend:** HTML5, CSS3, Bootstrap 5, Vanilla JS

## Installation Guide

1. **Clone the repository** (if applicable) or navigate to the project folder:
   ```bash
   cd ConnectX
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Database Configuration:**
   Ensure MySQL is running on your machine.
   Update the `DATABASE_URL` in `.env` if necessary. (Default: `mysql+pymysql://root:@localhost/connectx_db`)
   Create the database in MySQL:
   ```sql
   CREATE DATABASE connectx_db;
   ```

6. **Initialize and migrate the database:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. **Run the application:**
   ```bash
   python run.py
   ```

The server will start on `http://127.0.0.1:5000/`.
