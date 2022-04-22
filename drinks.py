from flask import Flask, session, redirect, url_for, render_template
from helper_functions import *
from config import *
from secrets import FLASK_SECRET_KEY
import os
from flaskext.autoversion import Autoversion


app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
app.autoversion = True
Autoversion(app)

@app.route("/")
def index():
    if "username" in session:
        print(session['user_id'])
        print(session['username'])
    else:
        return redirect(url_for("select_name"))
    return render_template("select_drink.html", drink_image_filenames=os.listdir('static'))

@app.route("/select_name")
def select_name():
    return render_template('select_name.html', users = getGroupMembers(SPLITWISE_GROUP_ID))

@app.route("/set_user/<user_id>/<username>")
def set_user(user_id, username):
    session['username'] = username
    session['user_id'] = user_id
    return redirect(url_for('index'))

@app.route("/pay/<filename>")
def pay(filename):
    product_name, amount = filename[:-4].split('_')
    add_expense(amount, session['user_id'], description=product_name, group_id=SPLITWISE_GROUP_ID)
    return render_template("success.html", filename=filename)



if __name__=='__main__':
    app.run()