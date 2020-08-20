import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for 
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# auth라는 이름의 Blueprint 생성. url_prefix를 지정할 수 있다 
bp = Blueprint('auth', __name__, url_prefix ='/auth')

@bp.route('/register', methods = ('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required'
        elif db.execute(    
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(    
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    
    return render_template('auth/login.html')

    @bp.before_app_request
    def load_logged_in_user():
        user_id = session.get('user_id')
            
        if user_id is None:
            g.user = None
        else:
            g.user = get_db().execute( 
                'SELECT * FROM user WHERE id = ?', (user_id,)
            ).fetchone()

    
    @bp.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))

    def login_required(view):
        # 해당 뷰를 검사해서 로그인이 되어 있지 않으면 로그인 페이지로 redirect한다. Spring에서의 AOP와 비슷한 개념 
        @functions.wrap(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for('auth.login'))
            
            return view(**kwargs)
        