python -m venv venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
$env:FLASK_APP='bikeservice'
flask init-db
deactivate