import sqlite3            

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

contestants = """CREATE TABLE IF NOT EXISTS "contestants" (
	"handle" TEXT,
	PRIMARY KEY("handle")
);"""

sheets = """CREATE TABLE IF NOT EXISTS "sheets" (
	"link"	TEXT,
	"name"	TEXT,
	"num" INTEGER,
	PRIMARY KEY("link")
);"""

problems = """CREATE TABLE IF NOT EXISTS "problems" (
	"name"	TEXT,
	"link"	TEXT,
	PRIMARY KEY("name")
);"""

solved = """CREATE TABLE IF NOT EXISTS "solved" (
	"handle" TEXT,
	"Pname"	TEXT,
	PRIMARY KEY("handle","Pname"),
	FOREIGN KEY("Pname") REFERENCES "problems"("name"),
	FOREIGN KEY("handle") REFERENCES "contestants"("handle")
);"""

history = """CREATE TABLE IF NOT EXISTS "history" (
	"handle" TEXT,
	"Pname"	TEXT,
	PRIMARY KEY("handle","Pname"),
	FOREIGN KEY("Pname") REFERENCES "problems"("name"),
	FOREIGN KEY("handle") REFERENCES "contestants"("handle")
);"""

wrongs = """CREATE TABLE IF NOT EXISTS "wrongs" (
	"handle" TEXT,
	"Pname"	TEXT,
	"cnt"	INTEGER,
	PRIMARY KEY("handle","Pname"),
	FOREIGN KEY("handle") REFERENCES "contestants"("handle"),
	FOREIGN KEY("Pname") REFERENCES "problems"("name")
);"""

cursor.execute(contestants)
cursor.execute(sheets)
cursor.execute(history)
# cursor.execute(solved)