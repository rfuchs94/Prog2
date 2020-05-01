from flask import Flask
from flask import render_template


app = Flask("templates")


@app.route("/")
def hello():
    return render_template("start.html")

@app.route("/new")
def new():
    return render_template("new.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)