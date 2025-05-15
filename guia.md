#inicia el entrono virtual
venv\Scripts\activate  

#si no puedes iniciar el entorno
python -m venv venv

#actualiza los requirements cada que descargues algo
pip freeze > requirements.txt