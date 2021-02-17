from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Grocery(db.Model):
    """Класс описывает таблицу базы данных"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Grocery {self.name}>'


@app.route('/', methods=['GET', 'POST'])
def index():
    """Function represents index page"""
    if request.method == 'POST':  # если форму заполнили и отправили
        name = request.form['name']  # взять name из формы
        if len(name) > 1:
            new_stuff = Grocery(name=name)  # и записать продукт в БД
        else:
            return render_template('404.html', message='You can not adding an empty element!'), 404

        try:  # попробовать
            db.session.add(new_stuff)  # добавить запись в БД
            db.session.commit()  # применить изменения
            return redirect('/')  # в случае успеха, вернуть пользователя на главную страницу
        except:  # если что-то пошло не так
            return 'There was a problem adding new item!'  # отобразить сообщение с ошибкой
    else:
        groceries = Grocery.query.order_by(Grocery.created).all()
        return render_template('index.html', items=groceries)


@app.route('/delete/<int:id>')
def delete(id):
    grocery = Grocery.query.get_or_404(id)
    try:
        db.session.delete(grocery)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting item.'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    grocery = Grocery.query.get_or_404(id)

    if request.method == 'POST':
        grocery.name = request.form['name']
        # заменяю имя продукта на новое имя из формы
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating data.'
    else:
        title = 'Update product'
        return render_template('update.html', title=title, grocery=grocery)


@app.errorhandler(404)
def error_404(error):
    return render_template('404.html', title='Ошибка!'), 404
        
if __name__ == '__main__':
    app.run(debug=True, port=8910)
