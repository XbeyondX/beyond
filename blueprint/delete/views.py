from flask import redirect
from flask import url_for
from book_1 import Author, Book, db
from . import delete_blue


@delete_blue.route('/delete_author/<author_id>')
def delete_author(author_id):
    try:
        author = Author.query.get(author_id)
    except Exception as e:
        print(e)
        return '查询错误'
    if not author:
        return '作者不存在'
    try:
        Book.query.filter(Book.author_id==author_id).delete()
        db.session.delete(author)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return '删除失败'
    return redirect(url_for('index_view.index'))


@delete_blue.route('/delete_book/<book_id>')
def delete_book(book_id):
    try:
        book = Book.query.get(book_id)
        author = book.author
    except Exception as e:
        print(e)
        return '查询失败'
    if not book:
        return '书籍不存在'
    try:
        db.session.delete(book)
        db.session.commit()
        book_count = Book.query.filter(Book.author_id==author.id).count()
        if book_count == 0:
            db.session.delete(author)
            db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return '删除失败'
    return redirect(url_for('index_view.index'))

