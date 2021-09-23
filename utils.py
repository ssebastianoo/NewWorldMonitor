import bs4, html5lib, config

class Monitor:
    def __init__(self, session):
        self.session = session
        self.statuses = {
            "up": "ags-ServerStatus-content-responses-response-server-status--up",
            "down": "ags-ServerStatus-content-responses-response-server-status--down",
            "full": "ags-ServerStatus-content-responses-response-server-status--full",
            "maintenance": "ags-ServerStatus-content-responses-response-server-status--maintenance"
        }

    async def get_server_status(self, server):
        r = await self.session.get("https://www.newworld.com/it-it/support/server-status")
        soup = bs4.BeautifulSoup(await r.text(), 'html5lib')

        res = soup.findAll("div", {"class": 'ags-ServerStatus-content-responses-response-server'})
        data = [r for r in res if r.find("div", {"class": "ags-ServerStatus-content-responses-response-server-name"}).text.replace("\n", "").strip().lower() == server.lower()]

        if len(data) == 0:
            raise KeyError('server not found')

        else:
            classes = data[0].find("div", {"class": "ags-ServerStatus-content-responses-response-server-status"})["class"]

            for s in self.statuses:
                if self.statuses[s] in classes:
                    status = s
                    break

            return {"name": data[0].find("div", {"class": "ags-ServerStatus-content-responses-response-server-name"}).text.replace("\n", "").strip(), "status": status}

    async def get_servers_status(self):
        r = await self.session.get("https://www.newworld.com/it-it/support/server-status")
        soup = bs4.BeautifulSoup(await r.text(), 'html5lib')

        res = soup.findAll("div", {"class": 'ags-ServerStatus-content-responses-response-server'})

        servers = dict()

        for server in res:
            name = server.find("div", {"class": "ags-ServerStatus-content-responses-response-server-name"}).text.replace("\n", "").strip()
            data = server.find("div", {"class": "ags-ServerStatus-content-responses-response-server-status"})
           
            for s in self.statuses:
                if self.statuses[s] in data["class"]:
                    servers[name] = s
                    break

        return servers

class DataBase:
    def __init__(self, connection):
        self.db = connection

    async def check(self):
        await self.db.execute("CREATE TABLE IF NOT EXISTS messages (server text, message id, channel id, guild id)")
        await self.db.execute("CREATE TABLE IF NOT EXISTS servers (server text, status text)")
        await self.db.execute("CREATE TABLE IF NOT EXISTS language (guild id, language text)")
        await self.db.commit()

    async def get_status(self, server):
        data = await (await self.db.execute("SELECT status FROM servers WHERE server=?", (server.lower(),))).fetchone()
        return data[0] if data else None

    async def update_server(self, server, status):
        data = await (await self.db.execute("SELECT status FROM servers WHERE server=?", (server.lower(),))).fetchone()
        if not data:
            await self.db.execute("INSERT INTO servers (server, status) VALUES (?, ?)", (server.lower(), status.lower()))
        else:
            await self.db.execute("UPDATE servers SET status=? WHERE server=?", (status.lower(), server.lower()))
        await self.db.commit()

    async def get_messages(self, server):
        data = await (await self.db.execute("SELECT message, channel FROM messages WHERE server=?", (server.lower(),))).fetchall()
        if len(data) == 0:
            return None
        else:
            return [{'message': d[0], 'channel': d[1]} for d in data]

    async def update_message(self, server, message, channel, guild):
        data = await (await self.db.execute("SELECT message FROM messages WHERE server=?", (server.lower(),))).fetchone()
        if not data:
            await self.db.execute("INSERT INTO messages (server, message, channel, guild) VALUES (?, ?, ?, ?)", (server.lower(), message, channel, guild))
        else:
            await self.db.execute("UPDATE messages SET message=?, channel=?, guild=? WHERE server=?", (message, channel, guild, server.lower()))
        await self.db.commit()

    async def remove_log(self, server, guild):
        await self.db.execute("DELETE FROM messages WHERE server=? AND guild=?", (server.lower(), guild))
        await self.db.commit()

    async def get_log(self, server, guild):
        data = await (await self.db.execute("SELECT message, channel FROM messages WHERE server=? AND guild=?", (server.lower(), guild,))).fetchone()
        if not data:
            return None
        else:
            return {'message': data[0], 'channel': data[1]}

    async def get_logs(self, guild):
        data = await (await self.db.execute("SELECT channel, server FROM messages WHERE guild=?", (guild,))).fetchall()
        if len(data) == 0:
            return None
        else:
            logs = dict()
            for d in data:
                if logs.get(d[0]):
                    logs[d[0]].append(d[1])
                else:
                    logs[d[0]] = [d[1]]
            return logs

    async def update_language(self, guild, language):
        data = await (await self.db.execute("SELECT language FROM language WHERE guild=?", (guild,))).fetchone()
        if not data:
            await self.db.execute("INSERT INTO language (guild, language) VALUES (?, ?)", (guild, language.lower()))
        else:
            await self.db.execute("UPDATE language SET language=? WHERE guild=?", (language.lower(), guild))
        await self.db.commit()

    async def get_language(self, guild):
        if not guild:
            return config.languages['english']
        data = await (await self.db.execute("SELECT language FROM language WHERE guild=?", (guild.id,))).fetchone()
        return config.languages[data[0]] if data else config.languages['english']
