from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_flask():
    return "Hello Flask apps!!!"

if __name__ == '__main__':
    app.run()


# FLASK_DEBUG=1 flask run
