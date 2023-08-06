from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")