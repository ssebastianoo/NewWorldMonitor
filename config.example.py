import discord

class bot:
    prefix = "m!"
    token = "abc"
    colour = {'up': discord.Colour.green(), 'down': discord.Colour.red(), 'maintenance': discord.Colour.gold(), 'full': discord.Colour.blurple()}
    full_status = {'up': "Online", 'down': "Offline", 'maintenance': "Maintenance", 'full': "Full"}

class emojis:
    success = "✅"
    fail = "❌"
    maintenance = "🔧"
    full = "🌡️"
    loading = "<a:loading:869177307066155078>"
    status = {'up': success, 'down': fail, 'maintenance': maintenance, 'full': full}

av_languages = ["english", "italian", "french", "spanish"]
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
        "logsEmpty": "No logs has been set",
        "invite": "Invite me"
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
        "logsEmpty": "Non è stato impostato nessun log",
        "invite": "Invitami"
    },
    "spanish": {
        "checkTitle": "Servidores de New World",
        "slot": "Espacios {slots}",
        "serverNotFound": f"{emojis.fail} Servidor no encontrado",
        "updateAllServers": "Canal para todos los servidores actualizados es {channel.mention}",
        "updateServer": "Canal para el servidor  **{server['name']}** actualizado en el canal  {channel.mention}",
        "removeAllLogs": "Registros eliminados para todos los servidores",
        "removeLogs": "Registros del servidor  **{server['name']}** eliminados",
        "invalidLanguage": "No es un lenguaje válido, lenguajes disponibles {' '.join(config.av_languages)}",
        "languageUpdate": "Lenguaje actualizado a {language_name}",
        "logsEmpty": "Ningún registro configurado",
        "invite": "Invitame"
    },
    "french": {
        "checkTitle": "Serveurs du New World",
        "slot": "Slot {slots}",
        "serverNotFound": f"{emojis.fail} Serveur non trouvé",
        "updateAllServers": "Canal pour tous les serveurs mis à jour à {channel.mention}",
        "updateServer": "Canal du serveur **{server['name']}** actualisé à {channel.mention}",
        "removeAllLogs": "Suppression des journaux pour tous les serveurs",
        "removeLogs": "Suppression des journaux du serveur **{server['name']}**",
        "invalidLanguage": "Langue non valide, choisissez entre {' '.join(config.av_languages)}",
        "languageUpdate": "Langue mise à jour {language_name}",
        "logsEmpty": "Aucun journal n'a été défini",
        "invite": "Invitez-moi"
    }
}