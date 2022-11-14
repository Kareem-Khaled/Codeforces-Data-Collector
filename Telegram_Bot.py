import requests
import sqlite3            
import random            

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

botKey = '5033647825:AAE97qk1v9GPVm4salO72UbPN5G_1kv1Oa8'
testId = '-1001369877872'
trainingId = '-709113185'

paidG = '-1001729010493'
G = '-1001757014913'
paidB = '-1001607419329'
B = '-1001775122981'

# Get all contestants to get their aceepted soultions
get = "select * from contestants"
contestants = cursor.execute(get).fetchall()
# special = []

def History():
    # get = "select * from history"
    # history = cursor.execute(get).fetchall()
    lst = []
    # speclst = []
    msg = "AC PROBLEMS FOR THE LAST DAYS 🙄\n=========================\n"
    # specMsg = "It's filtration time 🙃"
    for contestant in contestants: # itreate over contestants
            query = f"select Pname from history where handle = '{contestant[0]}'"
            problems = cursor.execute(query).fetchall()
            Pnum = len(problems)
            # msg += f"{contestant[0]} --> {Pnum}\n------------------\n"
            # if contestant[0] not in special:
            lst.append((-Pnum, contestant[0]))
            # else:
                # speclst.append((-Pnum, contestant[0]))
    lst.sort()
    # speclst.sort()
    # # lst.reverse()
    row = 1
    for i in lst:
         msg += f"{row} - {i[1]} --> {abs(i[0])}\n------------------\n"
         row += 1
    # row = 1
    # for i in speclst:
    #      specMsg += f"{row} - {i[1]} --> {abs(i[0])}\n------------------\n"
    #      row += 1
    # msg2 = "or last 2 years 😂"
    # print(msg)
    # print(specMsg)
    # verify=False
    # print(msg)
    #url = f"https://api.telegram.org/bot{botKey}/sendMessage?chat_id={paidG}&text={specMsg}"
    #requests.get(url)
    url = f"https://api.telegram.org/bot{botKey}/sendMessage?chat_id={G}&text={msg}"
    requests.get(url)
    # url = f"https://api.telegram.org/bot{botKey}/sendMessage?chat_id={paidB}&text={msg}"
    # requests.get(url)
    url = f"https://api.telegram.org/bot{botKey}/sendMessage?chat_id={B}&text={msg}"
    requests.get(url)
    # url = f"https://api.telegram.org/bot{botKey}/sendMessage?chat_id={testId}&text={msg}"
    # requests.get(url)
    # url = f"https://api.telegram.org/bot{botKey}/sendMessage?chat_id={testId}&text={msg2}"
    # requests.get(url)
    
    # url = f"https://api.telegram.org/bot{botKey}/sendMessage?chat_id={G}&text={msg2}"
    # requests.get(url)
    # url = f"https://api.telegram.org/bot{botKey}/sendMessage?chat_id={B}&text={msg2}"
    # requests.get(url)

    # for his in history:
    #     # msg = f'Congratulation :)\n "{his[0]}"\n for solving: \n{his[1]} problem ^^'
    #     url = f"https://api.telegram.org/bot{botKey}/sendMessage?chat_id={testId}&text={msg}"
    #     requests.get(url)

    delete = "delete from history"
    cursor.execute(delete)
    conn.commit()

support = [
'⭐️ <handle>\nعاااااااااش بجد 💪\nاول حد يحل\n[<problem>]',
'⭐️ <handle>\nاحلي Accepted دي ولا اييييه 😍\nsolved\n[<problem>]',
'⭐️ <handle>\nالله الله الله 🙈❤️\nايه ال AC الجامدة دي\n[<problem>]',
'Our Hero 🥰\n⭐️ <handle> \njust solved\n[<problem>] ',
'Our Hero for today 🥰 is \n⭐️ <handle> ⭐️\n KeepGoingggggggg ❤️❤️']

def Standing():
    data = []
    get = "select * from contestants"
    contestants = cursor.execute(get).fetchall()
    for contestant in contestants: # itreate over contestants
        get = "select Pname from history where handle = ?"
        problems = cursor.execute(get, (contestant[0], )).fetchall()
        data.append((len(problems), contestant[0]))
    msg = "-------- Today Final Standing 😎 --------\n---------------------------------------\n"
    data.sort(reverse = True)
    msg2 = "Our heroes who need to put in a little effort to finish this sheet\n------------------------\n"
    msg3 = "Our heroes who finished the first sheet 🥳\n------------------------\n"
    for idx in range(len(data)):
        msg += f'{idx + 1} - {data[idx][1]}\nsolved : {data[idx][0]}\n---------------------\n'
    #     if data[idx][0] > 25:
    #         msg3 += f"⭐️ {data[idx][1]} ⭐️\n"
    #     elif data[idx][0] > 14:
    #         msg2 += f"⭐️ {data[idx][1]} ⭐️\n"
    # msg2 += "------------------------\n Put in a little extra effort 💪💪"
    # msg3 += "------------------------\n i hope you will be always Amazing like that 🥰😘"
    url = f"https://api.telegram.org/bot{botKey}/sendMessage?chat_id={testId}&text={msg}"
    requests.get(url)
   

def notification():
    get = "select * from history"
    history = cursor.execute(get).fetchall()
    for idx in range(len(history)):
        msg = support[idx % len(support)] 
        msg = msg.replace('<handle>', history[idx][0]).replace('<problem>', history[idx][1])
        url = f"https://api.telegram.org/bot{botKey}/sendMessage?chat_id={testId}&text={msg}"
        requests.get(url)
        
    # delete = "delete from history"
    # cursor.execute(delete)
    # conn.commit()

#Standing()
#groups = f"https://api.telegram.org/bot{botKey}/getUpdates"
#req = requests.get(groups)
#print(req.text)
#notification()

def send_test(chat):
        msg = "It's filtration time 🙃"
        url = f"https://api.telegram.org/bot{botKey}/sendMessage?chat_id={chat}&text={msg}"
        requests.get(url)

if __name__ == '__main__':
    # fi = open('special.txt', 'r')
    # for line in fi:
    #     special.append(line.rstrip())
    History() 
    # send_test(B)
    # send_test(G)
    # print(requests.get(f'https://api.telegram.org/bot{botKey}/getUpdates').content)