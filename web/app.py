from flask import Flask
from flask import render_template, request
from flask import redirect, url_for
import model


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    flights = model.get_flights()
    fic = model.get_fic()
    return render_template('flights.html', fic=fic, flights=flights)


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        acid = request.form['acid']
        state = request.form['state']
        model.save_flight(acid, state)

    return redirect(url_for('index'))
