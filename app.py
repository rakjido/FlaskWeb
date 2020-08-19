
from flask import Flask, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route("/hello/")
def hello_flask():
    return "Hello Flask apps???"

@app.route("/profile/<username>")
def show_user_profile(username):
    return "User " + username
    #return "User %s" %escape(username)

@app.route("/post/<username>/<int:post_id>")
def show_user_post(username, post_id):
    return "POST/" + username +"/%d" % post_id    

@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    return 'Subpath %s' % escape(subpath)

@app.errorhandler(404)
def page_not_found(error):
    return '%s' %error

if __name__ == '__main__':
    #app.run(host='0.0.0.0') #외부에서 접근 가능 
    with app.test_request_context():
        print(url_for('show_user_profile', username="Tom Mitchell"))
        print(url_for('show_user_post', username="Tom Mitchell", post_id=32))
        print(url_for('show_subpath', subpath='Colony/23/POST'))

# FLASK_DEBUG=1 flask run
