import config
import discord
from discord.ext import commands

from utils.helper import admin_only, verification_embed_dm


class Menu(discord.ui.View):
    """
    A Discord UI view that displays a menu for EMAIL VERIFICATION.
    """
    def __init__(self) -> None:
        """
        Initializes the menu view and adds a 'Verify' button to the view.
        """
        super().__init__()
        self.add_item(discord.ui.Button(
            label="Verify", custom_id='verify_email', style=discord.ButtonStyle.blurple))


class Verification(commands.Cog):

    def __init__(self,bot) -> None:
        self.bot = bot

    @commands.command()
    @admin_only()
    async def create(self,ctx):
        await ctx.channel.send("Join our exclusive community and gain access to private channels and premium content by verifying your email address. Click the button below to complete the process and unlock all the benefits of being a part of our server.", view=Menu())

    @commands.command()
    @admin_only()
    async def send(self, ctx):
        embed=verification_embed_dm()
        await ctx.author.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != config.AUTOMATE_CHANNEL:
            return
        # Compare with ID of Webhook used by Webapp to send the msg
        if message.author.id == config.AUTOMATE_WEBHOOK_ID: 
            data = message.content
            await message.delete()

            # Extract the user's ID, Roll number and old username from the message
            user_id, roll, old_user = data.split("|")
            user_id = int(user_id)

            guild = self.bot.get_guild(762774569827565569) # ID of the server
            user = guild.get_member(user_id)
            
            # Remove all the roles from the user, except the @everyone role
            for role in user.roles[1:]:
                await user.remove_roles(role)
            if roll[2] == 'f':
                Foundational = 780875583214321684
                role = discord.utils.get(guild.roles, id=Foundational)
                await user.add_roles(role)  # Foundational
            elif roll[3] == 'p':
                Programming = 924703833693749359
                role = discord.utils.get(guild.roles, id=Programming)
                await user.add_roles(role)  # Diploma Programming
            elif roll[3] == 's':
                Science = 924703232817770497
                role = discord.utils.get(guild.roles, id=Science)
                await user.add_roles(role)  # Diploma Science

            # If other users using the same email address are present in the server, remove their roles
            if old_user != 'None':
                if old_user != str(user_id):
                    old_user = int(old_user)
                    Qualifier = 780935056540827729
                    Qualifier = discord.utils.get(guild.roles, id=Qualifier)
                    mem = guild.get_member(old_user)
                    if mem:
                        for role in mem.roles[1:]:
                            await mem.remove_roles(role)
                        await mem.add_roles(Qualifier)  # Qualifier

            # Send DM to the user
            embed = verification_embed_dm()
            await user.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Verification(bot))
