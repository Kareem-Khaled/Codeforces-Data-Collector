import sqlite3
import requests
from colored import fg
from bs4 import BeautifulSoup

color = {
    "Unrated,": 58,
    "Newbie": 15,
    "Pupil": 47,
    "Specialist": 51,
    "Expert": 33,
    "Candidate": 165,
    "Master": 9,
    "Grandmaster": 9
}

# Database connection
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# To insert accepted solutions
his = "insert or ignore into history (handle, Pname) values(?,?)"

def insertContestant(handle):
    insert = "insert or ignore into contestants (handle) values(?)"
    try:
        cursor.execute(insert, (handle, ))
        conn.commit()
    except Exception as e:
        return f"->>> There is an error while inserting {handle} - {str(e)}"

    return f'{handle} inserted successfully!' 

def insertSheet(link, sheetName, proNum):
    insert = "insert or ignore into sheets (link, name, num) values(?,?,?)"
    try:
        sheet = f"""CREATE TABLE IF NOT EXISTS "{sheetName}" (
                "handle" TEXT,
                "Pname"	TEXT,
                PRIMARY KEY("handle","Pname"),
                FOREIGN KEY("handle") REFERENCES "contestants"("handle"),
                FOREIGN KEY("Pname") REFERENCES "problems"("name")
            );"""
        cursor.execute(sheet)
        cursor.execute(insert, (link, sheetName, proNum, ))
        conn.commit()
    except:
        return f"->>> There is an error while inserting {sheetName} sheet!"

    return f'{sheetName} inserted successfully!'

def readFile(fileName):
    ret = []
    try:
        with open(fileName, 'r') as f:
            for line in f:
                ret.append(line.strip())
    except Exception as e:
            print(fg(9) + str(e))
            exit(0)

    return ret

problems = []

def get_solutions(trs, sheetName, sheetLink):
    ac = f"insert or ignore into '{sheetName}' (handle, Pname) values(?,?)"
    i = (1 if len(problems) else 0)
    while i < len(trs) - 1:
        if i == 0: #problems
            tr = trs[i].find_all('th')
        else: #contestants
            contestants = {}
            team = '' 
            tr = trs[i].find_all('td')

            try:
                isTeam = True
                trA = tr[1].span.find_all('a')
            except: 
                isTeam = False
            
            if isTeam and 'team' in trA[0]['href']: # it's a team
                team = trA[0]['title']
                for k in range(1, len(trA)):
                    tmp = trA[k]['title'].split(' ')
                    contestants[tmp[-1]] = tmp[0]

            else: # it's a contestant
                tmp = tr[1].a['title'].split(' ')
                contestants[tmp[-1]] = tmp[0]

            if len(team):
                print(fg(10) + '\n' + team + ': ', flush=True)

            for name, rate in contestants.items():
                insertContestant(name)
                print(fg(color[rate]) + '-> ' + name, flush=True)

            if len(team): print()

        j = 4
        while j < len(tr): 
            if i == 0:
                txt = tr[j].a['title']
                problems.append(txt)
            else:
                verdict = tr[j].text.strip()
                if '+' in verdict:
                    for contestant in contestants:
                        cursor.execute(ac, (contestant, problems[j - 4],))
                        cursor.execute(his, (contestant, problems[j - 4],))
            j += 1
            
        if i == 0:
            insertSheet(sheetLink, sheetName, len(problems))
            print(fg(11) + '+ ' + sheetName + ': ', flush=True)
            print('------------------------------', flush=True)

        i += 1
    conn.commit()

if __name__ == '__main__':
    try:
        handelsList = readFile('Handels_List.txt')[0]
        sheets = readFile('sheets.txt')
    except:
        print(fg(9) + "->>> Error in reading files")
        exit(0)

    for sheetLink in sheets:
       
        page = 1
        problems = []
        sheetName = ''
        lastStanding = ''
        while True:
            link = f'{sheetLink}/standings/page/{str(page)}?list={handelsList}&showUnofficial=true'
            curPage = requests.get(link)        
            soup = BeautifulSoup(curPage.content, 'lxml')
            sheetName = soup.find('div', class_ = 'contest-name').text.strip()
            standing = soup.find('table', class_ = 'standings')
            if lastStanding == standing: break
            lastStanding = standing
            get_solutions(standing.find_all('tr'), sheetName, sheetLink)
            page += 1

        print(flush=True)

    print(fg(10) + "Done :)", flush=True)