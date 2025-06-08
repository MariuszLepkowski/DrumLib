<img src=DrumLib/static/assets/img/drumlib-logo2.png alt="Alt Text" style="width:70%; height:auto;">

**DrumLib** is a self-developed web application created out of a passion for music, drumming, and backend development. It allows users to explore profiles of legendary drummers, browse their discographies, and listen to related tracks using a built-in custom audio player.

The project also includes social features such as user registration, login, profile editing, and the ability to comment and suggest new content.

---

## Project Goals

The main goal of **DrumLib** was to serve as a learning environment for mastering backend development with Django. From designing the architecture to deployment and containerization – this project reflects my self-taught journey and growth as a developer.

---

## 🔧 Tech Stack

- **Backend:** Python 3.11, Django 4.x  
- **Frontend:** Django Templates, HTML/CSS, JavaScript (custom audio player)  
- **Database:** PostgreSQL  
- **DevOps:** Docker, Docker Compose, Nginx, Gunicorn, Let's Encrypt (SSL)  
- **Testing:** `pytest`, `pytest-django`  
- **Hosting:** DigitalOcean VPS (Ubuntu)  

---

## Project Structure

The project follows Django’s modular architecture, with each app responsible for specific features:

```
DrumLib/
├── DrumLib/                    # Django project config (settings, URLs, WSGI)
├── drummers_app/              # Drummer profiles and photos
├── discography_app/           # Albums, tracks, and views
├── album_generator_app/       # Random album generator
├── comments_app/              # User comments
├── suggestions_app/           # Suggest new content
├── user_management_app/       # Auth, registration, profiles
├── home_app/                  # Landing page
│
├── templates/                 # HTML templates grouped by app
├── static/                    # CSS, JS, images
│
├── manage.py                  # Django CLI runner
│
├── requirements.txt           # Base dependencies
├── requirements-dev.txt       # Dev environment dependencies
├── requirements-prod.txt      # Production dependencies
│
├── Dockerfile                 # Dev Docker image
├── Dockerfile.prod            # Production Docker image
├── docker-compose.yml         # Dev service orchestration
├── docker-compose.prod.yml    # Prod service orchestration
├── .env                       # Environment variables (used in both modes)
└── README.md                  # Project documentation


```
---

## Features

-  **Custom audio player** – built in vanilla JavaScript, supports play, pause, seek, volume control (YouTube-based)
-  **Drummer exploration** – detailed artist pages
-  **Discographies** – albums and track listings for each drummer
-  **Random album generator** – pick a random record by a selected drummer
-  **Community features** – user accounts, comments, profile management
-  **Content suggestions** – users can submit ideas for new drummers and albums
-  **Admin panel** – Django admin interface for content and user management

---

## Deployment & Hosting

The application is deployed on a **DigitalOcean VPS** using:

- **Docker** for containerization (separate containers for Django app & PostgreSQL DB)
- **Nginx** as a reverse proxy and SSL termination (Let's Encrypt certificates)
- **Gunicorn** as the WSGI HTTP server

Production environment setup includes `.env` variables and separate configuration files for local and production builds.

---

## Testing

All apps include unit and integration tests using:

- `pytest`
- `pytest-django`

---

## What I Learned

Building DrumLib from scratch helped me develop key backend and DevOps skills:

### Backend
- Designing modular Django architecture
- Building application logic (FBVs, CBVs)
- Handling forms, views, templates

### Databases
- Modeling data with Django ORM
- Using PostgreSQL
- Managing migrations and schema evolution

### Testing
- Writing unit and integration tests with pytest

### Frontend
- Implementing interactive components in JavaScript
- Designing a responsive UI with plain HTML/CSS

### DevOps
- Creating Docker containers for dev & production
- Configuring Nginx, Gunicorn, and environment variables
- Hosting and managing the app on a VPS

### Workflow & Version Control
- Using Git for version control
- Managing dependencies and environments

---

## Live Demo & Repository

- **Live App:** [https://drumlib.duckdns.org/](https://drumlib.duckdns.org/)
- **Source Code:** [github.com/MariuszLepkowski/DrumLib](https://github.com/MariuszLepkowski/DrumLib)

---

