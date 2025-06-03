@echo off

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit the .env file with your Hetzner credentials
)

echo Setup complete! Don't forget to:
echo 1. Edit the .env file with your credentials
echo 2. Activate the virtual environment with 'venv\Scripts\activate' when working on the project 