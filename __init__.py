from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests  
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
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
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

from flask import render_template

@app.route('/commits/')
def show_commits():
    return render_template('commits.html')

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    """ Extrait la minute d'un timestamp GitHub. """
    try:
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.strftime('%H:%M')  # Format HH:MM
        return jsonify({'minutes': minutes})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/commits/')
def get_commits():
    """ Récupère les commits depuis GitHub et compte ceux par minute. """
    try:
        response = requests.get(GITHUB_API_URL)
        if response.status_code != 200:
            return jsonify({"error": "Impossible de récupérer les données"}), 500

        commits = response.json()
        commits_by_minute = {}

        for commit in commits:
            commit_date = commit['commit']['author']['date']

            # Utilisation de la route extract-minutes
            minutes = extract_minutes(commit_date).json['minutes']

            commits_by_minute[minutes] = commits_by_minute.get(minutes, 0) + 1

        return jsonify(commits_by_minute)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
  app.run(debug=True)

