from flask import Flask
from flask import render_template
from flask import request
import json 
from datetime import date, timedelta
import uuid 


#zur Ausführung der Datei müssen alle obige Pakete from flask "" oder import "" geladen sein. 
#Zum Aufrufen der Startseite bitte /home/ verwenden
#hier wird die datei gelesen/geladen, wenn bestehende Daten vorhanden sind.
#ansonsten gilt except 
#tutoring und Quelle Einführung Programmieren Json 

def datei_öffnen(datei, standardwert):
    
    try:
        with open (datei, "r", encoding="utf-8") as json_file:
            daten=json.load(json_file)
            return daten
    except Exception:
            return standardwert

#datei wird geladen und überschrieben/die einträge ergänzt, die Daten werden somit gespeichert
#wenn noch keine Datei vorhanden, wird eine erstellt
#https://kite.com/python/answers/how-to-update-a-json-file-in-python
def datei_schreiben(datei, daten):
    with open (datei, "w", encoding="utf-8") as json_file:
            json.dump(daten,json_file, indent=4)

#es waren aufgrund eines Fehlers im Code bei der Änderung auf "status geschlossen" Einträge mehrfach vorhanden mit der gleichen ID.
#Mit der Funktion wird eine Liste kreiert für alle id's, wenn eine ID mehrmals vorkommt wird sie sortiert und aufgelistet in "doppelte_id".
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


# Formular Eingabe der hilfsbeürftigen Person. Funktion nimmmt die Eingabe per get post Method entgegen.
@app.route("/brauche_hilfe", methods=['GET', 'POST'])
def brauche_hilfe():
    alle_eingaben= datei_öffnen("text.json",[])
    ausgabe=""
    titel=""
#Quelle für Datum Funktion: https://www.programiz.com/python-programming/datetime/current-datetime 
#Datum wird durch date/timedelta umgewandelt
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
        titel = f'<h2 class=text-center style="color:black"> <br/> Auftrag erfolgreich eingegeben!</h2>'
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
            tag = str(date.today() + timedelta(14))
            
#Dictionary wird mit Eingaben des Formulars gefüllt
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
#dictionary wird in json file umgewandelt 
        alle_eingaben.append(eingabe_brauche_hilfe)
        datei_schreiben("text.json",alle_eingaben)
        
    return render_template("brauche_hilfe.html", ausgabe=ausgabe, titel=titel)
#auflistung der offenen einträge aus alle eingaben
#Quelle aus Unterlagen Einführung Programmieren 2
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

#Eingabe soll anhand der ID gefunden werden. Dynamische url 
# https://stackoverflow.com/questions/35107885/how-to-generate-dynamic-urls-in-flask
@app.route("/erledigt/<id>")
def erledigt(id):
    alle_eingaben= datei_öffnen("text.json",[])
    for eingabe in alle_eingaben:
        if eingabe["id"] == id:
                return render_template("erledigt.html", eingabe = eingabe)

   
#Helfende Person trägt Namen ein und bestätigt Eingabe. 
#Eingabe wird gespeichert und Status der Auftrags id auf "geschlossen" angepasst
#Eingabe wird somit nicht mehr angezeigt in der Tabelle "biete_hilfe_resultat.html"
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
    #Sortierung nach Name, falls eine Person, deren geholfen wurde wissen möchte wer ihr geholfen hat - findet sie sich selber schnell in der Liste.
    #Oder als Administrator einfache übersicht welche Tickets erledigt wurden, Frist nicht relevant zur Sortierung
    suchergebnis_2 = sorted(suchergebnis_2, key = lambda person:
        person['Name'])
        
    
    return render_template("uebersicht.html", suchergebnis=suchergebnis, eingabe=eingabe, suchergebnis_2=suchergebnis_2, erledigt=erledigt)

#alle_eingaben wird aufgrund der id nach dem Namen der helfenden Person abgefragt und ausgegeben.
@app.route("/helfer/<id>")
def helfer(id):
    alle_eingaben= datei_öffnen("text.json",[])
    for eingabe in alle_eingaben:
        if eingabe["id"] == id:
            return render_template("helfer.html", eingabe = eingabe)
    return render_template("helfer.html", eingabe = eingabe)


if __name__ == "__main__":
    app.run(debug=True, port=5000)


