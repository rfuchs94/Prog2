from flask import Flask
import plotly.express as px
from flask import render_template
from plotly.offline import plot



app = Flask("demos")

@app.route('/hello/')
def viz():
    data = px.data.gapminder()
    data_ch = data[data.country == 'Switzerland']
    fig = px.bar(data_ch, x='year', y='pop',
             hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
             labels={'pop': 'Einwohner der Schweiz', 'year': 'Jahrzehnt'}, height=400)
    div = plot(fig, output_type="div")
    return render_template('plotly.html', viz_div=div, name="Robin")

        
if __name__ == "__main__":
    app.run(debug=True, port=5000)

