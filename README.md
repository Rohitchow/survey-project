# Survey Management System

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
  - [1. Cloning the Repository](#1-cloning-the-repository)
  - [2. Creating and Activating a Virtual Environment](#2-creating-and-activating-a-virtual-environment)
  - [3. Installing Dependencies](#3-installing-dependencies)
  - [4. Configuring the Database](#4-configuring-the-database)
  - [5. Applying Migrations](#5-applying-migrations)
  - [6. Running the Development Server](#7-running-the-development-server)
- [Usage](#usage)
  - [Registering Users](#registering-users)
  - [Creating Surveys](#creating-surveys)
  - [Taking Surveys](#taking-surveys)
  - [Viewing Survey Results](#viewing-survey-results)
- [Project Structure](#project-structure)

---

## Overview
The **Survey Management System** is a Django-based web application that allows users to register as survey creators or survey takers. Creators can design, manage, and analyze surveys, while takers can participate in published or republished surveys.

---

## Features
- **User Roles**:
  - Survey Creator: Design and manage surveys.
  - Survey Taker: View and participate in available surveys.
- **Survey Management**:
  - Create, publish, close, and republish surveys.
  - Add questions with at least 4 options.
- **Results Dashboard**:
  - Aggregated answers with counts and percentages.
  - View total participants for each survey.

---

## Requirements
- **Python**: 3.10 or later
- **PostgreSQL**: Database backend
- **Git**: For cloning the repository

---

## Setup Instructions

### 1. Cloning the Repository
Clone the repository to your local machine:
```bash
git clone <repository_url>
cd survey2final
```

### 2. Creating and Activating a Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```
### 3. Installing Dependencies
Install the required Python libraries by running the following command in your terminal:

```bash
pip install -r requirements.txt
```

### 4. Configuring the Database

1. **Create a PostgreSQL Database**:
   - Access your PostgreSQL shell and execute the following command to create a new database:
     ```sql
     CREATE DATABASE survey_management;
     ```

2. **Update the `DATABASES` Configuration in `settings.py`**:
   - Open the `settings.py` file in your Django project.
   - Locate the `DATABASES` dictionary and modify it as follows:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'survey_management',  # Replace with your database name
             'USER': '<your_postgres_username>',  # Replace with your PostgreSQL username
             'PASSWORD': '<your_postgres_password>',  # Replace with your PostgreSQL password
             'HOST': 'localhost',  # Database host
             'PORT': '5432',  # Database port (default is 5432)
         }
     }
     ```
   - Replace `<your_postgres_username>` and `<your_postgres_password>` with your actual PostgreSQL credentials.

   **Note**: Ensure that the PostgreSQL server is running and that the specified user has the necessary permissions for the `survey_management` database.

### 5. Applying Migrations

To set up the database schema, run the following commands:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Running the Development Server

To start the development server, run the following command:

```bash
python manage.py runserver
```
After starting the server, visit the following URL in your browser:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

This will load the homepage of the application.

## Usage

### Registering Users
- **Survey Creators**: Register using the **Register as Survey Creator** form.
- **Survey Takers**: Register using the **Register as Survey Taker** form.

### Creating Surveys
1. Log in as a Survey Creator.
2. Create a survey by providing a name and description.
3. Add at least five questions, each with four options.
4. Publish the survey once it's ready.

### Taking Surveys
1. Log in as a Survey Taker.
2. View available surveys.
3. Participate in surveys that are published or republished.

### Viewing Survey Results
- **Survey Creators**: View aggregated responses and statistics for their published or closed surveys.

## Project Structure

```plaintext
survey2final/                # Django project folder
├── survey/                  # Project folder
│   ├── settings.py          # Project settings
│   ├── urls.py              # Project URL configuration
│   ├── wsgi.py              # WSGI application
│   ├── asgi.py              # ASGI application
├── surveyapp/               # Main application folder
│   ├── models.py            # Database models
│   ├── views.py             # Application views
│   ├── templates/           # HTML templates
│   ├── static/              # Static files (CSS/JSS)
│   ├── urls.py              # App URL configuration
├── manage.py                # Django command-line utility
├── requirements.txt         # Python dependencies
```







