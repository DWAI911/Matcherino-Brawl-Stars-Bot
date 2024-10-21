# Importing necessary Libraries
import discord
import os
import re
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta

# Load dot env file and get private keys
load_dotenv()
TOKEN = os.getenv('TOKEN')
LOG_CHANNEL_ID = os.getenv('LOG_CHANNEL_ID')
LOG_CHANNEL_ID = int(LOG_CHANNEL_ID)
BYPASS_ROLE_ID = os.getenv('BYPASS_ROLE_ID')
BYPASS_ROLE_ID = int(BYPASS_ROLE_ID)
ORGANIZER_ROLE = os.getenv('ORGANIZER_ROLE')
ORGANIZER_ROLE = int(ORGANIZER_ROLE)
BANNED_WORDS = os.getenv('BANNED_WORDS').split(',')
SECRET_COMMAND = "/postrules"
SELF_ROLE_COMMAND = "/selfrole"
REGION_MESSAGE_ID = os.getenv('REGION_MESSAGE_ID')
REGION_MESSAGE_ID = int(REGION_MESSAGE_ID)
ROLE_MESSAGE_ID = os.getenv('ROLE_MESSAGE_ID')
ROLE_MESSAGE_ID = int(ROLE_MESSAGE_ID)
message_counter = 0
pin_message_threshold = 100
last_pin_time = datetime.now() - timedelta(minutes=10)
emoji_to_region_role = {
    '🇺🇸': 'NA',
    '🇧🇷': 'LATAM',
    '🇯🇵': 'APAC',
    '🇪🇺': 'EMEA'
}
emoji_to_role = {
    '🎯': 'Organizer',
    '🎮': 'Player'
}

from keep_alive import keep_alive
keep_alive()

# Constants for the pin command
pin_text_title = "Exclusive Matcherino Pins Available in Brawl Stars"
pin_text_description = """
Currently, there are two exclusive pins available through Matcherino for the game Brawl Stars. These pins can be earned in two ways:

1. **Donation Pin**: Contribute $5 or more to a tournament. The tournament must be classified as a bronze tier or higher. By supporting the event with a donation, you'll receive this special pin as a reward for your contribution.

2. **Winning Pin**: Earn this pin by placing 1st in a silver-tier tournament or by finishing 2nd place or higher in a gold-tier tournament.

**Note**: Pins may take up to 14 business days to arrive directly in your in-game inbox. Tournament tiers are dependent on the actual tier of the tournament, not the total Cash Prize. A tournament with the winners pin will show up on the tournament page like below.
"""

# Regular expression pattern for detecting links
link_pattern = r'(https?://\S+|www\.\S+|\S+\.(com|net|org|gov|edu|ca|uk|io))'

# Create a new Discord client
class Client (discord.Client):
    # When the bot is ready, print a message to the console
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.change_presence(activity=discord.Game(name="Brawl Stars"))
        for guild in self.guilds:
            print(f"Connected to guild: {guild.name}")
            log_channel = self.get_channel(LOG_CHANNEL_ID)
            if log_channel is None:
                print(f"Log channel with ID {LOG_CHANNEL_ID} not found.")
            else:
                print(f"Log channel {log_channel.name} is ready.")

    async def on_raw_reaction_add(self, payload):
        guild = self.get_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        if payload.message_id == REGION_MESSAGE_ID:
            role_name = emoji_to_region_role.get(str(payload.emoji))
            if role_name:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    await member.add_roles(role)
                    print(f"Added {role_name} role to {member.name}.")
        elif payload.message_id == ROLE_MESSAGE_ID:
            role_name = emoji_to_role.get(str(payload.emoji))
            if role_name:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    await member.add_roles(role)
                    print(f"Added {role_name} role to {member.name}.")

    async def on_raw_reaction_remove(self, payload):
        guild = self.get_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)

        if payload.message_id == REGION_MESSAGE_ID:
            role_name = emoji_to_region_role.get(str(payload.emoji))
            if role_name:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    await member.remove_roles(role)
                    print(f"Removed {role_name} role from {member.name}.")

        elif payload.message_id == ROLE_MESSAGE_ID:
            role_name = emoji_to_role.get(str(payload.emoji))
            if role_name:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    await member.remove_roles(role)
                    print(f"Removed {role_name} role from {member.name}.")

    # When a message is sent, check for banned words and links as well as keyword "pin"
    async def on_message(self, message):
        global message_counter
        global last_pin_time
        if message.author == self.user:
            return
        message_counter += 1

        if any(word in message.content.lower() for word in BANNED_WORDS):
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, your message was removed for using inappropriate language. Further use will result in a ban.")
                log_channel = self.get_channel(LOG_CHANNEL_ID)
                if log_channel is not None:
                    await log_channel.send(f"Deleted message from {message.author} for profanity: {message.content}")
            except discord.Forbidden:
                print(f"Could not delete message from {message.author}. Check bot permissions.")
            except discord.HTTPException as e:
                print(f"Failed to delete message due to an error: {e}")

        # Check if the message author has the bypass role
        bypass_role = discord.utils.get(message.author.roles, id=BYPASS_ROLE_ID)
        organizer_role = discord.utils.get(message.author.roles, id=ORGANIZER_ROLE)

        if not bypass_role and not organizer_role and re.search(link_pattern, message.content, re.IGNORECASE):
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, links are not allowed in this server.")
                log_channel = self.get_channel(LOG_CHANNEL_ID)
                if log_channel is not None:
                    await log_channel.send(f"Deleted message from {message.author} for containing a link: {message.content}")
            except discord.Forbidden:
                print(f"Could not delete message from {message.author}. Check bot permissions.")
            except discord.HTTPException as e:
                print(f"Failed to delete message due to an error: {e}")

        keywords_pattern = re.compile(r'\b(pin|emote|matcherino spike)\b', re.IGNORECASE)

        if keywords_pattern.search(message.content.lower()):
            time_since_last_pin = datetime.now() - last_pin_time
            if message_counter >= pin_message_threshold or time_since_last_pin >= timedelta(minutes=10):
                embed = discord.Embed(
                    title=pin_text_title,
                    description=pin_text_description,
                    color=discord.Color.blue()
                )
                embed.set_image(url="https://media.discordapp.net/attachments/1081230446026838076/1295978303026499614/Screenshot_2024-10-16_at_1.10.35_AM.png?ex=67109d59&is=670f4bd9&hm=17bd68e3aeda4af3440fc3d4b7262f77ded55cc1d142251571561c63af1ad7ec&=&format=webp&quality=lossless&width=1196&height=192")
                await message.channel.send(embed=embed)
                message_counter = 0
                last_pin_time = datetime.now()

        if bypass_role and message.content.startswith(SECRET_COMMAND):
            embed = discord.Embed(
                title="Matcherino Brawl Stars Server Rules",
                description="Please follow the rules outlined below to ensure a positive experience for everyone.",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="1. Be respectful",
                value="Please be mindful of your language and how you communicate with others in the server.",
                inline=False
            )
            embed.add_field(
                name="2. Tournament Support",
                value="For tournament-related issues, please contact the event organizer before reaching out to Matcherino support.",
                inline=False
            )
            embed.add_field(
                name="3. Platform Support",
                value="For platform-related support, join the official Matcherino Support Server: [Matcherino Support Server](https://discord.gg/matcherino).",
                inline=False
            )
            embed.add_field(
                name="4. Application Status",
                value="Please avoid spamming about application statuses. The program is currently at capacity. Keep an eye on the announcements channel for updates.",
                inline=False
            )
            embed.add_field(
                name="5. Advertising Events",
                value="Do not advertise events or streams. Organizers can share their events in the designated tournament announcement channels only.",
                inline=False
            )
            embed.add_field(
                name="6. FAQs",
                value=(
                    "Find FAQs in various languages here:\n"
                    "[English FAQ](https://matcherino.com/FAQeng)\n"
                    "[Spanish FAQ](https://matcherino.com/FAQspa)"
                ),
                inline=False
            )
            embed.add_field(
                name="7. Brawl Stars Players",
                value="If you’re looking for information or new teammates, please use the appropriate regional chat channels.",
                inline=False
            )
            await message.channel.send(embed=embed)
            await message.delete()


        if bypass_role and message.content.startswith(SELF_ROLE_COMMAND):
            # First embed: Regions
            embed_regions = discord.Embed(
                title="Select Your Region",
                description="Please select your region by reacting with the appropriate emoji.",
                color=discord.Color.green()
            )

            # Adding region fields with emojis
            embed_regions.add_field(
                name="NA",
                value="React with 🇺🇸 to select NA",
                inline=False
            )
            embed_regions.add_field(
                name="LATAM",
                value="React with 🇧🇷 to select LATAM",
                inline=False
            )
            embed_regions.add_field(
                name="APAC",
                value="React with 🇯🇵 to select APAC",
                inline=False
            )
            embed_regions.add_field(
                name="EMEA",
                value="React with 🇪🇺 to select EMEA.",
                inline=False
            )

            # Second embed: Role
            embed_roles = discord.Embed(
                title="Select Your Role",
                description="Please select your role by reacting with the appropriate emoji.",
                color=discord.Color.blue()
            )

            # Adding role fields with emojis
            embed_roles.add_field(
                name="Organizer",
                value="React with 🎯 to select Organizer.",
                inline=False
            )
            embed_roles.add_field(
                name="Player",
                value="React with 🎮 to select Player.",
                inline=False
            )

            # Send the first embed for regions
            await message.channel.send(embed=embed_regions)

            # Send the second embed for roles
            await message.channel.send(embed=embed_roles)

            # Delete the command message
            await message.delete()
        print(f'Message from {message.author}: {message.content}')

    # When a message is deleted, log the message in the log channel
    async def on_message_delete(self, message):
        log_channel = self.get_channel(LOG_CHANNEL_ID)

        if log_channel is not None:
            embed = discord.Embed(
                title="Message Deleted",
                description=f"**Author**: {message.author}\n**Content**: {message.content}",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Message ID: {message.id}")

            await log_channel.send(embed=embed)
        else:
            print(f"Log channel with ID {LOG_CHANNEL_ID} not found.")

# Create a new instance of the client and run the bot
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

client = Client(intents=intents)
client.run(TOKEN)
