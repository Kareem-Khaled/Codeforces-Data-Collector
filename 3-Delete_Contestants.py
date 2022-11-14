import sqlite3            

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Get all Sheets to iterate over its problem
get = "select * from sheets"
sheets = cursor.execute(get).fetchall()

contestants = []

if __name__ == '__main__':
    fi = open('Delete_Contestants.txt', 'r')
    for line in fi:
        contestants.append(line.rstrip())

    for sheet in sheets:
        for contestant in contestants: # itreate over contestants
            query = f"delete from '{sheet[1]}' where handle = '{contestant}'"
            query2 = f"delete from contestants where handle = '{contestant}'"
            query3 = f"delete from history where handle = '{contestant}'"
            cursor.execute(query)
            cursor.execute(query2)
            cursor.execute(query2)

    fi.close()
    conn.commit()