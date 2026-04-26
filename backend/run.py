import os
from api import create_app



# create the Flask application
app = create_app("config")


# route frontend
@app.route('/')
def index():
    return app.send_static_file('index.html')


# run the application
if __name__ == "__main__":
    flagDebug = os.environ.get('CHRYSELIS_FLASK_ENV') == 'development'
    app.run(debug=flagDebug)