# Minecraft Status Bot
Der Minecraft Status Bot ist ein Discord Bot, der den Status des Minecraft Server über ein Online API abfragt und in einem Discord Kanal als Nachricht anzeigt.
**Aktuell ist der Bot nur für Minecraft-Java Server auf port 25565 kompatibel!**

## Einrichtung
Benötigte Software:
<ul>
<li>python3</li>
<li>python3-pip</li>
</ul>

1. Installation der pip-Packete:<br>
```
pip install -r requirements.txt
```
oder
```
pip install nextcord==2.1.0 aiohttp==3.8.1
```

2. Erstelle einen Bot und lade ihn auf deinen Server ein:<br>
[Anleitung: Discord Bot erstellen und einladen](https://youtu.be/zrNloK9b1ro?t=37)

3. Trage nun deine Daten in die `config.json` ein:<br>
`status_channel` - ID des Text-Kanals in dem der Status angezeigt werden soll [Anleitung: Kanal-ID kopieren](https://youtu.be/C3XSildxVi0)<br>
`token` - der Token deines Discord Bots<br>
`address` - die Adresse deines Minecraft Servers<br>
`maintenance_keyword` - Ein Wort, das in der Motd des Servers enthalten ist, wenn der Wartungsmodus aktiviert ist<br>

4. Starte den Bot:<br>
Beim ersten Start des Bots treten Fehler auf!

## Befehle
| Befehl  | Beschreibung |
| --- | --- |
| /reload_config | läd die `config.json` neu und aktualisiert die Status-Nachricht |

# Bilder
<p align="center">
<img src="https://github.com/jonnytutorials/minecraft-status-discord/blob/main/images/online.png" alt="status-online">
<img src="https://github.com/jonnytutorials/minecraft-status-discord/blob/main/images/maintenance.png" alt="status-maintenance">
<img src="https://github.com/jonnytutorials/minecraft-status-discord/blob/main/images/offline.png" alt="status-offline">
</p>

### Fehler kannst du [hier](https://github.com/jonnytutorials/minecraft-status-discord/issues/new) melden. Für Verbesserungsvorschläge steht mein [Discord Server](https://discord.gg/s9tD46Fwh8) zur Verfügung.