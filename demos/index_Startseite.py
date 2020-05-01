from flask import Flask
from flask import render_template
from flask import request
import json 
from datetime import date, timedelta
import uuid 
  


def datei_öffnen(datei, standardwert):
    
    try:
        with open (datei, "r", encoding="utf-8") as json_file:
            daten=json.load(json_file)
            return daten
    except Exception:
            return standardwert

def datei_schreiben(datei, daten):
    with open (datei, "w", encoding="utf-8") as json_file:
            json.dump(daten,json_file, indent=4)



app = Flask("demos")

@app.route("/home/", methods=['GET', 'POST'])
def home():
    ausgabe= ""
    hamsterer= ""
    anzahl= ""
    total= ""
    if request.method == 'POST':
        anzahl = int(request.form['wcpapier'])
        total = anzahl * 8
        ausgabe = "Du hast noch genug für ca. " + str(total) + " Tage."
        if total > int(50):
                hamsterer = "Du bist ein Hamsterer!"
        
        
    return render_template("index_startseite.html", ausgabe=ausgabe, hamsterer=hamsterer)

@app.route("/home/")
def neu():
    dinger = ["Eins", "Zwei", "Drei"]
    zahl = 6
    return render_template("index_startseite.html", dinger=dinger, zahl=zahl)

@app.route("/brauche_hilfe", methods=['GET', 'POST'])
def brauche_hilfe():
    alle_eingaben= datei_öffnen("text.json",[])
    ausgabe=""

    if request.method == 'POST':
        eintragsid = uuid.uuid1() 
        vorname = request.form['vorname']
        name = request.form['name']
        weg = request.form['weg']
        plz = request.form['plz']
        ort = request.form['ort']
        eintrag = request.form['eintrag']
        tag = request.form['tag']
        email= request.form['email']
        kommentar= request.form['kommentar']
        ausgabe = "Vielen Dank " + vorname +" "+ name + "! Wir werden uns um Ihr Anliegen schnellst möglich kümmern. Ihr Anliegen '"+ eintrag +"' wird möglichst bis "+tag+ " erledigt. Bei Rückfragen werden wir uns bei Ihnen an " +email+" melden."
        if tag == "Heute":
            tag = str(date.today())
        if tag == "Morgen":
            tag = str(date.today() + timedelta(1))
        if tag == "Übermorgen":
            tag = str(date.today() + timedelta(2))
        if tag == "Bis in einer Woche":
            tag = str(date.today() + timedelta(7))
        if tag == "Bis in zwei Wochen":
            tag = str(date.today() + timedelta(7))

        eingabe_brauche_hilfe = {
            "id": str(eintragsid),
            "Vorname": vorname,
            "Name": name,
            "Adresse": weg,
            "PLZ": plz,
            "Ort": ort,
            "Email": email,
            "Eintrag": eintrag,
            "Frist": tag,
            "Kommentar": kommentar,
            "Status": "offen"
        }

        alle_eingaben.append(eingabe_brauche_hilfe)
        datei_schreiben("text.json",alle_eingaben)
        
    return render_template("brauche_hilfe.html", ausgabe=ausgabe)

@app.route("/biete_hilfe", methods=['GET', 'POST'])
def biete_hilfe():
    if request.method == "POST":
        plz = request.form.get("plz", "")
        suchergebnis = []
        alle_eingaben= datei_öffnen("text.json",[])
        for eingabe in alle_eingaben:
            if eingabe["PLZ"] == plz and eingabe["Status"] == "offen":
                suchergebnis.append(eingabe)

        return render_template("biete_hilfe_resultat.html", suchergebnis = suchergebnis)        
    return render_template("biete_hilfe.html")


@app.route("/erledigt/<id>")
def erledigt(id):
    alle_eingaben= datei_öffnen("text.json",[])
    for eingabe in alle_eingaben:
        if eingabe["id"] == id:
                return render_template("erledigt.html", eingabe = eingabe)

    return render_template("auswahl_name.html")

@app.route("/bestätigt/")
def bestätigt(id):
    if request.method == "POST":
        alle_eingaben= datei_öffnen("text.json",[])
        helfername = request.form.get("helfername","")
        eingabe["Status"] = "erledigt"
        if eingabe["helfername"] == helfername:
            return render_template("bestätigt.html", eingabe=eingabe)
                

    return render_template("erledigt.html")


@app.route("/uebersicht")
def uebersicht():
                
    return render_template("uebersicht.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)


