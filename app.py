from flask import Flask
from flask import send_file
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import jsonify
import mysql.connector
import setting
import save_collect_data
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "this is home page"

@app.route("/index/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        userName = request.form["username"]
        passWord = request.form["password"]
        print("password : ", passWord)
        print("username : ", userName)
        if userName == setting.USER and passWord == setting.PASSWORD:
            session['userName'] = userName
            print("session", session)
            return jsonify(isValid = True)
        else:
            return jsonify(isValid = False)
    else:
        return render_template("index.html")
        
@app.route("/return_file/")
def return_file():
    date = request.args.get("date")
    shop_list = save_collect_data.collect_ww_state(date)
    filename = "data/data.xlsx"
    save_collect_data.convert_data_to_xlsx(shop_list, filename)
    return send_file("data/data.xlsx", as_attachment=True)



@app.route("/chooseDate/", methods = ["GET", "POST"])
def chooseDate():
    if request.method == "POST":
        Year = request.form["Year"]
        Month = request.form["Month"]
        Day = request.form["Day"]
        if "userName" in session:
            return jsonify(success = str(Year) + "-" + str(Month) + "-" + str(Day))
        else:
            return jsonify(fail = "yes")
    else:
        return render_template("date-picker.html")



app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run()