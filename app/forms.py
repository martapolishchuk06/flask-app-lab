import re
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError

class ContactForm(FlaskForm):
    name = StringField('Ім\'я', validators=[
        DataRequired(message="Це поле є обов'язковим"),
        Length(min=4, max=10, message="Довжина імені має бути від 4 до 10 символів")
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message="Це поле є обов'язковим"),
        Email(message="Введіть коректну електронну адресу")
    ])
    
    phone = StringField('Телефон', validators=[
        Regexp(r'^\+380\d{9}$', message="Формат телефону повинен бути: +380XXXXXXXXX")
    ])
    
    subject = SelectField('Тема звернення', choices=[
        'Загальне питання',
        'Технічна підтримка',
        'Співпраця',
        'Інше'
    ], validators=[DataRequired(message="Виберіть тему")])
    
    message = TextAreaField('Повідомлення', validators=[
        DataRequired(message="Це поле є обов'язковим"),
        Length(max=500, message="Повідомлення не повинно перевищувати 500 символів")
    ])
    
    submit = SubmitField('Send Message')