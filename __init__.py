from flask import Flask, render_template, jsonify
import json
from datetime import datetime
from urllib.request import urlopen

app = Flask(__name__)

GITHUB_API_URL = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"  # Ajout de l'URL de l'API GitHub

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route('/commits/')
def show_commits():
    return render_template('commits.html')

@app.route('/api/commits/')
def get_commits():
    """ Récupère les commits depuis GitHub et compte ceux par minute. """
    try:
        # Appel de l'API GitHub
        with urlopen(GITHUB_API_URL) as url:
            commits_data = json.loads(url.read().decode())

        commits_by_minute = {}

        # Parcours des commits et extraction de la minute
        for commit in commits_data:
            commit_date = commit['commit']['author']['date']
            minute = extract_minutes(commit_date)
            
            # Comptage des commits par minute
            commits_by_minute[minute] = commits_by_minute.get(minute, 0) + 1

        return jsonify(commits_by_minute)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def extract_minutes(date_string):
    """ Extrait la minute d'un timestamp GitHub. """
    try:
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        return date_object.strftime('%H:%M')  # Format HH:MM
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
