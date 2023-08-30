from website import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) # debug mode automatically restarts the flask web server after code changes