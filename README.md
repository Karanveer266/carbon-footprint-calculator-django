# Carbon Footprint Calculator

A Django web application that calculates and analyzes carbon footprints based on user activities and food consumption patterns.

## Features

- User activity-based carbon footprint calculation
- Food invoice/receipt analysis for carbon impact
- Personalized recommendations for reducing carbon footprint
- User accounts for tracking progress over time

## Technology Stack

- Django 4.2+
- TailwindCSS for styling
- Gemma 3 LLM API for carbon footprint analysis
- Python-dotenv for environment variable management

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js and npm (for TailwindCSS)
- Virtual environment tool (venv, virtualenv, etc.)

### Installation

1. Clone the repository

```bash
git clone <repository-url>
cd carbon_footprint_django
```

2. Create and activate a virtual environment

```bash
python -m venv env
# On Windows
env\Scripts\activate
# On macOS/Linux
source env/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables

Create a `.env` file in the project root with the following variables:

```
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here

# API Keys
GEMMA_API_KEY=your-gemma-api-key
```

5. Run migrations

```bash
python manage.py migrate
```

6. Install TailwindCSS dependencies

```bash
cd theme/static_src
npm install
```

7. Start the development server

```bash
python manage.py runserver
```

## Deployment

### Production Setup

1. Update the `.env` file with production settings:

```
DEBUG=False
SECRET_KEY=your-secure-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database settings (if using PostgreSQL)
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432

# API Keys
GEMMA_API_KEY=your-gemma-api-key
```

2. Collect static files

```bash
python manage.py collectstatic --settings=carbon_footprint.settings_prod
```

3. Run with a production server like Gunicorn

```bash
gunicorn carbon_footprint.wsgi:application --env DJANGO_SETTINGS_MODULE=carbon_footprint.settings_prod
```

## Directory Structure

- `accounts/` - User authentication and profile management
- `calculator/` - Core carbon footprint calculation functionality
- `carbon_footprint/` - Project settings and configuration
- `media/` - User-uploaded files
- `templates/` - Global templates
- `theme/` - TailwindCSS configuration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.