#!/usr/bin/env python
"""
Deployment helper script for Carbon Footprint Calculator

This script helps with common deployment tasks:
1. Collecting static files
2. Running migrations
3. Creating necessary directories
"""

import os
import sys
import subprocess
from pathlib import Path

# Ensure we're in the project directory
BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)

def run_command(command):
    """Run a shell command and print output"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(e.stderr)
        return False

def main():
    # Create necessary directories
    os.makedirs("logs", exist_ok=True)
    print("Created logs directory")
    
    # Activate virtual environment if it exists
    if os.path.exists("env/Scripts/activate"):
        # Windows
        activate_cmd = "env\\Scripts\\activate"
    elif os.path.exists("env/bin/activate"):
        # Unix
        activate_cmd = "source env/bin/activate"
    else:
        print("Virtual environment not found. Please create one first.")
        return
    
    # Install requirements
    if not run_command(f"{activate_cmd} && pip install -r requirements.txt"):
        print("Failed to install requirements")
        return
    
    # Collect static files
    if not run_command(f"{activate_cmd} && python manage.py collectstatic --noinput --settings=carbon_footprint.settings_prod"):
        print("Failed to collect static files")
        return
    
    # Run migrations
    if not run_command(f"{activate_cmd} && python manage.py migrate --settings=carbon_footprint.settings_prod"):
        print("Failed to run migrations")
        return
    
    print("\nDeployment preparation completed successfully!")
    print("\nTo start the server with Gunicorn, run:")
    print(f"{activate_cmd} && gunicorn carbon_footprint.wsgi:application --env DJANGO_SETTINGS_MODULE=carbon_footprint.settings_prod")

if __name__ == "__main__":
    main()