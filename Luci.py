import signal
import sys
import asyncio
import aiohttp
import json
import websocket
import threading
import time
import bakup

loop = asyncio.get_event_loop()
client = aiohttp.ClientSession(loop=loop)
got_json = False

async def get_json(client , url):
    async with client.get(url) as response:
        try :
            assert response.status == 200
            global got_json
            got_json = True
            return await response.read()
        except AssertionError:
            ws.send(json.dumps({"cmd" : "chat" , "text" : "Sub doesnt exist"}))

async def get_reddit_top(subreddit , client):
    data1 = await get_json(client , 'https://www.reddit.com/r/' + subreddit + '/top.json?sort=Hot&t=day&limit=3')
    global got_json
    if got_json:
        j = json.loads(data1.decode('utf-8'))
        for i in j['data']['children']:
            score = i['data']['score']
            title = i['data']['title']
            link = i['data']['url']
            output = str(score) + ": " + title + ' (' + link + ')'
            output = json.dumps(output)
            ws.send(json.dumps({"cmd" : "chat" , "text" : output}))
        print('Done: ' , subreddit + '\n')
    else :
        print("User tried to enter an unexisting sub \n")
    got_json = False

def signal_handler(signal , frame):
    loop.stop()
    client.close()
    sys.exit(0)

signal.signal(signal.SIGINT , signal_handler)

def main(sub):
    loop.run_until_complete(get_reddit_top(sub , client))

url = "wss://hack.chat/chat-ws"
ws = websocket.WebSocket()
prefix = '::'
#nick = input("UR NICK\n")
fixed = "Luci"  #to not see ma own msgs
nick = "Luci#jerker"
#trip = input("passwd (enter 100 to not apply)\n")
#if trip != 100 :
#   nick = nick +'#' + trip
channel = input("which channel?\n")

trip_dict ={}
last_msg = ''
last_sender = ''

def saver():
    with open("Db/log.txt" , "r") as file:
        for line in file :
            trip , list_trip = line.split("\t")
            list_trip = json.loads(list_trip)
            trip_dict[trip] = list_trip

def send_msg() :
    txt = input()
    cmd = {'cmd' :"chat" , "text" :txt }
    ws.send(json.dumps(cmd))

def recive():
    dump = json.loads(ws.recv())
    if dump['cmd'] == 'chat':
        if dump['nick'] == fixed :
            with open("Db/text_log.txt" , "a") as log:
                log.write( '<{}>\t{}'.format(nick , dump['text'])+ '\n')
        else:
            if prefix in dump['text'] :
                anaylizor(dump['text'] , dump['nick'])

            global last_sender
            last_sender = dump['nick']
            if 'trip' in dump:
                dump['nick']= dump['trip'] + '##' + dump['nick']
            text = "<" + dump['nick'] + ">" +"\t"+ dump['text']
            global last_msg
            last_msg = dump['text']
            print(text)
            with open("Db/text_log.txt" , "a") as log:
                log.write(text + '\n')

    elif dump['cmd'] == 'info' or recived['cmd'] == 'warn' :
        print(recived)
    elif dump['cmd'] == 'onlineRemove':
        print("%s left "%(dump['nick']))
        with open("Db/text_log.txt" , "a") as log:
            log.write("{} left \n".format(dump['nick']))
        users_list.remove(dump['nick'])
    elif dump['cmd'] == 'onlineAdd':
        print("%s joined "%(dump['nick']))
        with open("Db/text_log.txt" , "a") as log:
            log.write("{} joined ".format(dump['nick']))
        users_list.append(dump['nick'])
        if dump['trip'] not in trip_dict:
            trip_dict[dump['trip']] = [dump['nick']]
        else :
            if dump['nick'] not in trip_dict[dump['trip']]:
                trip_dict[dump['trip']].append([dump['nick']])
                writer()
    elif dump['cmd'] == 'warn':
        pass
    else:
        print(dump)


ws.connect(url) # start of the connection

intro = {"cmd": "join" , "channel": channel  , "nick": nick}
ws.send(json.dumps(intro))
recived = json.loads(ws.recv())

connected = False
try :

    users = recived['users']
    users_list = []
    for user in users :
        users_list.append(user['nick'])
    connected = True
except KeyError:
    print(recived['text'])

saver()

print('Online comrades : ', end="")
if connected :
    for user in users :
        print(user['nick'] , end=',')
    print("\n")

if connected:
    for user in users :
        if user['trip'] != None:
            if user['trip'] not in trip_dict.keys() :
                trip_dict[user['trip']] = [user['nick']]
            else:
                if user['nick'] not in trip_dict[user['trip']]:
                    trip_dict[user['trip']].append([user['nick']])


def writer():
    open
    with open('Db/log.txt' , 'w') as f:
        for trip in trip_dict.keys() :
            f.write(trip + '\t' + json.dumps((trip_dict[trip])) + '\n')

def stay():
    while True:
        ws.send(json.dumps({"cmd":"ping"}))
        time.sleep(40)

def constant():
    while ws.connected :
        recive()

def constant2():
    while ws.connected:
        send_msg()

def quote():
    txt = "```css\n" + "“" + last_msg + "„" + "\n\t\t\t\t\t\t\t\t\t\t\t\t-" + last_sender
    cmd = {'cmd' :"chat" , "text" :txt }
    ws.send(json.dumps(cmd))

def anaylizor(string , user_nick):
    if "coffee" in  string :
        ws.send(json.dumps({"cmd" :"chat" , "text":"/me sips coffee for {}".format(user_nick)}))
    elif "reddit" in string :
        try :
            command , sub = string.split(" ")
        except ValueError:
            try :
                command , sub , sec = string.split(" ")
                sub = sub + sec
            except ValueError:
                ws.send(json.dumps({"cmd" : "chat" , "text" :"enter 1 sub  , not more not less"}))
        main(sub)
    #elif "lyrics" in string:
        #song = string.strip('{}lyrics'.format(prefix))
        #bakup.main_l(song)
        #with open("Db/lyrics.txt" , 'r') as lyrics :
            #for line in lyrics :
                #if not line.isspace():
                    #ws.send(json.dumps({"cmd": "chat" , "text" : '{}'.format(line)}))
                    #time.sleep(5)
    elif "quote" in string :
        quote()

stay = threading.Thread(target = stay)
sendmsg = threading.Thread(target = constant2)
recv = threading.Thread(target = constant)
writer()

sendmsg.start()
recv.start()
stay.start()





