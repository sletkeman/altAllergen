"""
    Entry point for this Flask application
"""

from os import path
from flask import render_template, send_from_directory
from flask_cors import CORS
import connexion

# Create the application instance
flask_app = connexion.App(__name__)

# Read the swagger.yml file to configure the endpoints
flask_app.add_api('swagger.yml')

app = flask_app.app

CORS(app)

# Create a URL route in our application for "/"
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """renders the template 'index.html' at /"""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """gets the favicon"""
    return send_from_directory(
        path.join(app.root_path, 'templates'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
           