# # # # # # # # # # # # # # # # # # #
#            Status Bot             #
#        by Jonny Tutorials         #
#     kontakt@jonnytutorials.de     #
# # # # # # # # # # # # # # # # # # #
import datetime
import json
import os.path
import nextcord
import aiohttp

from nextcord.ext import commands, tasks

def config_loader():
    global settings, old_message
    if os.path.exists("config.json") and os.path.exists("old_msg"):
        try:
            old_message = int(open(file="old_msg", mode="r").read())
            settings = json.loads(open(file="config.json", mode="rb").read())
            print("[✔] Einstellungen (neu) geladen")
        except Exception as e:
            print(f"{e}\n[x] Konfiguration fehlerhaft -- STOPPE --")
            exit("cfg_err")
    else:
        print("[x] Keine Konfigurationsdatei gefunden -- STOPPE --")
        exit("no_cfg")


config_loader()

client = commands.Bot(intents=nextcord.Intents.all())


@client.event
async def on_ready():
    print(f"[i] Eingeloggt als: {client.user}")
    await refresh_status.start()


async def apirq():
    async with aiohttp.ClientSession() as session:
        async with session.get(settings["api"]["java"] + settings["address"]) as java_response:
            if java_response.status in range(200, 299):
                print("[i] Serverdaten abgefragt!")
                return {"success": True, "data": await java_response.json()}


@tasks.loop(minutes=2)
async def refresh_status():
    server_data = await apirq()

    status_color = None
    status = None
    players_max = None
    players_online = None
    motd = None

    if server_data and server_data.get("success") and server_data.get("data").get("online"):
        if settings["maintenance_keyword"] in server_data['data']['motd']['clean'][0].lower():
            status_color = nextcord.Color.yellow()
            status = ":yellow_circle: Wartung"
            players_max = server_data['data']['players']['max']
            players_online = server_data['data']['players']['online']
            motd = server_data['data']['motd']['clean'][0]
        else:
            status_color = nextcord.Color.green()
            status = ":green_circle: Online"
            players_max = server_data['data']['players']['max']
            players_online = server_data['data']['players']['online']
            motd = server_data['data']['motd']['clean'][0]

    else:
        status_color = nextcord.Color.red()
        status = ":red_circle: Offline"
        players_max = "-"
        players_online = "-"
        motd = "-"
        if not server_data:
            print("[i] Abfrage möglicherweise fehlerhaft!")

    message = None
    embed = nextcord.Embed(title="Minecraft Status", color=status_color, timestamp=datetime.datetime.now())
    embed.add_field(name="Serveradresse", value=settings['address'])
    embed.add_field(name="Status", value=status)
    embed.add_field(name="Spieler", value=f"{players_online} / {players_max}")
    embed.add_field(name="Motd", value=motd)
    try:
        message = client.get_channel(settings["status_channel"]).get_partial_message(old_message)
        await message.edit(embed=embed)
    except:
        print("[i] Die Nachricht wird neu erstellt!")
        try:
            await client.http.delete_message(message_id=old_message, channel_id=settings["status_channel"])
        except Exception as e:
            print(f"{e}\n[x] Die alte Nachricht konnte nicht gelöscht werden!")
        try:
            new_message = await client.get_channel(settings["status_channel"]).send(embed=embed)

            open(file="old_msg", mode="w").write(str(new_message.id))
            config_loader()
        except Exception as e:
            print(f"{e}\n[x] Die Nachricht konnte nicht aktualisiert werden!")


@client.slash_command(name="reload_config", default_member_permissions=nextcord.Permissions(administrator=True))
async def reload_config_cmd(interaction: nextcord.Interaction):
    try:
        config_loader()
        await refresh_status()
        embed = nextcord.Embed(description="Konfiguration und Nachricht wurden erfolgreich neu geladen!",
                               color=nextcord.Color.green())
        embed.set_author(icon_url="https://cdn-icons-png.flaticon.com/512/716/716225.png", name="Erfolg")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except:
        embed = nextcord.Embed(description="Konfiguration und Nachricht konnten nicht neu geladen werden!",
                               color=nextcord.Color.red())
        embed.set_author(icon_url="https://cdn-icons-png.flaticon.com/512/463/463612.png", name="Fehler")
        return await interaction.response.send_message(embed=embed, ephemeral=True)


client.run(settings['token'])
