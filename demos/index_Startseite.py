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

def doppelte_einträge(alle_eingaben):
    alle_id = []
    alle_doppelte_id = []
    for eingabe in alle_eingaben:
        if eingabe["id"] in alle_id:
            alle_doppelte_id.append(eingabe["id"])
        else:
            alle_id.append(eingabe["id"])
    for doppelte_id in sorted(alle_doppelte_id):
        print(doppelte_id)
        




app = Flask("demos")
#Hamster Test (Berechnung nur Annahme, bitte mit Humor nehmen)
@app.route("/home/", methods=['GET', 'POST'])
def home():
    ausgabe= ""
    hamsterer= ""
    anzahl= ""
    total= ""
    if request.method == 'POST':
        anzahl = int(request.form['wcpapier'])
        total = anzahl * 8
        ausgabe = "Sie haben noch genug für ca. " + str(total) + " Tage."
        if total > int(50):
                hamsterer = "Sie sind ein Hamsterer!"
        else:
            hamsterer = "Bitte nehmen Sie nur so viel wie nötig beim nächsten Einkauf."
        
        
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
    titel=""

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
        titel = "Auftrag erfolgreich eingegeben!"
        ausgabe = "Vielen Dank " + vorname +" "+ name + "! Wir werden uns um Ihr Anliegen schnellst möglich kümmern. Ihr Anliegen '"+ eintrag +"' wird möglichst bis "+tag+ " erledigt. Bei Rückfragen werden wir uns bei Ihnen an " +email+" melden."
        if tag == "heute":
            tag = str(date.today())
        if tag == "morgen":
            tag = str(date.today() + timedelta(1))
        if tag == "übermorgen":
            tag = str(date.today() + timedelta(2))
        if tag == "in einer Woche":
            tag = str(date.today() + timedelta(7))
        if tag == "in zwei Wochen":
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
            "Status": "offen",
            "Helfername": "nicht definiert"
        }

        alle_eingaben.append(eingabe_brauche_hilfe)
        datei_schreiben("text.json",alle_eingaben)
        
    return render_template("brauche_hilfe.html", ausgabe=ausgabe, titel=titel)

@app.route("/biete_hilfe", methods=['GET', 'POST'])
def biete_hilfe():
    if request.method == "POST":
        plz = request.form.get("plz", "")
        suchergebnis = []
        alle_eingaben= datei_öffnen("text.json",[])
        for eingabe in alle_eingaben:
            if eingabe["PLZ"] == plz and eingabe["Status"] == "offen":
                if eingabe["Frist"] == str(date.today()) or eingabe["Frist"] == str(date.today() + timedelta(1,2)):
                    eingabe["Frist"]= f'<a style="color:orange">{eingabe["Frist"]}</a>'
                if eingabe["Frist"] == str(date.today()) or eingabe["Frist"] <= str(date.today() - timedelta(1,2,3,4)):
                    eingabe["Frist"]= f'<a style="color:red">{eingabe["Frist"]}</a>'
                else:
                    eingabe["Frist"]= f'<a style="color:green">{eingabe["Frist"]}</a>'
                suchergebnis.append(eingabe)

        return render_template("biete_hilfe_resultat.html", suchergebnis = suchergebnis)        
    return render_template("biete_hilfe.html")


@app.route("/erledigt/<id>")
def erledigt(id):
    alle_eingaben= datei_öffnen("text.json",[])
    for eingabe in alle_eingaben:
        if eingabe["id"] == id:
                return render_template("erledigt.html", eingabe = eingabe)

   

@app.route("/confirmed/",  methods=['GET', 'POST'])
def confirmed():
    if request.method == "POST":
        helfername = request.form.get("helfername")
        auftrag = request.form.get("auftrag_id")
        suchergebnis = []
        alle_eingaben= datei_öffnen("text.json",[])
        for eingabe in alle_eingaben:
            if eingabe["id"] == auftrag:
                eingabe["Status"] = "geschlossen"
                eingabe["Helfername"] = helfername

                #alle_eingaben.append(eingabe)
        datei_schreiben("text.json",alle_eingaben)
                
        
        return render_template("confirmed.html", helfername=helfername, eingabe=eingabe)
    return render_template("confirmed.html", helfername=helfername, eingabe=eingabe)
                

    

#farbe von frist wird in html manuell überschrieben nach variabel
#Einträge mit Frist heute oder bis übermorgen werden gelb angezeigt
#Einträge mit abgelaufener Frist wird rot angezeigt
#Einträge mit Frist in 3 Tagen und höher werden grün angezeigt
@app.route("/uebersicht")
def uebersicht():
   
    suchergebnis=[]
    suchergebnis_2=[]
    alle_eingaben = datei_öffnen("text.json",[])
    doppelte_einträge(alle_eingaben)
    for eingabe in alle_eingaben:
        if eingabe["Status"] == "offen":
            if eingabe["Frist"] == str(date.today()) or eingabe["Frist"] == str(date.today() + timedelta(1,2)):
                eingabe["Frist"]= f'<a style="color:orange">{eingabe["Frist"]}</a>'
            if eingabe["Frist"] == str(date.today()) or eingabe["Frist"] <= str(date.today() - timedelta(1,2,3,4)):
                eingabe["Frist"]= f'<a style="color:red">{eingabe["Frist"]}</a>'
            else:
                eingabe["Frist"]= f'<a style="color:green">{eingabe["Frist"]}</a>'

            suchergebnis.append(eingabe)
    ###funktion zur sortierung. wichtig suchergebnis muss zugewiesen werden https://www.geeksforgeeks.org/ways-sort-list-dictionaries-values-python-using-lambda-function/
    suchergebnis = sorted(suchergebnis, key = lambda person:
        person['PLZ'])

    for erledigt in alle_eingaben:
        if erledigt["Status"] == "geschlossen":
            suchergebnis_2.append(erledigt)
        
    
    return render_template("uebersicht.html", suchergebnis=suchergebnis, eingabe=eingabe, suchergebnis_2=suchergebnis_2, erledigt=erledigt)

@app.route("/helfer/<id>")
def helfer(id):
    alle_eingaben= datei_öffnen("text.json",[])
    for eingabe in alle_eingaben:
        if eingabe["id"] == id:
            return render_template("helfer.html", eingabe = eingabe)
    return render_template("helfer.html", eingabe = eingabe)


if __name__ == "__main__":
    app.run(debug=True, port=5000)


