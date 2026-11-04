import logging
from flask import request, redirect, url_for, render_template, abort, flash
from . import app
from .forms import ContactForm

logging.basicConfig(
    filename='contact_form.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

@app.route('/')
def main():
    return render_template("index.html", title="Резюме")

@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template("homepage.html", agent=agent)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data

        try:
            logging.info(f"Форма відправлена: Ім'я: {name}, Email: {email}, Тел: {phone}, Тема: {subject}, Повідомлення: {message}")
            flash('Ваше повідомлення успішно відправлено та збережено!', 'success')
        except Exception as e:
            logging.error(f"Помилка при збереженні даних контактної форми: {e}")
            flash('Виникла помилка під час відправки повідомлення.', 'danger')

        return redirect(url_for('contact'))

    return render_template('contact.html', title='Контакти', form=form)