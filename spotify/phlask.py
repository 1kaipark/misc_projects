from flask import Flask, request

app = Flask(__name__)

@app.route('/callback')
def callback():
    return "h"
    # # Extract the authorization code from query parameters
    # code = request.args.get('code', '')
    # if code:
    #     # Here, you'd typically exchange the code for a token
    #     return f"Authorization code: {code}"
    # else:
    #     return "No code provided", 400

if __name__ == '__main__':
    app.run(port=8888)
