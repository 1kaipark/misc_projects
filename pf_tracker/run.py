from application import app

if __name__ == "__main__":
    import os

    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.run(debug = True)