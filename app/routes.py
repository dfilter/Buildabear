from flask import render_template
from app import app


# Route is only used to display something if you decide to visit the api's url.
@app.route('/')
def index():
    return render_template('index.html')
