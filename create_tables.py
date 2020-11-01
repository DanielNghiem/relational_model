import sqlite3
from sqlite3 import Error
from pathlib import Path     

DB_PATH = Path().absolute() / "fh-classes.db"


def sql_connect(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        print("Connected to " + str(db_path))

        return cur, conn

    except Error as e:
        print(e)

create_classes ="""
    CREATE TABLE IF NOT EXISTS classes (
        crn integer PRIMARY KEY,
        dept text,
        course text,
        section text,
        title text,
        units real,
        start text,
        end text,
        seats integer,
        wait_seats integer,
        status text
    );"""

create_meetings = """
    CREATE TABLE IF NOT EXISTS meetings (
        id INTEGER PRIMARY KEY,
        crn integer NOT NULL,
        days text,
        start_time text,
        end_time text,
        location text,
        FOREIGN KEY (crn)
            REFERENCES classes (crn)
        )"""

create_instructor_class = """
    CREATE TABLE IF NOT EXISTS instructor_class (
        name text,
        crn integer,
        PRIMARY KEY (name, crn),
        FOREIGN KEY (crn)
            REFERENCES classes (crn)
        )"""

def drop_tables(cur):
    try:
        cur.execute("DROP TABLE IF EXISTS classes")
        cur.execute("DROP TABLE IF EXISTS meetings")
        cur.execute("DROP TABLE IF EXISTS instructor_class")
        print("Dropped existing clases, meetings, and instructor_class tables")
    except Error as e:
        print(e)

def create_tables(cur):
    try:
        cur.execute("PRAGMA foreign_keys = ON") # Enable foreign key constraint
        cur.execute(create_classes)
        cur.execute(create_meetings)
        cur.execute(create_instructor_class)
        print("Created classes, meetings, and instructor_class tables")
    except Error as e:
        print(e)

if __name__ == "__main__":

    cur, conn = sql_connect(DB_PATH)

    # Drop all tables if they exist
    # Then create new tables
    drop_tables(cur)
    create_tables(cur)

    conn.close()
