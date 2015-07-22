
from app import app
# app.run(host='0.0.0.0',debug=True)
# app.run(debug = True)
#!flask/bin/python
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=80)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080,debug=True)
