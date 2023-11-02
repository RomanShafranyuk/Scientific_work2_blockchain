from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
from block import *
import database
import block
import time


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        start = time.time()
        session = database.create_session()
        lender = request.form['lender']
        amount = request.form['amount']
        borrower = request.form['borrower']
        block.write_block(session, name=lender, amount=amount, to_whom=borrower)
        session.close()
        end = time.time()
        time_to_add = end - start
        database.add_time(lender, time_to_add)
        return {}
          
    return render_template('index.html')


# @app.route('/check', methods=['GET'])
# def check():
#     get_average_time()
#     return render_template('index.html')

if __name__ == '__main__':
    session = database.create_session()
    database.init_db(session)
    if database.is_database_empty(session) == True:
        block.write_block(session, "Admin", 10000, "George")
    session.close()
    app.run("25.22.250.163", 5000, debug=True)