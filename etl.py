import json
from pathlib import Path
from create_tables import sql_connect, DB_PATH

data_path = Path().absolute() / "fh-classes.json"


def load_classes(cur, conn, data):

    insert_classes ="""
        INSERT INTO classes VALUES (
            :CRN,
            :dept,
            :course,
            :section,
            :title,
            :units,
            :start,
            :end,
            :seats,
            :wait_seats,
            :status
            )"""
    for cls in data:
        cur.execute(insert_classes, cls)

    conn.commit()
    print("Inserted rows into table: classes")


def load_instructor_class(cur, conn, data):
    for cls in data:
        crn = cls['CRN']
    
    instructors = set()
    
    for time in cls['times']:
        for name in time['instructor']:
            instructors.add(name)

    for name in instructors:
        cur.execute("INSERT INTO instructor_class VALUES (?, ?)", (name, crn))

    conn.commit()
    print("Inserted rows into table: instructor_class")


def load_meetings(cur, conn, data):
    for cls in data:
        crn = cls['CRN']

    for time in cls['times']:
        days = time.get('days').replace('Th', 'H')  
        cur.execute("INSERT INTO meetings VALUES (null, ?, ?, ?, ?, ?)", (crn, days, time['start_time'], time['end_time'], time['location']))
    
    conn.commit()
    print("Instered rows into table: meetings")


def main():
    cur, conn = sql_connect(DB_PATH)

    with data_path.open() as f:
        data = json.load(f)

    load_classes(cur, conn, data)
    load_instructor_class(cur, conn, data)
    load_meetings(cur, conn, data)

    conn.close()
    

if __name__ == "__main__":
    main()

    """
    cur, conn = sql_connect(DB_PATH)

    # Test load_classes
    cur.execute("SELECT * FROM classes LIMIT 5")
    result = cur.fetchall()
    print(result)

    # Test load_instructor_class
    cur.execute("SELECT * FROM instructor_class LIMIT 5")
    result = cur.fetchall()
    print(result)

    # Test load_meetings
    cur.execute("SELECT * from meetings LIMIT 5")
    result = cur.fetchall()
    print(result)

    conn.close()
    """
