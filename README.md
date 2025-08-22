<div align="center">
<img src=DrumLib/static/assets/img/drumlib-logo2.png alt="Alt Text" style="width:70%; height:auto; display: block; margin-left:auto; margin-right:auto;">
</div>

**DrumLib** is a self-developed web platform developed out of a passion for music, drumming, and programming.
<div align="center">
<img src=DrumLib/static/assets/img/drumlib_home_page.jpg alt="Alt Text" style="width:70%; height:auto; display: block; margin-left:auto; margin-right:auto;">
</div>

It combines three key components:

1. A **music application** with a custom-built audio player for track playback.
2. A **content management system**, allowing easy administration of drummers, albums, and tracks.
3. A **thematic social space**, where users can register, comment, and suggest new content.

<div align="center">
<img src=DrumLib/static/assets/img/drumlib_album_generator.jpg alt="Alt Text" style="width:70%; height:auto; display: block; margin-left:auto; margin-right:auto;">
</div>

The platform lets users explore profiles of iconic drummers, browse their discographies, and listen to albums and tracks featuring their drumming within the platform.

<div align="center">
<img src=DrumLib/static/assets/img/drumlib_drummers_explorer.jpg alt="Alt Text" style="width:70%; height:auto; display: block; margin-left:auto; margin-right:auto;">
</div>

---

## Project Goals

The main goal of **DrumLib** was to serve as a learning environment for mastering backend development with Django. From designing the architecture to deployment and containerization – this project reflects my self-taught journey and growth as a developer.

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


## Tech Stack

- **Backend:** Python 3.11, Django 4.x
- **Frontend:** Django Templates, HTML/CSS, JavaScript (custom audio player)
- **Database:** PostgreSQL
- **DevOps:** Docker, Docker Compose, Nginx, Gunicorn, Let's Encrypt (SSL)
- **Testing:** `pytest`, `pytest-django`
- **Hosting:** DigitalOcean VPS (Ubuntu)

---

## Setup / Running Locally
#### Prerequisites:
- Docker & Docker Compose installed on your machine
- Git

**To run DrumLib locally, follow these steps:**
### 1. Clone the repository
  ```sh
    git clone https://github.com/MariuszLepkowski/DrumLib.git
    cd DrumLib
  ```
### 2. Set up environment variables
Copy the example env file and edit it if needed:
  ```sh
    cp .env.example .env
  ```
### 3. Build and start the containers
If you're on Linux, you might need to use sudo unless your user has Docker permissions:
  ```sh
    docker compose up --build
  ```
This will build the Docker image and start two containers:
- drumlib_web_local (the Django app)
- drumlib_db_local (PostgreSQL database)

App will be available at http://localhost:8000

---
### 4. Run migrations and create superuser (only on first run)
Once containers are up, in a new terminal:
  ```sh
    docker exec -it drumlib_web_local python manage.py migrate
    docker exec -it drumlib_web_local python manage.py createsuperuser
  ```
---

### 5. Access the admin panel

Go to: http://localhost:8000/admin.

Login with the superuser credentials you just created.

**Note:** Some features (like album generator and drummer profiles) require content to be added via the Django Admin Panel.

**The database is empty by default.**

Use the superuser account to populate it after initial setup.

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
## Testing

All apps include unit and integration tests using:

- `pytest`
- `pytest-django`

---

## Deployment & Hosting

The application is deployed on a **DigitalOcean VPS** using:

- **Docker** for containerization (separate containers for Django app & PostgreSQL DB)
- **Nginx** as a reverse proxy and SSL termination (Let's Encrypt certificates)
- **Gunicorn** as the WSGI HTTP server

Production environment setup includes `.env` variables and separate configuration files for local and production builds.

---

## License / Disclaimer

**Disclaimer:** The project has been created by Mariusz Łepkowski as a non-commercial programming portfolio project for educational and recruitment purposes only.

**DrumLib is not licensed for commercial use or redistribution.**

All rights reserved.

---

## Live Demo & Repository

- **Live App:** [https://drumlib.duckdns.org/](https://drumlib.duckdns.org/)
- **Source Code:** [github.com/MariuszLepkowski/DrumLib](https://github.com/MariuszLepkowski/DrumLib)

---
