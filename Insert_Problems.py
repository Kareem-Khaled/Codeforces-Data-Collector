import sqlite3
import os            
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions

#To get browser dir and hide it
options = ChromeOptions()
options.headless = True
driver = Chrome(executable_path = f'{os.getcwd()}\chromedriver', options = options)

#To connect to DB
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

#To get sheets links
get = "select * from sheets"
sheets = cursor.execute(get).fetchall()

#To insert problem data
insert = "insert or ignore into problems (name, link) values(?,?)"

sheetNum = 0
for sheet in sheets:
    #go to the page and get the source
    driver.get(*sheet)
    src = driver.page_source

    #clean the source and get the problems table
    soup = BeautifulSoup(src, 'lxml')
    table = soup.find('table',class_ = "problems").find_all('td')

    #insert problem(name, link) into DB
    idx = 1
    while idx < len(table):
        char = table[idx - 1].text.strip()
        problem = table[idx].a
        name = f"{char} - {problem.text}"
        link = f"https://codeforces.com{problem['href']}"
        cursor.execute(insert, (name, link,))
        idx += 4
    conn.commit()
    sheetNum += 1
    print(f"- Sheet ({sheetNum}) has been successfully added.\n")
print("Done :)\n========")