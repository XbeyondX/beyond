from flask import flash
from flask import render_template
from flask import request
from . import index_blue

from day_06.blueprint.book_1 import AddBookForm, Author, db, Book


@index_blue.route('/', methods=['GET', 'POST'])
def index():
    book_form = AddBookForm()
    if book_form.validate_on_submit():
        author_name = book_form.author.data
        book_name = book_form.book.data
        # author_name = request.form.get('author')
        # book_name = request.form.get('book')
        author = Author.query.filter(Author.name==author_name ).first()


        if not author:
            try:
                author = Author(name=author_name)

                db.session.add(author)
                db.session.commit()

                book = Book(name=book_name, author_id=author.id)
                db.session.add(book)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
                flash('添加失败')
        else:
            book = Book.query.filter(Book.name==book_name).first()
            if not book:
                try:
                    book = Book(name=book_name, author_id=author.id)
                    db.session.add(book)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash('添加失败')
            else:
                flash('该书已存在')
    else:
        if request.method == 'POST':
            flash('参数错误')


    db.session.commit()
    author = Author.query.all()
    return render_template('demo_book.html', authors=author, form=book_form)