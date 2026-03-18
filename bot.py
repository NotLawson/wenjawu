# wenjawu :)
import discord
from discord.ext import commands
import random

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
        "deepfried via reid (the airfryer) by wenjawu",
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
            raise BlacklistUserAlreadyExists
        with open(self.filepath, "a") as file:
            file.write(str(user.id) + "\n")
            

    def remove(self, user: discord.User):
        self.read()
        if str(user.id) not in self.list:
            raise BlacklistUserDoesNotExist
        i = self.list.index(str(user.id))
        with open(self.filepath, "w") as file:
            for index, line in enumerate(self.list):
                if index != (i):
                    file.write(line + "\n")

    def read(self):
        with open(self.filepath, "r") as file:
            self.list = []
            for line in file.readlines():
                self.list.append(line.strip("\n"))
        
    def listed(self, user: discord.User):
        self.read()
        if str(user.id) in self.list:
            return True
        return False
    
def remove_tracker(message):
    words = message.content.split(" ")
    link = ""
    for word in words:
        if "https://open.spotify.com" in word:
            link = word.split("?")[0]
            return link

class Wenjawu(commands.Bot):
    def __init__(self, config={}, **kwargs):
        self.config = config
        
        super().__init__(**kwargs, command_prefix="|", activity=discord.activity.Game(
            name="the game of life"
        ))

    async def on_ready(self):
        print("Logged on as ", self.user)
        await self.tree.sync()
        self.blacklist = Blacklist()

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return # stop execution
        
        if self.blacklist.listed(message.author) == True:
            return # stop execution
        
        if message.content == "type":
            await message.reply("shit\n-# " + random_attribution_comment())

        if "https://open.spotify.com" in message.content:
            await message.reply("tracker removed: " + remove_tracker(message) + "\n-# " + random_attribution_comment())


intents = discord.Intents.default()
intents.message_content = True
intents

with open("config.json", "r") as file:
    import json
    config = json.load(file)

client = Wenjawu(intents=intents, config=config)
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

client.run(config.get("token"))