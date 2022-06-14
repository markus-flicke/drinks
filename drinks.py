
from email.policy import default
from flask import Flask, session, redirect, url_for, render_template, flash
from helper_functions import *
from config import *
from secrets import FLASK_SECRET_KEY
import os
from flaskext.autoversion import Autoversion


app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
app.autoversion = True
Autoversion(app)

@app.route("/", defaults={'message': None})
@app.route("/<string:message>")
def index(message):
    if "username" in session:
        print(session['user_id'])
        print(session['username'])
    else:
        return redirect(url_for("select_name"))
    return render_template("select_drink.html", 
                            drink_image_static_paths=[os.path.join('drinks', path) for path in  os.listdir('static/drinks')], 
                            snack_image_static_paths=[os.path.join('snacks', path) for path in  os.listdir('static/snacks')],
    message=message)

@app.route("/select_name")
def select_name():
    return render_template('select_name.html', users = getGroupMembers(SPLITWISE_GROUP_ID))

@app.route("/set_user/<user_id>/<username>")
def set_user(user_id, username):
    session['username'] = username
    session['user_id'] = user_id
    return redirect(url_for('index'))
import re
@app.route("/pay/<filename>")
def pay(filename):
    amount = re.findall("_([\w\W]+)\.", filename)[0]
    product_name = filename.split('_')[0]

    add_expense(amount, session['user_id'], description=product_name, group_id=SPLITWISE_GROUP_ID)
    return redirect(url_for('index', message = "Paid {}€ for {}".format(amount, product_name)))

@app.route("/refund")
def refund():
    add_expense(-0.25, session['user_id'], description="Bottle refund", group_id=SPLITWISE_GROUP_ID)
    return index(message="You have been refunded (25¢).")


if __name__=='__main__':
    app.run()