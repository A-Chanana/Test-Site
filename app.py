import dbfunc
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__, template_folder='static/templates')


@app.route('/')
def index():
    return render_template("index.html"), 200



@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'POST':
        name = request.form.get('ProjectName', '')
        client = request.form.get('ProjectClient', '')

        if not name.strip() or not client.strip():
            return "Error: Datos invalidos.", 400
        
        dbfunc.db_save_project(name, client)
        # Can't send 201 on a redirect, this resends the data on refresh, but it is what I was asked to do
        return render_template("projects.html", projects=dbfunc.db_get_projects()[::-1]), 201

    return render_template("projects.html", projects=dbfunc.db_get_projects()[::-1]), 200


@app.route('/api/projects', methods=['GET', 'POST'])
def api_projects():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name', '')
        client = data.get('client', '')

        if not name.strip() or not client.strip():
            return jsonify({"Error": "Datos invalidos."}), 400
        
        dbfunc.db_save_project(name, client)
        return jsonify({"message": "Proyecto creado exitosamente."}), 201
    
    else:
        projects = dbfunc.db_get_projects_and_tasks()
        if projects:
            return jsonify(projects), 200
        else:
            return jsonify({"Error": "No se encontraron proyectos."}), 404



@app.route('/projects/<int:project_id>/tasks', methods=['GET', 'POST'])
def project(project_id):
    id = dbfunc.db_get_project(project_id)
    if not id:
        return "Error: Proyecto no encontrado.", 404
        
    if request.method == 'POST':
        description = request.form.get('TaskDescription', '')
        due_date = request.form.get('TaskDate', '')

        if not description.strip() or not dbfunc.is_valid_date(due_date):
            return "Error: Datos invalidos.", 400

        dbfunc.db_save_task(description, project_id, due_date)
    

    tasks = dbfunc.db_get_tasks(project_id)[::-1]

    return render_template("project.html", project=id[0], tasks=tasks), 200


@app.route('/api/projects/<int:project_id>/tasks', methods=['GET', 'POST'])
def api_project(project_id):
    id = dbfunc.db_get_project(project_id)
    if not id:
        return jsonify({"Error": "Proyecto no encontrado."}), 404
      
    if request.method == 'POST':
        data = request.get_json()
        description = data.get('description', '')
        due_date = data.get('dueDate', '')

        if not description.strip() or not dbfunc.is_valid_date(due_date):
            return jsonify({"Error": "Datos invalidos."}), 400

        dbfunc.db_save_task(description, project_id, due_date)
        return jsonify({"message": "Tarea creada exitosamente."}), 201
    
    else:
        return jsonify({"Error": "Metodo invalido."}), 400



@app.route('/tasks/<int:task_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def task(task_id):
    id = dbfunc.db_get_task(task_id)
    if not id:
        return "Error: Tarea no encontrada.", 404
    
    if request.method == 'POST':
        request.method = request.form.get('_method', request.method)
    
    if request.method == 'PUT':
        completion = request.form.get('TaskCompletion', '') == 'True'
        dbfunc.update_task_completion(task_id, completion)
        id = dbfunc.db_get_task(task_id)
    
    if request.method == 'DELETE':
        dbfunc.delete_task(task_id)
        return render_template("index.html"), 200

    return render_template("task.html", task=id[0]), 200


@app.route('/api/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def api_task(task_id):
    id = dbfunc.db_get_task(task_id)
    if not id:
        return jsonify({"Error": "Tarea no encontrada."}), 404

    if request.method == 'PUT':
        data = request.get_json()
        completion = data.get('completed', False)
        dbfunc.update_task_completion(task_id, completion)
        return jsonify({"message": "Tarea actualizada exitosamente."}), 200
    
    if request.method == 'DELETE':
        dbfunc.delete_task(task_id)
        return jsonify({"message": "Tarea eliminada exitosamente."}), 200

app.run(host='0.0.0.0', port=5000, debug=True)