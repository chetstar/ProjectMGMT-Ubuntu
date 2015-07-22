# from flask import Flask
# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Coming soon!"

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=8080)
#!flask/bin/python
from app import app
# app.run(host='0.0.0.0',debug=True)
# app.run(debug = True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080,debug=True)
