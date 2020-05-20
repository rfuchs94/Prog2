
**Projektidee
Webapplikation gemeinsam gegen COVID-19**

**Ausgangslage**<br />
Seit dem Ausbruch der Pandemie sind Personen aus der Risikogruppe besonders im Alltag von der Krise betroffen. Alltägliche Dinge wie Einkaufen oder auf der Post etwas abzuholen, kann für sie bereits ein grosses Risiko darstellen. Meine Webapplikation soll die Solidarität in den Regionen fördern und es den betroffenen Personen ermöglichen Hilfe anzufordern. Freiwillige können dann via PLZ prüfen, wer im Dorf/Stadt hilfe braucht und kann sich anschliessend an die Person wenden. 

**Funktion**<br />
Es soll eine zweiseitige Plattform entstehen. Einerseits zur Eingabe der betroffenen Personen, sie können via Formular eintragen bei was, wann und wo sie Hilfe brauchen. Die freiwilligen Helfer können über die Navigation per PLZ die hilfsbedürftigen Personen in ihrer Nähe abrufen und von der Übersicht eine Person auswählen sowie anschliessend kontaktieren.  

**Workflow**<br />
**Dateneingabe**<br />
Hilfsbedürftige Person geht auf "benötige Hilfe" aus dem Startmenü und wählt im Formular aus, wobei sie Hilfe braucht, sowie persönliche Kontaktdaten. Die Person, welche Hilfe anbieten möchte, kann aus dem Startnavigation "möchte helfen" auswählen und gelangt zur Eingabe der lokalen PLZ. Wenn der Auftrag ausgewählt wurde muss der Name der helfenden Person eingegeben und die Hilfe bestätigt werden. Offene Aufträge können auch aus der Übersicht ausgewählt und bearbeitet werden. <br />
**Datenverarbeitung**<br />
Die Anfrage wird als dictionary entgegengenommen und dann in einer Stammdatenbank (json Datei) mit einer Auftrags ID mit dem Status offen gespeichert. Wenn ein Auftrag abgeschlossen wird, wird der Eintrag anhand der ID gefunden und der Status umgeschrieben auf "geschlossen". Der name der helfenden Person wird im json File abgespeichert.<br />
**Datenausgabe**<br />
Möchte helfen: Die Json Datei wird nach der PLZ abefragt und listet alle offenen Aufträge ein. 
Übersicht: Die ganze Datei wird in zwei Tabellen unterteilt offene Aufräge und geschlossene Aufträge. Die offenen Aufträge werden anhand der PLZ sortiert und die Frist in rot, orange oder grün angezeigt aufgund der ausstehenden Deadline (Deadline Vergangenheit, heute/morgen,+2 Tage).
Die geschlossenen Aufträge werden anhand des Namens aufgelistet. So kann die Person ihr Ticket finden und einsehen, wer Ihr geholfen hat.
Der Name der helfenden Person wird bei der Auswahl des geschlossenen Auftrags angezeigt. 

**Ablaufdiagramm**


![Bild](https://github.com/rfuchs94/Prog2/AblaufdiagrammWebapplikation.png)
=======


