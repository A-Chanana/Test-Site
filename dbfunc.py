import psycopg2
from psycopg2 import OperationalError


def db_get_projects():
    connection = psycopg2.connect(host="localhost", port=5432, dbname="postgres", user="postgres", password=1234)
    cur = connection.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS project (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        client VARCHAR(50) NOT NULL
        );""")

    cur.execute("SELECT * FROM project;")
    rows = cur.fetchall()

    connection.commit()
    connection.close()
    cur.close()

    return rows


def db_save_project(name, client):
    connection = psycopg2.connect(host="localhost", port=5432, dbname="postgres", user="postgres", password=1234)
    cur = connection.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS project (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        client VARCHAR(50) NOT NULL
        );""")

    cur.execute("INSERT INTO project (name, client) VALUES (%s, %s)", (name, client))

    connection.commit()
    connection.close()
    cur.close()


def db_test():
    connection = psycopg2.connect(host="localhost", port=5432, dbname="postgres", user="postgres", password=1234)
    cur = connection.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS project (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        client VARCHAR(50) NOT NULL
        );""")

    cur.execute("INSERT INTO project (name, client) VALUES (%s, %s)", ("Test Project", "Test Client"))

    cur.execute("SELECT * FROM project;")
    rows = cur.fetchall()

    connection.commit()
    connection.close()
    cur.close()

    print(rows)


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

db_test()