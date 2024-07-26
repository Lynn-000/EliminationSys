from flask import Blueprint,render_template,request,flash,g,redirect,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Administrators
from flask_login import login_user, login_required, logout_user, current_user
from . import db
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        usernameentered = request.form.get('Username')
        passwordentered = request.form.get('Password') 

        user = Administrators.query.filter_by(Username = usernameentered).first()
        if user:
            if check_password_hash(user.Password, passwordentered):
                flash('Successfully logged in!', category = 'success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect username and password combination or user does not exist.', category = 'error')
        else:
            flash('Incorrect username and password combination or user does not exist.', category = 'error')
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
