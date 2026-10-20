import psycopg2
from datetime import datetime

####
# Projects
####
def db_get_projects():
    connection = create_db_connection()
    cur = connection.cursor()
    instantiate_projects_table(cur)

    cur.execute("SELECT * FROM projects;")
    rows = cur.fetchall()

    connection.close()
    cur.close()

    return rows


def db_get_project(project_id):
    connection = create_db_connection()
    cur = connection.cursor()
    instantiate_projects_table(cur)

    cur.execute("SELECT * FROM projects where ID = %s;", (project_id,))
    rows = cur.fetchall()

    connection.close()
    cur.close()

    return rows


def db_save_project(name, client):
    connection = create_db_connection()
    cur = connection.cursor()
    instantiate_projects_table(cur)

    cur.execute("INSERT INTO projects (name, client) VALUES (%s, %s)", (name, client))

    connection.commit()
    connection.close()
    cur.close()


####
# Tasks
####
def db_get_tasks(project_id):
    connection = create_db_connection()
    cur = connection.cursor()
    instantiate_tasks_table(cur)

    cur.execute("SELECT * FROM tasks WHERE project_id = %s ORDER BY due_date;", (project_id,))
    rows = cur.fetchall()

    connection.close()
    cur.close()

    return rows


def db_get_task(task_id):
    connection = create_db_connection()
    cur = connection.cursor()
    instantiate_tasks_table(cur)

    cur.execute("SELECT * FROM tasks where ID = %s;", (task_id,))
    rows = cur.fetchall()

    connection.close()
    cur.close()

    return rows


def db_save_task(description, project_id, due_date, completed=False):
    connection = create_db_connection()
    cur = connection.cursor()
    instantiate_tasks_table(cur)

    cur.execute("INSERT INTO tasks (description, project_id, due_date, completed) VALUES (%s, %s, %s, %s)", (description, project_id, due_date, completed))

    connection.commit()
    connection.close()
    cur.close()


def update_task_completion(task_id, completed):
    connection = create_db_connection()
    cur = connection.cursor()
    instantiate_tasks_table(cur)

    cur.execute("UPDATE tasks SET completed = %s WHERE id = %s", (completed, task_id))

    connection.commit()
    connection.close()
    cur.close()


def delete_task(task_id):
    connection = create_db_connection()
    cur = connection.cursor()
    instantiate_tasks_table(cur)

    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))

    connection.commit()
    connection.close()
    cur.close()



def db_get_projects_and_tasks():
    connection = create_db_connection()
    cur = connection.cursor()
    instantiate_projects_table(cur)
    instantiate_tasks_table(cur)

    cur.execute("""
        SELECT p.id, p.name, p.client, t.id, t.description, t.due_date, t.completed
        FROM projects p
        LEFT JOIN tasks t ON p.id = t.project_id
        ORDER BY p.id, t.due_date;
    """)
    rows = cur.fetchall()

    connection.close()
    cur.close()

    projects_output = {}
    
    for row in rows:
        #print(row)
        p_id, p_name, p_client, t_id, t_desc, t_due, t_completed = row

        if p_id not in projects_output:
            projects_output[p_id] = {
                "name": p_name,
                "client": p_client,
                "tasks": []
            }

        if t_id is not None:
            task_dict = {
                "id": t_id,
                "description": t_desc,
                "dueDate": str(t_due),
                "completed": t_completed
            }
            projects_output[p_id]["tasks"].append(task_dict)
    
    return projects_output


def is_valid_date(date_string, date_format="%Y-%m-%d"):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except:
        return False



####
# Initialization
####
def instantiate_projects_table(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS projects (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            client VARCHAR(50) NOT NULL
            );""")

def instantiate_tasks_table(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            description TEXT NOT NULL,
            project_id INTEGER NOT NULL,
            due_date DATE NOT NULL,
            completed BOOLEAN DEFAULT FALSE
            );""")


def create_db_connection():
    return psycopg2.connect(host="localhost", port=5432, dbname="postgres", user="postgres", password=1234)