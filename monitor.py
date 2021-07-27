import requests, bs4, html5lib

up = "ags-ServerStatus-content-responses-response-server-status--up"
down = "ags-ServerStatus-content-responses-response-server-status--down"

r = requests.get("https://www.newworld.com/it-it/support/server-status")
soup = bs4.BeautifulSoup(r.text, 'html5lib')

res = soup.findAll("div", {"class": 'ags-ServerStatus-content-responses-response-server'})
servers = dict()

for server in res:
    name = server.find("div", {"class": "ags-ServerStatus-content-responses-response-server-name"}).text.replace(" ", "").replace("\n", "").lower()
    data = server.find("div", {"class": "ags-ServerStatus-content-responses-response-server-status"})
    if down in data["class"]:
        servers[name] = "down"

    elif up in data["class"]:
        servers[name] = "up"

print(servers)
