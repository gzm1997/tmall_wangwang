from flask import Flask
from flask import send_file
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
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
        # 这里需要添加数据库的链接 返回数据的文件
        return "post succeed"
    else:
        return render_template("index.html")
        
@app.route("/return_file/")
def return_file():
    print("return File")
    return send_file("test.xlsx", as_attachment=True)

@app.route("/chooseDate/", methods = ["GET", "POST"])
def chooseDate():
    if request.method == "POST":
        print("Year :", request.form["Year"])
        print("Month :", request.form["Month"])
        print("Day :", request.form["Day"])
        return redirect(url_for("return_file"))
    else:
        return render_template("date-picker.html")

if __name__ == "__main__":
    app.run()