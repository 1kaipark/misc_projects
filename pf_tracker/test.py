from app import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <h1>Hello World!</h1>
    <p>HI BRO</p>
    """

if __name__ == "__main__":
    app.run(debug=True)