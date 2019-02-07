from app import app

@app.route('/')
def index():
    return 'Portada de mi app web'