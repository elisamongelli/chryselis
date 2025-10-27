from api import create_app



# create the Flask application
app = create_app("config")


# run the application
if __name__ == "__main__":
    app.run(debug=True)