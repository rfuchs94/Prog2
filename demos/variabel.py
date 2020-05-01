
from flask import Flask
from flask import render_template
from flask import request

app = Flask("templates")


@app.route("/variabel/")
def hello():
    dinger = ["Eins", "Zwei", "Drei"]
    zahl = 6

    name = input("Wie heissst du")
    if name == "Robin":
        print("cool das du da bist!")
    return render_template("variabel.html",dinger=dinger, zahl=zahl)



if __name__ == "__main__":
    app.run(debug=True, port=5000)


