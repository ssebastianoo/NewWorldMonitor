class bot:
    prefix = "m!"
    token = "ODY4NjAwNDgwNTE3OTkyNDkw.YPyBPA.tJ1hc9BZqmUDZWTTUpXRi9hqDDQ"

class emojis:
    success = "✅"
    fail = "❌"
    loading = "<a:loading:869177307066155078>"

av_languages = ["english", "italian"]
languages = {
    "english": {
        "checkTitle": "New World Servers",
        "slot": "Slot {slots}",
        "serverNotFound": f"{emojis.fail} Server not found",
        "updateAllServers": "Channel for all servers updated to {channel.mention}",
        "updateServer": "Channel for server **{server['name']}** updated to {channel.mention}",
        "removeAllLogs": "Removed logs for all servers",
        "removeLogs": "Logs for server **{server['name']}** removed",
        "invalidLanguage": "That's not a valid language, choose from {' '.join(config.av_languages)}",
        "languageUpdate": "Language updated to {language_name}",
        "logsEmpty": "No logs has been set"
    },
    "italian": {
        "checkTitle": "Server di New World",
        "slot": "Casella {slots}",
        "serverNotFound": f"{emojis.fail} Server non trovato",
        "updateAllServers": "Canale per tutti i server aggiornato a {channel.mention}",
        "updateServer": "Canale per il server **{server['name']}** aggiornato a {channel.mention}",
        "removeAllLogs": "Rimossi i log per tutti i server",
        "removeLogs": "Rimossi i log per il server **{server['name']}**",
        "invalidLanguage": "Lingua non valida, scegli tra {' '.join(config.av_languages)}",
        "languageUpdate": "Lingua aggiornata a {language_name}",
        "logsEmpty": "Non è stato impostato nessun log"
    }
}
