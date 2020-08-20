import os  

from flask import Flask

from . import db
from . import auth
from . import blog

def create_app(test_config=None):
    # create and configure the app
    # __name__은 현재 python module의 이름. path등을 알아내기에 편리 
    # instance_relative_config=True는 보안을 위해 (version control에 올리지 않는) 별도의 instance 폴더에 config정보들을 저장한다는 의미.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # SECRET_KEY : data 보안. random값을 사용할 것 
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'flaskr.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, Flask!'
    

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app    


# export FLASK_APP=flaskr
# export FLASK_ENV=development
# flask run

# flask init-db

# https://flask.palletsprojects.com/en/1.1.x/tutorial/database/

# https://flask.palletsprojects.com/en/1.1.x/tutorial/views/