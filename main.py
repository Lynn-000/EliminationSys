from website import create_app
#Importing
from jinja2 import Template
from flask import Flask, render_template, redirect, url_for, request, g
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
app = create_app()
if __name__ == '__main__':
    app.run(debug = True)