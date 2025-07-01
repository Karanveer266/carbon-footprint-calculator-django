# Deployment link -

http://karan266.pythonanywhere.com

NOTE - I have hosted this app on pythonanywhere.com. So, it takes a lot of time to load different pages.

# DEMO VIDEO 

https://www.dropbox.com/scl/fi/setd1lxfi1nga7aeayhh8/django_cfc_demo.mp4?rlkey=mazqe6qgmwpfqi1v5fqd2m9kz&st=16lbv48r&dl=0

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
- Gemma 3 LLM API for carbon footprint analysis, or any other llm api key as epr your preference
- Python-dotenv for environment variable management

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js and npm (for TailwindCSS)
- Virtual environment tool (venv, virtualenv, etc.)

### Installation

1. Clone the repository

```bash
git clone https://github.com/Karanveer266/carbon-footprint-calculator-django.git
cd carbon-footprint-calculator-django
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

7. Run tailwind and Start the development server

```bash
python manage.py tailwind start
python manage.py runserver
```

## Directory Structure

- `accounts/` - User authentication and profile management
- `calculator/` - Core carbon footprint calculation functionality
- `carbon_footprint/` - Project settings and configuration
- `templates/` - Global templates
- `theme/` - TailwindCSS configuration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.