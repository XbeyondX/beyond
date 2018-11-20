from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask.ext.wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from index import index_blue
from delete import delete_blue



app = Flask(__name__)

app.register_blueprint(index_blue)
app.register_blueprint(delete_blue)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/book'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.secret_key = '13edsf'




class AddBookForm(FlaskForm):
    author = StringField('作者：', validators=[InputRequired('请输入读者')])  # 错误验证
    book = StringField('书名：', validators=[InputRequired('请输入书名')])
    submit = SubmitField('添加')

class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    books = db.relationship('Book', backref='author')
    # def __repr__(self):
    #     return 'Author:%s' %self.name


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    # def __str__(self):
    #     return 'Book:%s,%s'%(self.info,self.lead)

# @app.route('/delete_author/<author_id>')
# def delete_author(author_id):
#     try:
#         author = Author.query.get(author_id)
#     except Exception as e:
#         print(e)
#         return '查询错误'
#     if not author:
#         return '作者不存在'
#     try:
#         Book.query.filter(Book.author_id==author_id).delete()
#         db.session.delete(author)
#         db.session.commit()
#     except Exception as e:
#         print(e)
#         db.session.rollback()
#         return '删除失败'
#     return redirect(url_for('index'))
#
#
# @app.route('/delete_book/<book_id>')
# def delete_book(book_id):
#     try:
#         book = Book.query.get(book_id)
#         author = book.author
#     except Exception as e:
#         print(e)
#         return '查询失败'
#     if not book:
#         return '书籍不存在'
#     try:
#         db.session.delete(book)
#         db.session.commit()
#         book_count = Book.query.filter(Book.author_id==author.id).count()
#         if book_count == 0:
#             db.session.delete(author)
#             db.session.commit()
#     except Exception as e:
#         print(e)
#         db.session.rollback()
#         return '删除失败'
#
#     return redirect(url_for('index'))
#
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     book_form = AddBookForm()
#     if book_form.validate_on_submit():
#         author_name = book_form.author.data
#         book_name = book_form.book.data
#         # author_name = request.form.get('author')
#         # book_name = request.form.get('book')
#         author = Author.query.filter(Author.name==author_name ).first()
#
#
#         if not author:
#             try:
#                 author = Author(name=author_name)
#
#                 db.session.add(author)
#                 db.session.commit()
#
#                 book = Book(name=book_name, author_id=author.id)
#                 db.session.add(book)
#                 db.session.commit()
#             except Exception as e:
#                 db.session.rollback()
#                 print(e)
#                 flash('添加失败')
#         else:
#             book = Book.query.filter(Book.name==book_name).first()
#             if not book:
#                 try:
#                     book = Book(name=book_name, author_id=author.id)
#                     db.session.add(book)
#                     db.session.commit()
#                 except Exception as e:
#                     print(e)
#                     flash('添加失败')
#             else:
#                 flash('该书已存在')
#     else:
#         if request.method == 'POST':
#             flash('参数错误')
#
#
#
#     author = Author.query.all()
#     return render_template('demo_book.html', authors=author, form = book_form)
#


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    au1 = Author(name='老王')
    au2 = Author(name='老尹')
    au3 = Author(name='老刘')
    # 把数据提交给用户会话
    db.session.add_all([au1, au2, au3])
    # 提交会话
    db.session.commit()
    bk1 = Book(name='老王回忆录', author_id=au1.id)
    bk2 = Book(name='我读书少，你别骗我', author_id=au1.id)
    bk3 = Book(name='如何才能让自己更骚', author_id=au2.id)
    bk4 = Book(name='怎样征服美丽少女', author_id=au3.id)
    bk5 = Book(name='如何征服英俊少男', author_id=au3.id)
    # 把数据提交给用户会话
    db.session.add_all([bk1, bk2, bk3, bk4, bk5])
    # 提交会话
    db.session.commit()
    app.run(debug=True, port=8080)
