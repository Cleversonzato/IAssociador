from waitress import serve
from src.iniciar import app

serve(app, host='0.0.0.0', port=5000)
