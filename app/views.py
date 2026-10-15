from flask import request, redirect, url_for, render_template, abort
from . import app

@app.route('/')
def main():
    return render_template("index.html", title="Резюме")

@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template("homepage.html", agent=agent)