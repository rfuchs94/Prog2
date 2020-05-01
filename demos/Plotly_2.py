from flask import Flask
import plotly.express as px
import plotly.graph_objects as go



Wochentage=['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag']
anz_kunden = {'mo':10, 'di':8,'mi':12,'do':15,'fr':20,'sa':60}
anz_stunden = {'mo':5, 'di':4,'mi':6,'do':8,'fr':12,'sa':36}


fig = go.Figure(data=[
    go.Bar(name='Anzahl Kunden', x=Wochentage, y=[anz_kunden['mo'], anz_kunden['di'], anz_kunden['mi'], anz_kunden['do'], anz_kunden['fr'], anz_kunden['sa']]),
    go.Bar(name='Anzahl Arbeitsstunden', x=Wochentage, y=[anz_stunden['mo'], anz_stunden['di'], anz_stunden['mi'], anz_stunden['do'], anz_stunden['fr'], anz_stunden['sa']]),
])


# Change the bar mode
fig.update_layout(barmode='group',
    title="Wöchentlicher Kundentraffic",
    xaxis_title="Wochentage",
    yaxis_title="Anzahl",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    ))
fig.show()



