import dbfunc
from flask import Flask, render_template, request
import random

app = Flask(__name__, template_folder='static/templates')

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api/projects', methods=['GET', 'POST'])
def projects():

    if request.method == 'POST':
        name = request.form.get('ProjectName')
        client = request.form.get('ProjectClient')

        if not name.strip() and not client.strip():
            return "Error: Invalid input.", 400
        else:
            dbfunc.db_save_project(name, client)

    return render_template("projects.html", projects=dbfunc.db_get_projects())

app.run(debug=True)