from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(min=3, max=150, message="Довжина має бути від 3 до 150 символів")
    ])
    content = TextAreaField('Текст поста', validators=[
        DataRequired(message="Це поле обов'язкове")
    ])
    category = SelectField('Категорія', choices=[
        ('news', 'Новини'),
        ('publication', 'Публікація'),
        ('tech', 'Технології'),
        ('other', 'Інше')
    ], default='news')
    submit = SubmitField('Зберегти')