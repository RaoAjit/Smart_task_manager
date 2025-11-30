git clone https://github.com/RaoAjit/Smart_task_manager.git
cd task-analyzer

Create a virtual environment:
python3 -m venv venv
source venv/bin/activate     (Mac/Linux)
venv\Scripts\activate        (Windows)
Install backend dependencies:

Copy code
pip install -r backend/requirements.txt
Apply migrations:



cd backend
python manage.py migrate

Run the server:
python manage.py runserver
The backend will run at:
http://127.0.0.1:8000

Frontend:
Open the file:
frontend/index.html
