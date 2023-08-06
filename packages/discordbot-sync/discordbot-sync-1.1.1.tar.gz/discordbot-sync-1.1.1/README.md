# Discordbot

This package provides an interface to the RESTful and websocket Discord API so users don't have to worry about rate limits, asyncio, or error handling.

It's as simple as:
```py
import discordbot as discord

bot = discord.Bot("my_api_token")

def on_message(raw_event, message):
	print(message.author, "sent a message in", message.channel, "which said", message.content)
	
	if message.content == "!ping":
		bot.send_message(message.channel, "Pong!")
bot.on_event(discord.event.guild_message_sent, on_message)

bot.run()
```

discordbot also provides a simple way to add commands to your bot
```py
import discordbot as discord

bot = discord.Bot("my_api_token")

role_moderator = '00000000000000' # the id of the role which is required to use the kick command

def cmd_kick(message, member, reason):
    bot.kick(message.guild, member, reason)
    bot.send_message(message.channel, "Member %s kicked. They are allowed to re-join. Ban them if you do not want this behavior." % member, reply_to = message, reply_ping = False)
bot.register_command("kick", "Temporarily remove someone from the server", cmd_kick, required_role = role_moderator, args = [
    {
        "name": "member",
        "description": "The member to kick",
        "type": "user"
    },
    {
        "name": "reason",
        "description": "Reason for kick",
        "type": "string",
        "default": None
    }
])

bot.command_prefix = "!"

bot.register_default_commands() # (optional) adds !cmds and !ping

bot.run()
```

for more examples, please see this [project on github](https://github.com/GabeMillikan/discordbot-sync/tree/main/examples)