# wenjawu :)
import discord
from discord.ext import commands
import random
import logging

LOGGER = logging.getLogger()

def random_attribution_comment():
    return random.choice([
        "automated by wenjawu",
        "brought to you by wenjawu"
        "wenjawu wenjawu wenjawu",
        "#wenjawu",
        "helpfully commented by wenjawu",
        "how much wood could a wood chuck chuck if a wood chuck could chuck wood",
        "sponsored by wenjawu",
        "whipped into shape by wenjawu",
        "fried via reid (the airfryer) by wenjawu",
        "<insert joke here> - wenjawu",
        "by your ai overlord, wenjawu",
        "baked on high heat by wenjawu",
        "⇧ ⇩ ⇦ ⇨ ⇧ by wenjawu",
        "spawned into existence by wenjawu",
        "reproduced by wenjawu",
        "matter formed into the concept of a message by wenjawu",
        "3.14159265359 - wenjawu"
    ])

class BlacklistUserDoesNotExist(Exception):
    pass
class BlacklistUserAlreadyExists(Exception):
    pass

class Blacklist:
    def __init__(self, filepath = "blacklist.txt"):
        self.filepath = filepath
        self.read()
    
    def add(self, user: discord.User):
        self.read()
        if str(user.id) in self.list:
            LOGGER.warning(f"User {str(user.id)} already exists on blacklist, but tried to add themself.")
            raise BlacklistUserAlreadyExists
        with open(self.filepath, "a") as file:
            file.write(str(user.id) + "\n")
        LOGGER.info(f"User {str(user.id)} added to the blacklist.")
            

    def remove(self, user: discord.User):
        self.read()
        if str(user.id) not in self.list:
            LOGGER.warning(f"User {str(user.id)} doesn't exist on the blacklist, but tried to remove themself.")
            raise BlacklistUserDoesNotExist
        i = self.list.index(str(user.id))
        with open(self.filepath, "w") as file:
            for index, line in enumerate(self.list):
                if index != (i):
                    file.write(line + "\n")
        LOGGER.info(f"User {str(user.id)} removed from the blacklist.")
    def read(self):
        with open(self.filepath, "r") as file:
            self.list = []
            for line in file.readlines():
                self.list.append(line.strip("\n"))
        
    def listed(self, user: discord.User):
        self.read()
        if str(user.id) in self.list:
            LOGGER.debug(f"User {str(user.id)} is on the blacklist.")
            return True
        LOGGER.debug(f"User {str(user.id)} is not on the blacklist.")
        return False
    
def remove_tracker(message):
    words = message.content.split(" ")
    LOGGER.debug(f"Recived message '{message.content}' to remove tracker from.")
    link = ""
    for word in words:
        for url in config["urls"]:
            if url in word:
                LOGGER.debug(f"Found url {url} in message.")
                link = word.split("?")
                if len(link) < 2:
                    LOGGER.debug("Link already clean.")
                    return # stop execution
                LOGGER.debug("Linked cleaned.")
                return link[0]

class Wenjawu(commands.Bot):
    def __init__(self, config={}, **kwargs):
        self.config = config
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(**kwargs, command_prefix="|", intents=intents, activity=discord.activity.Game(
            name="the game of life"
        ))

    async def on_ready(self):
        LOGGER.info("wenjawu is ready!")
        await self.tree.sync()
        LOGGER.info("Interactions synced.")
        self.blacklist = Blacklist()

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return # stop execution
        
        if self.blacklist.listed(message.author) == True:
            LOGGER.debug(f"Message from black listed user {str(message.author.id)} dropped.")
            return # stop execution
        
        if message.content.lower() == "type":
            LOGGER.debug("type invocation.")
            await message.reply("shit\n-# " + random_attribution_comment())

        if any(url in message.content for url in config["urls"]):
            await message.reply("tracker removed: " + remove_tracker(message) + "\n-# " + random_attribution_comment())

with open("config.json", "r") as file:
    import json
    config = json.load(file)

client = Wenjawu(config=config)
@client.tree.command(name="blacklist", description="Stop wenjawu from responding to your messages.")
async def blacklist_user(interaction: discord.Interaction):
    b = Blacklist()
    try:
        b.add(interaction.user)
        await interaction.response.send_message("Done!", ephemeral=True)
    except BlacklistUserAlreadyExists:
        await interaction.response.send_message("You're already blacklisted :(", ephemeral=True)
@client.tree.command(name="unblacklist", description="Allow wejawu to respond to your messages again!")
async def unblacklist_user(interaction: discord.Interaction):
    b = Blacklist()
    try:
        b.remove(interaction.user)
        await interaction.response.send_message("Done!", ephemeral=True)
    except BlacklistUserDoesNotExist:
        await interaction.response.send_message("You're not on the blacklist :)", ephemeral=True)

@client.tree.command(name="sync", description="Re-sync interactions with this server.")
async def sync_interactions(interaction: discord.Interaction):
    await client.tree.sync(guild=interaction.guild.id)
    LOGGER.info(f"Interactions synced for {interaction.guild.id}")
    await interaction.response.send_message("Done!", ephemeral=True)

if __name__ == "__main__":
    client.run(config.get("token"))