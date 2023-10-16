from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
from block import *
import database


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        session = database.create_session()
        lender = request.form['lender']
        amount = request.form['amount']
        borrower = request.form['borrower']
        write_block(session, name=lender, amount=amount, to_whom=borrower)
        session.close()
        return {}
          
    return render_template('index.html')


# @app.route('/check', methods=['GET'])
# def check():
#     results = check_integrity()
#     return render_template('index.html', results=results)

if __name__ == '__main__':
    session = database.create_session()
    database.init_db(session)
    if database.is_database_empty(session) == True:
        database.add_block(session, "Admin", 10000, "George", "-", 0)
    session.close()
    app.run("25.22.250.163", 5000, debug=True)