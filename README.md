# Masterchef Web App

## Overview

The **Masterchef Web App** is a platform designed for cooking enthusiasts to explore, create, and share recipes. Users can browse a variety of recipes, save favorites, create their own recipes, and engage with the community by leaving comments and reviews. The app provides personalized recommendations and includes features like social media sharing and an interactive user dashboard.

## Features

- **Recipe Discovery:** Explore a vast collection of recipes by cuisine, cooking time, ingredients, and dietary preferences.
- **User Authentication:** Secure sign-up, login, and password management using Django’s authentication system.
- **Profile Management:** Users can create personal profiles, save favorite recipes, and organize them into collections.
- **Recipe Creation:** Users can submit their own recipes, including ingredients, instructions, and images.
- **Comments & Reviews:** Engage with other users by adding comments and reviews on shared recipes.
- **Recommendations:** Get personalized recipe suggestions based on user activity and preferences.
- **Social Media Integration:** Share your favorite recipes on platforms like Facebook and Twitter.
- **Responsive Design:** Optimized for use on desktops, tablets, and mobile devices.
  
## Technologies Used

- **Frontend:**
  - HTML5
  - CSS3
  - JavaScript (for dynamic interactions)
  - Bootstrap (for responsive design)

- **Backend:**
  - Django (Python)
  - PostgreSQL (Database)

- **Authentication:**
  - Django’s built-in authentication system
  - OAuth (for social media integration)

- **APIs:**
  - Spoonacular API (for additional recipe data)

## Setup Instructions

### Prerequisites

Ensure you have the following installed:

- [Python 3.8+](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/) (or any preferred database)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/masterchef-webapp.git
   cd masterchef-webapp
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root of the project and add the following variables:

   ```bash
   SECRET_KEY=your_django_secret_key
   DEBUG=True  # Change to False in production
   DATABASE_URL=your_postgresql_database_url
   SPOONACULAR_API_KEY=your_spoonacular_api_key
   ```

5. **Set up the database:**

   If you’re using PostgreSQL, ensure it’s running, then apply the migrations:

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   The app will run at `http://127.0.0.1:8000/`.

## Project Structure

```bash
masterchef-webapp/
│
├── masterchef/            # Django project settings
├── recipes/               # Recipes app (core functionality)
│   ├── migrations/        # Database migrations
│   ├── templates/         # HTML templates
│   ├── static/            # Static files (CSS, JS)
│   ├── models.py          # Database models (Recipe, User)
│   ├── views.py           # Application views (logic)
│   ├── forms.py           # Django forms for recipe creation
│   ├── urls.py            # URL routing for the app
│   └── tests.py           # Unit tests
├── users/                 # User management app
├── static/                # Project-wide static files
├── templates/             # Project-wide templates
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Running Tests

You can run the test suite with the following command:

```bash
python manage.py test
```

## Available Scripts

- `python manage.py runserver` – Runs the development server.
- `python manage.py migrate` – Applies database migrations.
- `python manage.py createsuperuser` – Creates an admin user for Django’s admin interface.
- `python manage.py test` – Runs the test suite.

## Deployment

For production, ensure you:

- Set `DEBUG=False` in your `.env` file.
- Use a production-ready database like PostgreSQL or MySQL.
- Configure a WSGI server like Gunicorn.
- Serve static files using a CDN or web server like Nginx.

## Contribution Guidelines

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE.md` file for more details.

## Contact

For any inquiries or support:

- Email: support@masterchefapp.com
- GitHub: [niral-nadisara](https://github.com/niral-nadisara)

---

This README reflects your Django app's structure and setup!
