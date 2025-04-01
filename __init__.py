from flask import Flask, render_template, jsonify
import json
from datetime import datetime, timedelta
from urllib.request import urlopen

app = Flask(__name__)

GITHUB_API_URL = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"  # URL de l'API GitHub

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


@app.route('/commits-data/')
def get_commits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    commits = response.json()

    commits_by_minute = {}

    for commit in commits:
        commit_date = commit['commit']['author']['date']  # Format: "2024-02-11T11:57:27Z"
        minute = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ').minute

        if minute in commits_by_minute:
            commits_by_minute[minute] += 1
        else:
            commits_by_minute[minute] = 1

    return jsonify(commits_by_minute)



if __name__ == "__main__":
    app.run(debug=True)
