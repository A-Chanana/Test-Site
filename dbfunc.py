import psycopg2
from psycopg2 import OperationalError

####
# Projects
####
def db_get_projects():
    connection = create_db_connection()
    cur = connection.cursor()
    instantiate_projects_table(cur)

    cur.execute("SELECT * FROM projects;")
    rows = cur.fetchall()

    connection.commit()
    connection.close()
    cur.close()

    return rows


def db_get_project(project_id):
    connection = create_db_connection()
    cur = connection.cursor()
    instantiate_projects_table(cur)

    cur.execute("SELECT * FROM projects where ID = %s;", (project_id,))
    rows = cur.fetchall()

    connection.commit()
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


def is_db_valid(db_name, user, password, host="localhost", port="5432"):
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host=host,
            port=port
        )
        connection.autocommit = True
        cursor = connection.cursor()

        query = "SELECT 1 FROM pg_database WHERE datname = %s;"
        cursor.execute(query, (db_name,))
        exists = cursor.fetchone() is not None

        cursor.close()
        connection.close()
        return exists

    except OperationalError as e:
        print(f"Connection to PostgreSQL server failed: {e}")
        return False



def create_db_connection():
    return psycopg2.connect(host="localhost", port=5432, dbname="postgres", user="postgres", password=1234)


def instantiate_projects_table(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS projects (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            client VARCHAR(50) NOT NULL
            );""")



####
# Tasks
####
def db_get_tasks(project_id):
    connection = create_db_connection()
    cur = connection.cursor()
    instantiate_tasks_table(cur)

    cur.execute("SELECT * FROM tasks WHERE project_id = %s ORDER BY due_date;", (project_id,))
    rows = cur.fetchall()

    connection.commit()
    connection.close()
    cur.close()

    return rows


def db_get_task(task_id):
    connection = create_db_connection()
    cur = connection.cursor()
    instantiate_tasks_table(cur)

    cur.execute("SELECT * FROM tasks where ID = %s;", (task_id,))
    rows = cur.fetchall()

    connection.commit()
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


def instantiate_tasks_table(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            description TEXT NOT NULL,
            project_id INTEGER NOT NULL,
            due_date DATE NOT NULL,
            completed BOOLEAN DEFAULT FALSE
            );""")