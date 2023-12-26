# Django Blog Application

A simple blogging application built with Django, designed to provide a seamless experience for users to create, view, edit, and manage blog posts.

## Features:

-User registration and authentication.

-Create, edit, and delete blog entries.

-View a list of all blog entries.

-Detailed entry view with author details.

-User-specific functionalities: Only the author can edit or delete their posts.


## Requirements
To run this application locally, ensure you have the following installed:

Python 3.x
Django
SQLite or another database system of choice

Other dependencies as listed in requirements.txt

## Installation and Usage
Follow these steps to get the application up and running:

1. Clone the repository and navigate to the directory:

```bash
git clone https://github.com/yourusername/django-blog.git
cd django-blog
```
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```
3. Set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```
4. Run the Django application:
```bash
python manage.py runserver
```
5. Access the application in your web browser:
```bash
http://localhost:8000/blog
```
## Usage:

-User Registration: Navigate to /register/ to create a new user account.

-Login: Access /login/ to log into your account.

-Creating Blog Entries: Use /entry_create/ to add new blog posts.

-Viewing and Managing Entries: Visit /entries_list/ to see all blog entries. Only the authors can edit or delete their respective posts.
