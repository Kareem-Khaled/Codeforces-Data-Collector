import sqlite3            
import xlsxwriter
import Sheet_Update

# from Telegram_Bot import *

# Database connection
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Get all Sheets to iterate over its problem
get = "select * from sheets"
sheets = cursor.execute(get).fetchall()

# Get all contestants to get their aceepted soultions
get = "select * from contestants"
contestants = cursor.execute(get).fetchall()

workbook = xlsxwriter.Workbook('K_K - Training.xlsx')
worksheet = workbook.add_worksheet('Standing')
bold = workbook.add_format({'bold': True})

if __name__ == '__main__':
    worksheet.write(0, 0, 'Handle/Sheet')
    worksheet.write(0, 1, 'Total')
    
    row = 0
    col = 1
    for sheet in sheets: # sheets with url
        col += 1
        worksheet.write_url(row, col, sheet[0], string=sheet[1])

    sortedContestants = []
    for contestant in contestants: # to sort contestants by total AC
        cnt = 0
        for sheet in sheets:
            query = f"select Pname from '{sheet[1]}' where handle = '{contestant[0]}'"
            problems = cursor.execute(query).fetchall()
            cnt -= len(problems)
        sortedContestants.append((cnt, contestant[0]))

    sortedContestants.sort()
    row = 0
    for contestant in sortedContestants: # write the contestants and total AC
        row += 1
        worksheet.write_url(row, 0, 'https://codeforces.com/profile/' + contestant[1], string=contestant[1])
        worksheet.write_url(row, 1, str(-contestant[0]))

    row = 1
    col = 2
    for contestant in sortedContestants: # write the number of AC at each sheet
        col = 2
        for sheet in sheets:
            query = f"select Pname from '{sheet[1]}' where handle = '{contestant[1]}'"
            problems = cursor.execute(query).fetchall()
            Pnum = str(len(problems)) + '/' + str(sheet[2])
            worksheet.write(row, col, Pnum)
            col += 1
        row += 1
            
    workbook.close()
    Sheet_Update.update()