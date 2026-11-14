from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange

CATEGORIES = [
    'Електроніка',
    'Смартфони',
    'Аксесуари',
    'Побутова техніка',
    'Інше'
]

class ProductForm(FlaskForm):
    name = StringField('Назва товару', validators=[
        DataRequired(message="Це поле є обов'язковим"),
        Length(min=3, message="Назва має містити щонайменше 3 символи")
    ])
    
    content = TextAreaField('Опис товару', validators=[
        DataRequired(message="Це поле є обов'язковим")
    ], render_kw={"rows": 5, "cols": 40})
    
    price = DecimalField('Ціна ($)', places=2, validators=[
        DataRequired(message="Це поле є обов'язковим"),
        NumberRange(min=0.01, message="Ціна повинна бути додатним числом")
    ])
    
    category = SelectField('Категорія', choices=CATEGORIES, validators=[
        DataRequired(message="Виберіть категорію")
    ])
    
    quantity = IntegerField('Кількість одиниць', validators=[
        InputRequired(message="Це поле є обов'язковим"),
        NumberRange(min=0, message="Кількість не може бути від'ємною")
    ])
    
    image = FileField('Зображення товару', validators=[
        FileAllowed(['png', 'jpg', 'jpeg'], 'Дозволено тільки формати PNG, JPG, JPEG!')
    ])
    
    submit = SubmitField('Зберегти')