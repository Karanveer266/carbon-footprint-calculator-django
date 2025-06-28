@echo off
REM Deployment helper script for Carbon Footprint Calculator

echo Creating necessary directories...
mkdir logs 2>nul

echo Activating virtual environment...
call env\Scripts\activate.bat

echo Installing requirements...
pip install -r requirements.txt

echo Collecting static files...
python manage.py collectstatic --noinput --settings=carbon_footprint.settings_prod

echo Running migrations...
python manage.py migrate --settings=carbon_footprint.settings_prod

echo.
echo Deployment preparation completed successfully!
echo.
echo To start the server with Gunicorn, run:
echo env\Scripts\activate.bat ^&^& env\Scripts\gunicorn carbon_footprint.wsgi:application --env DJANGO_SETTINGS_MODULE=carbon_footprint.settings_prod

pause