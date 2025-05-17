#inicia el entrono virtual
venv\Scripts\activate  

iniciar el entormno virtual en el vps
source venv/bin/activate

instalar los requirements
pip install -r requirements.txt

salir del entorno virtual
deactivate


#si no puedes iniciar el entorno
python -m venv venv

#actualiza los requirements cada que descargues algo
pip freeze > requirements.txt

abrir vps
& "C:\Windows\System32\OpenSSH\ssh.exe" root@173.212.225.35


iniciar servidor fast api
 uvicorn server:app --reload       

 iniciar servidor en vps
 uvicorn server:app --host 0.0.0.0 --port 800

llamada prueba dorado
http://127.0.0.1:8000/eldorado/run?limit=10&amount_currency_id=USD&crypto_currency_id=TATUM-TRON-USDT&fiat_currency_id=USD&payment_methods=app_zinli_us&show_user_offers=true&show_favorite_mm_only=false