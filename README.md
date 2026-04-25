# Online Exam Portal

## Project Overview

Online Exam Portal is a web-based examination management system developed using Flask and SQLite. It is designed to simplify the process of conducting online exams for educational institutions by providing separate modules for Admins and Students.

The system allows administrators to create exams, manage questions, monitor students, and evaluate results, while students can register, log in, attend exams, and view their results securely.

This project helps reduce manual work, improves exam management efficiency, and supports a smooth digital examination process.

---

## Features

### Admin Module

* Admin Login Authentication
* Create New Exams
* Add and Manage Questions
* View Student Performance
* Monitor Exam Activity
* Result Management
* Dashboard for Full Control

### Student Module

* Student Registration and Login
* Secure Exam Access
* Attempt Online Exams
* View Detailed Results
* Performance Tracking
* User-Friendly Dashboard

### Additional Features

* Flask-Based Backend
* SQLite Database Integration
* Responsive Frontend using HTML, CSS, JavaScript
* Session Management
* Proctoring Support
* Result Analysis

---

## Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask

### Database

* SQLite

### Tools Used

* Visual Studio Code
* Git
* GitHub

---

## Project Structure

```text
online_exam_portal/
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── admin/
│   ├── student/
│   ├── base.html
│   ├── login.html
│   └── register.html
│
├── instance/
│   └── exam_hall.db
│
├── app.py
├── models.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/Sumedha-15/online_exam_portal.git
```

### Step 2: Move into Project Folder

```bash
cd online_exam_portal
```

### Step 3: Create Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate Virtual Environment

### For Windows

```bash
venv\Scripts\activate
```

### For Mac/Linux

```bash
source venv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the Project

```bash
python app.py
```

---

## Real-World Use Case

This project can be used by:

* Colleges and Universities
* Schools
* Coaching Institutes
* Online Certification Platforms
* Training Organizations

It helps institutions conduct secure and efficient online examinations without heavy manual management.

---

## Limitations

* Basic proctoring only
* SQLite is not ideal for very large-scale systems
* No AI-based cheating detection
* Limited scalability for enterprise-level use

---

## Future Scope

* AI-Based Proctoring System
* Face Detection and Anti-Cheating Features
* Email Notifications
* Performance Analytics Dashboard
* Cloud Deployment
* Multi-Institution Support
* Live Exam Monitoring
* Certificate Generation

---

## Author

Developed by Sumedha Modi
Lovely Professional University

Aspiring Software Engineer | Full-Stack Developer | Python & Flask Enthusiast

---

## GitHub Repository
https://github.com/Sumedha-15/online_exam_portal


---
